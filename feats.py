#!/usr/bin/env python

"""
Return set of morphological features in training and test data

MT, 18-09-15
(Turns out I could've just googled that, it's the TIGER tag set.)
"""
import sys
import pdb
import string

if len(sys.argv) == 2:
    ### Data file in CoNLL-2009 format
    infile = sys.argv[1]
else:
    print 'Usage: python feats.py <data file>'


with open(infile, 'r') as f:

    sentence = []
    feat_set = set()

    for line in f:
        if line.strip():
            sentence.append(line.split('\t'))
        else:
            for field_line in sentence:
                for element in field_line[6].split('|'):
                    feat_set.add(element)

    for x in feat_set:
        print x,