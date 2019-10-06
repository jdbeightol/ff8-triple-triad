#!/usr/bin/env python3

class SeeD():
    @staticmethod
    def load(filename):
        with open(filename, 'rb') as dat_file:
            return SeeD(dat_file.read())

    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index-1]

    def get_rule(self, index):
        if self.data[index-1] >= 224:
            return "Elemental"
        if self.data[index-1] >= 192:
            return "Same Wall"
        if self.data[index-1] >= 160:
            return "Open"
        if self.data[index-1] >= 128:
            return "Sudden Death"
        if self.data[index-1] >= 96:
            return "Random"
        if self.data[index-1] >= 64:
            return "Plus"
        if self.data[index-1] >= 32:
            return "Same"
        if self.data[index-1] >= 0:
            return "Open"

    def can_abolish(self, index):
        return self.data[index-1] >= 128

    def can_adopt(self, index):
        return self.data[index-1] < 64

def find_abolish(seed, start, current_rules, carry_rules, target):
    spreadable_rules = []
    for r in carry_rules:
        if r not in current_rules:
            spreadable_rules.append(r)
    if len(spreadable_rules) == 0:
        return 0, "cannot mix rules"
    if target not in current_rules:
        return 0 , "target rule does not exist in current rules"
    for i in range(start, len(seed) - 2):
        if seed.get_rule(i+2) == target and seed.can_abolish(i+3):
            if len(carry_rules) == 0 or seed.get_rule(i) not in spreadable_rules \
                    and seed.get_rule(i+1) not in spreadable_rules \
                    and seed.get_rule(i+2) not in spreadable_rules:
                return i, None
    return 0, "exhausted seed candidates"

def find_spread(seed, start, current_rules, carry_rules, target):
    spreadable_rules = []
    for r in carry_rules:
        if r not in current_rules:
            spreadable_rules.append(r)
    if len(spreadable_rules) == 0:
        return 0, "cannot mix rules"
    if target not in spreadable_rules:
        return 0, "target rule does not exist in spreadable rules"
    for i in range(start, len(seed) - 2):
        candidate_rules = [seed.get_rule(i), seed.get_rule(i+1), seed.get_rule(i+2)]
        if target in candidate_rules:
            for r in spreadable_rules:
                if r in candidate_rules and r != target:
                    break
            else:
                return i, None
    return 0, "exhausted seed candidates"

def calculate_steps(seed, index, start, current_rules, carry_rules, queen, q_challenge):
    # Assume we will always be challenging + mixing rules.  Add 1 for queen.
    challenge = 2
    if queen:
        challenge += 1
    if q_challenge:
        challenge += 1
    play = 4
    step = start
    steps = []
    while step < index - challenge:
        if index - step >= challenge + play \
                and not seed.can_adopt(step) \
                and is_play_safe(seed, index, current_rules, carry_rules, queen):
            steps.append("challenge and play")
            step += challenge + play
        elif index - step >= challenge \
                and not seed.can_adopt(step):
            steps.append("challenge and decline")
            step += challenge
        else:
            steps.append("read a magazine or draw a spell")
            step += 1
    steps.append("challenge and play")
    return steps

def is_play_safe(seed, index, current_rules, carry_rules, queen):
    scary_rules = []
    for r in carry_rules:
        if r not in current_rules:
            scary_rules.append(r)
    d = [seed.get_rule(index), seed.get_rule(index+1), seed.get_rule(index+2)]
    for s in scary_rules:
        if s in d:
            return False
    if seed.get_rule(index+2) in current_rules:
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
