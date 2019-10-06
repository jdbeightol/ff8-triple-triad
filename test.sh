#!/bin/bash -e

./triple-triad.py abolish same -c open -r same
./triple-triad.py spread open -c open -r same
./triple-triad.py spread Open -c Open -r Same -s 50
./triple-triad.py abolish Same -c Open -r Same -q -x
./triple-triad.py spread Open -c Open -r Same -x
./triple-triad.py abolish Same -c Open -r Same -q
./triple-triad.py abolish Same -c Open -r Same
./triple-triad.py spread Open -c Open -r Same
