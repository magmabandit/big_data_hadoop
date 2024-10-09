#!/usr/bin/env python
"""reducer.py"""

from operator import itemgetter
import sys

current_prez = None
current_val = 0
num_words = 0
prez = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    prez_pair = line.split('\t')
    prez = prez_pair[0]
    val = prez_pair[1]

    # convert count (currently a string) to int
    try:
        val = int(val)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue
    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_prez == prez:
        # take the AVERAGE valence. We need to keep track of the total words spoken by the prez as well
        current_val += (val / num_words)
        num_words += 1
    else:
        if current_prez:
            # write result to STDOUT
            print ('%s\t%s' % (current_prez, current_val))
        current_prez = prez
        current_val = (val / num_words)

# do not forget to output the last word if needed!
if current_prez == prez:
    print ('%s\t%s' % (current_prez, current_val))