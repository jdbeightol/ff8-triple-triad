#!/usr/bin/env python3

import argparse
import csv
import math


class SeeD():
    @staticmethod
    def load(filename):
        # with open(filename, 'r') as csv_file:
        #     return SeeD(csv.reader(csv_file))
        with open(filename, 'rb') as dat_file:
            return SeeD(dat_file.read())

    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def get_rule(self, index):
        if self.data[index] >= 224:
            return "Elemental"
        if self.data[index] >= 192:
            return "Same Wall"
        if self.data[index] >= 160:
            return "Open"
        if self.data[index] >= 128:
            return "Sudden Death"
        if self.data[index] >= 96:
            return "Random"
        if self.data[index] >= 64:
            return "Plus"
        if self.data[index] >= 32:
            return "Same"
        if self.data[index] >= 0:
            return "Open"

    def abolish(self, index):
        return self.data[index] >= 128

    def adopt(self, index):
        return self.data[index] < 64

def find_abolish(dat, start, current_rules, carry_rules, target):
    spreadable_rules = []
    for r in carry_rules:
        if r not in current_rules:
            spreadable_rules.append(r)
    if len(spreadable_rules) == 0:
        return 0, "cannot mix rules"
    if target not in current_rules:
        return 0 , "target rule does not exist in current rules"
    for i in range(start, len(dat) - 4):
        if dat.get_rule(i+2) == target and dat.abolish(i+3):
            if len(carry_rules) == 0 or dat.get_rule(i) not in spreadable_rules \
                    and dat.get_rule(i+1) not in spreadable_rules \
                    and dat.get_rule(i+2) not in spreadable_rules:
                return i, None
    return 0, "exhausted seed candidates"

def find_spread(dat, start, current_rules, carry_rules, target):
    spreadable_rules = []
    for r in carry_rules:
        if r not in current_rules:
            spreadable_rules.append(r)
    if len(spreadable_rules) == 0:
        return 0, "cannot mix rules"
    if target not in spreadable_rules:
        return 0, "target rule does not exist in spreadable rules"
    for i in range(start, len(dat) - 1):
        candidate_rules = [dat.get_rule(i), dat.get_rule(i+1), dat.get_rule(i+2)]
        if target in candidate_rules:
            for r in spreadable_rules:
                if r in candidate_rules and r != target:
                    break
            else:
                return i, None
    return 0, "exhausted seed candidates"

def calculate_steps(dat, index, start, current_rules, carry_rules, queen, q_challenge):
    # Assume we will always be challenging + mixing rules.  Add 1 for queen.
    challenge = 2
    if queen:
        challenge += 1
    if q_challenge:
        challenge += 1
    play = 4
    seed = start
    steps = []
    while seed < index - challenge:
        if index - seed >= challenge + play \
                and not dat.adopt(seed) \
                and is_play_safe(dat, index, current_rules, carry_rules, queen):
            steps.append("challenge and play")
            seed += challenge + play
        elif index - seed >= challenge \
                and not dat.adopt(seed):
            steps.append("challenge and decline")
            seed += challenge
        else:
            steps.append("read a magazine or draw a spell")
            seed += 1
    steps.append("challenge and play")
    return steps

def is_play_safe(dat, index, current_rules, carry_rules, queen):
    scary_rules = []
    for r in carry_rules:
        if r not in current_rules:
            scary_rules.append(r)
    d = [dat.get_rule(index), dat.get_rule(index+1), dat.get_rule(index+2)]
    for s in scary_rules:
        if s in d:
            return False
    if dat.get_rule(index+2) in current_rules:
        return False
    return True

def compress_list(l):
    cur = None
    cnt = 0
    compressed_list = []
    for i in l:
        if i == cur:
            cnt = cnt + 1
        else:
            if cur != None:
                compressed_list.append(compress(cur, cnt))
            cur = i
            cnt = 1
    compressed_list.append(compress(cur, cnt))
    return compressed_list

def compress(item, count):
    if count > 1:
        return("%s x%d" % (item, count))
    else:
        return(item)


a = argparse.ArgumentParser(description="Triple Triad RNG manipulation utility.")
a.add_argument('action', choices=['spread', 'abolish'], help="action")
a.add_argument('target', help="target of action")
a.add_argument('--rules', '-r', nargs='+', default=[], help="current rules")
a.add_argument('--carry', '-c', nargs='+', default=[], help="carry rules")
a.add_argument('--seed', '-s', type=int, default=0, help="start seed")
a.add_argument('--queen-in-region', '-q', action="store_true", help="if queen is present in region")
a.add_argument('--challenging-queen', '-x', action="store_true", help="if you are challenging the queen. implies queen is in the region")
args = a.parse_args()

# For queen in region if you're challening the queen.
if args.challenging_queen:
    args.queen_in_region = True

dat = SeeD.load('random.dat')

print("Given:")
print("\tThe following rules in the target region:")

for rule in args.rules:
    print("\t\t- %s" % rule)

if len(args.rules) == 0:
    print("\t\t- None")

print("\n\tThe following carried rules:")

for rule in args.carry:
    print("\t\t- %s" % rule)

if len(args.carry) == 0:
    print("\t\t- None")

print("\n\tNo random environmental effects can interfere with the random number generator.")

print("\n\tYou are%s challenging the queen."% ("" if args.challenging_queen else " not"))

print("\n\tThe queen is%s in the target region.\n" % ("" if args.queen_in_region else " not"))

idx = 0
reason = None
if args.action == 'abolish':
    idx, reason = find_abolish(dat, args.seed, args.rules, args.carry, args.target) 
elif args.action == 'spread':
    idx, reason = find_spread(dat, args.seed, args.rules, args.carry, args.target)

if reason is not None:
    print("No opportunitiy to %s %s could be found." % (args.action, args.target))
    print("Reason: %s" % reason)
else:
    print("An opportunity to %s %s exists at seed %d." % (args.action, args.target, idx))
    steps = compress_list(calculate_steps(dat, idx, args.seed, args.rules, args.carry, args.queen_in_region, args.challenging_queen))
    print("Steps to achieve:")
    for step in steps:
        print("\t- %s" % step)
