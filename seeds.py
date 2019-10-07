#!/usr/bin/env python3

import argparse
import rand
import rules

def get_magazine(value):
    if value >= 256:
        return None
    if value >= 128:
        return "[There's nothing of interest here.]"
    if value >= 112:
        return "[Mother's Day-1 day massage ticket]"
    if value >= 96:
        return "[OK Shop-1 Rental discount ticket]"
    if value >= 80:
        return "[Aphrora Pub-1 drink discount ticket]"
    if value >= 72:
        return "Geezard Card"
    if value >= 64:
        return "Occult Fan II/Nothing"
    if value >= 48:
        return "Antidote"
    if value >= 32:
        return "Soft"
    if value >= 16:
        return "Phoenix Down"
    if value >= 0:
        return "Potion"
    return None

def process_ranges(func, values):
    for v in values:
        if v == 'all':
            for i in range(1, len(seed_data) + 1):
                func(seed_data[i], i)
        elif '-' in v:
            r = v.split('-')
            start = int(r[0])
            finish = int(r[1])
            for d in range(start, finish + 1):
                func(seed_data[d], d)
        elif ',' in v:
            for d in v.split(','):
                func(seed_data[int(d)], int(d))
        else:
            func(seed_data[int(v)], int(v))


a = argparse.ArgumentParser(description='RNG seed data utility.')
a.add_argument('command', choices=['print', 'get', 'get_rules', 'get_abolish', 'get_adopt', 'get_mags'], help='command')
a.add_argument('ranges', nargs='+', help='ranges of seeds relevant to the action')
a.add_argument('--random-file', '-f', default='random.dat', help='filename of random data to load')
args = a.parse_args()

# Load the seed data from a file.
seed_data = rand.load(args.random_file)

# Print will output the raw seed numbers.
if args.command == 'print':
    # All subcommands for print will be seed numbers and ranges.
    process_ranges(lambda x,y: print(x), args.ranges)

# Get returns a table of all relevant seed number information.
elif args.command == 'get':
    seed_list = []
    value_list = []
    rule_list = []
    abolish_list = []
    adopt_list = []
    process_ranges(lambda x,y : seed_list.append(y), args.ranges)
    process_ranges(lambda x,y : value_list.append(x), args.ranges)
    process_ranges(lambda x,y : rule_list.append(rules.get_rule(x)), args.ranges)
    process_ranges(lambda x,y : abolish_list.append('yes' if rules.can_abolish(x) else 'no'), args.ranges)
    process_ranges(lambda x,y : adopt_list.append('yes' if rules.can_abolish(x) else 'no'), args.ranges)

    print("%-6s  %-3s %-12s %-3s %-3s" % ('seed', 'val', 'rule', 'abl', 'adopt'))
    for i in range(0, len(value_list)):
        print("%-6d: %-3d %-12s %-3s %-3s" % (seed_list[i], value_list[i], rule_list[i], abolish_list[i], adopt_list[i]))

# Get rules allows us to see the rule names.
elif args.command == 'get_rules':
    process_ranges(lambda x,y : print(rules.get_rule(x)), args.ranges)

# Get rules allows us to see the rule names.
elif args.command == 'get_abolish':
    process_ranges(lambda x,y : print('yes' if rules.can_abolish(x) else 'no'), args.ranges)

# Get rules allows us to see the rule names.
elif args.command == 'get_adopt':
    process_ranges(lambda x,y : print('yes' if rules.can_abolish(x) else 'no'), args.ranges)

elif args.command == 'get_mags':
    process_ranges(lambda x,y: print("%d: %s" %(y, get_magazine(x))), args.ranges)
