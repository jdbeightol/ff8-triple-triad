#!/usr/bin/python

import argparse
import csv
import math


class SeeD():
    def __init__(this, data):
        this.data = {int(d[0]): [int(d[1]), d[2]] for d in data}

    def __len__(this):
        return len(this.data)

    def __getitem__(this, index):
        return this.data[index]

    def get_rule(this, index):
        return this.data[index][1]

    def abolish(this, index):
        return this.data[index][0] >= 128


def find_abolish(dat, start, current_rules, carry_rules, target):
    spreadable_rules = []
    for r in carry_rules:
        if r not in current_rules:
            spreadable_rules.append(r)
    for i in range(start, len(dat) - 4):
        if dat.get_rule(i+2) == target and dat.abolish(i+3):
            if len(carry_rules) == 0 or dat.get_rule(i) not in spreadable_rules \
                    and dat.get_rule(i+1) not in spreadable_rules \
                    and dat.get_rule(i+2) not in spreadable_rules:
                return i
    return -1

def find_spread(dat, start, current_rules, carry_rules, target):
    spreadable_rules = []
    for r in carry_rules:
        if r not in current_rules:
            spreadable_rules.append(r)
    if target not in spreadable_rules:
        return -1
    for i in range(start, len(dat) - 1):
        candidate_rules = [dat.get_rule(i), dat.get_rule(i+1), dat.get_rule(i+2)]
        if target in candidate_rules:
            for r in spreadable_rules:
                if r in candidate_rules and r != target:
                    break
            else:
                return i
    return -1

def calculate_steps(dat, index, start, current_rules, carry_rules, queen):
    # Assume we will always be challenging + mixing rules.  Add 1 for queen.
    challenge = 3 if queen else 2
    play = 4
    seed = start
    steps = []
    while seed < index - challenge:
        if index - seed >= challenge + play \
                and is_play_safe(dat, index, current_rules, carry_rules, queen):
            steps.append("challenge and play")
            seed += challenge + play
        elif index - seed >= challenge:
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
    d = [dat.get_rule(i), dat.get_rule(i+1), dat.get_rule(i+2)]
    for s in scary_rules:
        if s in d:
            return False
    if dat.get_rule(i+2) in current_rules:
        return False
    return True


a = argparse.ArgumentParser(description="Triple Triad RNG manipulation utility.")
a.add_argument('action', choices=['spread', 'abolish'], help="action")
a.add_argument('target', help="target of action")
a.add_argument('--rules', '-r', nargs='+', default=[], help="current rules")
a.add_argument('--carry', '-c', nargs='+', default=[], help="carry rules")
a.add_argument('--seed', '-s', type=int, default=1, help="start seed")
a.add_argument('--queen', '-q', action="store_true", help="if queen is present in region")
args = a.parse_args()

dat = None
with open('seed.dat', 'r') as csv_file:
    dat = SeeD(csv.reader(csv_file))

print("Given the following rules in a region:")
for rule in args.rules:
    print("\t- %s" % rule)

if len(args.rules) == 0:
    print("\t- None")

print("\nAnd the following carried rules:")
for rule in args.carry:
    print("\t- %s" % rule)
if len(args.carry) == 0:
    print("\t- None")

print("\nWith the queen%s in the region.\n" % ("" if args.queen else " not"))

i = 0
if args.action == 'abolish':
    i = find_abolish(dat, args.seed, args.rules, args.carry, args.target) 

elif args.action == 'spread':
    i = find_spread(dat, args.seed, args.rules, args.carry, args.target)

if i == -1:
    print("No %s opportunitiy could be found for %s." % (args.action, args.target))
else:
    print("%s %s opporunity exists for %s at seed %d." % ("A" if args.action == "spread" else "An", args.action, args.target, i))
    steps = calculate_steps(dat, i, args.seed, args.rules, args.carry, args.queen)
    print("\nSteps to reach:")
    for step in steps:
        print("\t- %s" % step)
