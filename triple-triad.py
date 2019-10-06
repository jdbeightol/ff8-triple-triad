#!/usr/bin/env python3

import argparse
import rand
import rules


a = argparse.ArgumentParser(description="Triple Triad RNG manipulation utility.")
a.add_argument('action', choices=['spread', 'abolish'], help="action")
a.add_argument('target', help="target of action")
a.add_argument('--random-file', '-f', default="random.dat", help="filename of random data to load")
a.add_argument('--rules', '-r', nargs='+', default=[], help="current rules (required for abolish)")
a.add_argument('--carry', '-c', nargs='+', default=[], help="carry rules (required for spread)")
a.add_argument('--start', '-s', type=int, default=1, help="start seed")
a.add_argument('--queen-in-region', '-q', action="store_true", help="if queen is present in region")
a.add_argument('--challenging-queen', '-x', action="store_true", help="if you are challenging the queen (implies queen in region)")
a.add_argument('--verbose', '-v', action="store_true", help="enable verbose output (assumptions, reasons, seed numbers, etc.)")
args = a.parse_args()

# Always set queen in region if you're challening the queen.
if args.challenging_queen:
    args.queen_in_region = True

# Load the seed data from a file.
seed_data = rand.load(args.random_file)

if args.verbose:
    print("Loaded %d seeds.\n" % len(seed_data))

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
    idx, reason = rules.find_abolish(seed_data, args.start, args.rules, args.carry, args.target) 
elif args.action == 'spread':
    idx, reason = rules.find_spread(seed_data, args.start, args.rules, args.carry, args.target)

if reason is not None:
    print("No opportunitiy to %s %s could be found." % (args.action, args.target))
    if args.verbose:
        print("Reason: %s" % reason)
else:
    steps = rules.compress_list(rules.calculate_steps(seed_data, idx, args.start, args.rules, args.carry, args.queen_in_region, args.challenging_queen))

    if args.verbose:
        print("An opportunity to %s %s exists at seed %d." % (args.action, args.target, idx))
    print("Steps to achieve:")
    for step in steps:
        print("\t- %s" % step)
