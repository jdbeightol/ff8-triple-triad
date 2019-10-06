#!/usr/bin/env python3

def get_rule(value):
    if value >= 256:
        return None
    if value >= 224:
        return "Elemental"
    if value >= 192:
        return "Same Wall"
    if value >= 160:
        return "Open"
    if value >= 128:
        return "Sudden Death"
    if value >= 96:
        return "Random"
    if value >= 64:
        return "Plus"
    if value >= 32:
        return "Same"
    if value >= 0:
        return "Open"
    return None

def can_abolish(value):
    return value >= 128

def can_adopt(value):
    return value < 64

def find_abolish(seed, start, current_rules, carry_rules, target):
    spreadable_rules = get_spreadable_rules(current_rules, carry_rules)
    if len(spreadable_rules) == 0:
        return 0, "cannot mix rules"
    if target not in current_rules:
        return 0 , "target rule does not exist in current rules"
    for i in range(start + 2, len(seed) - 2):
        if get_rule(seed[i+2]) == target and can_abolish(seed[i+3]):
            if len(carry_rules) == 0 or get_rule(seed[i]) not in spreadable_rules \
                    and get_rule(seed[i+1]) not in spreadable_rules \
                    and get_rule(seed[i+2]) not in spreadable_rules:
                return i, None
    return 0, "exhausted seed candidates"

def find_spread(seed, start, current_rules, carry_rules, target):
    spreadable_rules = get_spreadable_rules(current_rules, carry_rules)
    if len(spreadable_rules) == 0:
        return 0, "cannot mix rules"
    if target not in spreadable_rules:
        return 0, "target rule does not exist in spreadable rules"
    for i in range(start + 2, len(seed) - 2):
        candidate_rules = [get_rule(seed[i]), get_rule(seed[i+1]), get_rule(seed[i+2])]
        if target in candidate_rules:
            for r in spreadable_rules:
                if r in candidate_rules and r != target:
                    break
            else:
                return i, None
    return 0, "exhausted seed candidates"

def calculate_steps(seed, index, start, current_rules, carry_rules, queen, q_challenge, play_as_step=False):
    # Set up costs.
    # Assume we will always be challenging + mixing rules.
    # Add 1 for queen and another 1 for playing the queen.
    challenge = 2
    if queen:
        challenge += 1
    if q_challenge:
        challenge += 1
    # The play cost is 4.  3 for picking rules and a 4th for checking if the rule can be abolished.
    play = 4
    # The reserve cost is the required amount to save prior to the last play step.
    reserve = challenge
    step = start
    steps = []
    # Ideally, we want to maximize the number of high-cost steps when available.  Since challenging can sometimes lead to the 
    # end of mixing, order is important for these steps.  This algorithm could result in frequent 
    while index - step > reserve:
        # Playing as a step is experimental.  There are some extra variables to consider that change the number of getRandom checks.
        # See section 3.2.10 of https://pastebin.com/raw/5jv5AtcC for more information.
        if play_as_step \
                and index - step - reserve >= challenge + play \
                and not can_adopt(seed[step]) \
                and is_play_safe(seed, index, current_rules, carry_rules, queen):
            steps.append("challenge and play")
            step += challenge + play

        # Excluding play as a step, challenging is the next highest cost action.  We want to prefer it when possible, but only
        # if it won't put us past the last play attempt.
        elif index - step - reserve >= challenge \
                and not can_adopt(seed[step]):
            steps.append("challenge and decline")
            step += challenge

        # If we can't play or challenge, we must attempt to draw a spell or read a magazine.
        else:
            steps.append("read a magazine or draw a spell")
            step += 1

    # If the last step falls on a rule adoption seed, there is risk that the player might not ask to mix rules anymore.
    # Technically, this needs to happen twice and the algorithm avoids all adoption steps, so this should always be safe
    # when starting from Seed 1.
    if can_adopt(seed[step]) \
            or index - step != reserve:
        steps.append("(challenge and play)")
    else:
        steps.append("challenge and play")

    return steps

def is_play_safe(seed, index, current_rules, carry_rules, queen):
    spreadable_rules = get_spreadable_rules(current_rules, carry_rules)

    d = [get_rule(seed[index]), get_rule(seed[index+1]), get_rule(seed[index+2])]
    # Check that a carried rule will not spread during this step.
    for s in spreadable_rules:
        if s in d:
            return False

    # Check that a rule in the region won't be abolished.
    if get_rule(seed[index+2]) in current_rules and can_abolish(seed[index+3]):
        return False

    return True

def get_spreadable_rules(current_rules, carry_rules):
    spreadable_rules = []
    for r in carry_rules:
        if r not in current_rules:
            spreadable_rules.append(r)
    return spreadable_rules

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
