#!/usr/bin/env python3

import argparse
import seed as s


a = argparse.ArgumentParser(description="Triple Triad RNG manipulation utility.")
a.add_argument('action', choices=['spread', 'abolish'], help="action")
a.add_argument('target', help="target of action")
a.add_argument('--rules', '-r', nargs='+', default=[], help="current rules")
a.add_argument('--carry', '-c', nargs='+', default=[], help="carry rules")
a.add_argument('--seed', '-s', type=int, default=1, help="start seed")
a.add_argument('--queen-in-region', '-q', action="store_true", help="if queen is present in region")
a.add_argument('--challenging-queen', '-x', action="store_true", help="if you are challenging the queen. implies queen is in the region")
args = a.parse_args()

# For queen in region if you're challening the queen.
if args.challenging_queen:
    args.queen_in_region = True

seed = s.SeeD.load('random.dat')

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
    idx, reason = s.find_abolish(seed, args.seed, args.rules, args.carry, args.target) 
elif args.action == 'spread':
    idx, reason = s.find_spread(seed, args.seed, args.rules, args.carry, args.target)

if reason is not None:
    print("No opportunitiy to %s %s could be found." % (args.action, args.target))
    print("Reason: %s" % reason)
else:
    print("An opportunity to %s %s exists at seed %d." % (args.action, args.target, idx))
    steps = s.compress_list(s.calculate_steps(seed, idx, args.seed, args.rules, args.carry, args.queen_in_region, args.challenging_queen))
    print("Steps to achieve:")
    for step in steps:
        print("\t- %s" % step)
