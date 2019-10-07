#!/usr/bin/env python3

import rand
import rules
import sys

def help():
    print('commands:')
    print('\thelp - shows this help text')
    print('\nimports:')
    print('\trand - random number generator library')
    print('\trules - triple triad rules library')
    print('\nvariables and objects:')
    print('\tcarried_rules1 - list of most recently adopted rules')
    print('\tcarried_rules2 - list of the second-most recently adopted rule')
    print('\tdata - object containing all loaded seed data')

# Detect non-interactive modes and fail.
if not bool(getattr(sys, 'ps1', sys.flags.interactive)):
    print("This script is intended to only run in an interactive shell.")
    print("Rerun with python -i %s" % sys.argv[0])
    sys.exit(1)

print('Final Fantasy VIII Triple Triad Simulator')
data = rand.load('random.dat')
print('Loaded %d seeds from random.dat\n' % len(data))
print('Type help() for available commands, variables, and information.')

carried_rules1=[]
carried_rules2=[]


# User entry point.
