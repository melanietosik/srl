#!/usr/bin/env python

"""
Statistics on number of APREDs per sentence

MT, 18-09-15
"""

import sys
import pdb
import string

if len(sys.argv) == 2:
    ### Data file in CoNLL-2009 format
    infile = sys.argv[1]
else:
    print 'Usage: python pred_stats.py <data file>'


with open(infile, 'r') as f:

    sentence = []
    predicate_count = {}
    l = 0

    for line in f:
        if line.strip():
            sentence.append(line.split('\t'))
        else:
            for field_line in sentence:
                l = len(field_line)
        
            if l in predicate_count.keys():
                predicate_count[l] += 1
            else:
                predicate_count[l] = 1
            
            sentence = []
            l = 0

    print predicate_count
    print sum(predicate_count.values())


    """
    Test set
    --------
    {16: 48, 17: 4, 14: 1468, 15: 480}
    Total: 2000

    No predicate:   1468
    1 predicate:     480
                    ----
                    1948

    (1+ predicates:    52 = 0.03%)

    2 predicates:     48
    3 predicates:      4


    Training set
    ------------
    {14: 21738, 15: 11562, 16: 2370, 17: 311, 18: 31, 19: 7, 20: 1}
    Total: 36020

    No predicate:   21738
    1 predicate:    11562
                    -----
                    33300

    (1+ predicates:   2720 = 0.08%)

    2 predicates:    2370
    3 predicates:     311
    4 predicates:      31
    5 predicates:       7
    6 predicates:       1
    """
    
