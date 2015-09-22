#!/usr/bin/env python

"""
Feature extractor for semantic role labeling

"CRFsuite requires a data set in which an item line begins with its label,
followed by its attributes separated by TAB characters."

MT, 16-09-15
"""

import sys
import pdb
import string


##########################################
### CoNLL-2009 Dependency Format (columns)

###  ID  FORM  LEMMA  PLEMMA  POS  PPOS  FEAT  PFEAT  HEAD  PHEAD  DEPREL  PDEPREL FILLPRED  PRED  APREDs
###   1     2      3       4    5     6     7      8     9     10      11       12       13    14     15


###################
### Input and usage
if len(sys.argv) == 2:
	# Data file in CoNLL-2009 format
	datafile = sys.argv[1]
else:
	print 'Usage: python srl_v*.py <data file>'


def split_features(features):
	"""
	Split morphological features in FEAT into individual features
	"""
	
	### Set default to '_'
	genus = case = number = degree = \
		person = tense = mood = definite = "_"
	
	for x in features.split('|'):
		# Genus, case, number, degree, person, tense, mood, Nicht-Definitheit
		if x in ("Masc", "Fem", "Neut"):
			genus = x
		elif x in ("Nom", "Gen", "Dat", "Acc"):
			case = x
		elif x in ("Sg", "Pl"):
			number = x
		elif x in ("Pos", "Comp", "Sup"):
			degree = x
		elif x in ("1", "2", "3"):
			person = x
		elif x in ("Pres", "Past"):
			tense = x
		elif x in ("Ind", "Subj"):
			mood = x
		elif x in ("Inf", "Psp", "Imp", "Infzu"):
			definite = x
	
	### Return individual features
	return genus, case, number, degree, person, tense, mood, definite


################################################################
### Read data file, generate output file 'out.txt' in CRF format
with open(datafile, 'r') as f, open('out.txt', 'w') as out:

	### Store single sentences
	sentence = []

	for line in f:

		### Get single sentences
		if line.strip():
			sentence.append(line.split('\t'))

		### Process single sentences
		else:
			# Only keep sentences with exactly one verb predicate
			if all(len(li) == 15 for li in sentence):

				# Store dependency fields for each word
				# { ID : [ dependency fields ] }
				sentence_dict = {}

				# Predicate ID
				pred_id = 0
				# Predicate features
				pred_feat = []
				# Is predicate?
				# (Returns true if word is predicate, false otherwise)
				is_predicate = False
				# Pedicate sense in PropBank format, e.g. explain.01
				sense = False

				# Is child?
				# (Returns true if word is syntactic child of predicate, false otherwise)
				is_child = False
				# Semantic role label
				label = ""

				# Current argument word ID
				arg_id = 0

				# IDs of syntactic children of predicate
				child_ids = []
				# Children features
				child_feat = []

				# Store output features for each word
				# { ID : [ output features ] }
				output_features = {}
				# Helper list
				tmp_feat = []

				# Store individual morphological features after splitting
				split_feat = []

				### Fill sentence dictionary for each line in sentence
				for field_line in sentence:
					sentence_dict[field_line[0]] = field_line

				### Get predicate ID
				for x in range (1,len(sentence_dict)+1):
					if sentence_dict[str(x)][12] == 'Y':
						pred_id = sentence_dict[str(x)][0]
						sense = sentence_dict[str(x)][13]

				### Store predicate features
				for i in (1,2,4,6,10):
					pred_feat.append(sentence_dict[pred_id][i])
				pred_feat.append(sense)

				### Get IDs of children of predicate
				for x in range (1,len(sentence_dict)+1):
					if sentence_dict[str(x)][8] == pred_id:
						child_ids.append(str(x))

				### Store children features
				for i in child_ids:
					for j in (1,2,4,6,10):
						child_feat.append(sentence_dict[i][j])

				########################################################
				#<! Comment out features you don't want to use below !>#
				########################################################

				#####################
				### BASELINE FEATURES
				for x in range (1,len(sentence_dict)+1):
					for j in (14,1,2,4,6,10):
						tmp_feat.append(sentence_dict[str(x)][j])
					output_features[x] = tmp_feat
					tmp_feat = []

				#######################
				### ADDITIONAL FEATURES
				for x in range (1,len(sentence_dict)+1):

					######################
					### PREDICATE FEATURES
					for y in pred_feat:
						output_features[x].append(y)

					# Is predicate? feature
					is_predicate = True if str(x) == pred_id else False
					output_features[x].append(str(is_predicate))

					#####################
					### Is child? feature
					is_child = True if str(x) in child_ids else False
					output_features[x].append(str(is_child))

					#################################
					## CHILDREN OF PREDICATE FEATURES
					#################################
					for z in child_feat:
						output_features[x].append(z)

					#################################
					### SPLIT MORPHOLOGICAL FEATURES
					################################
					# Split FEAT
					for f in split_features(str(output_features[x][4])):
						split_feat.append(f)

					# Append to output features
					for f in split_feat:
						output_features[x].append(f)
					# Reset split features
					split_feat = []

					############################
					### Generate output features

					### Append label to front
					### CRF format: LABEL ATTR1 ATTR2 ...
					output_features[x][0] = str(output_features[x][0]).strip()

					### Write output to out.txt
					out.write('\t'.join(output_features[x]))
					out.write('\n')
			
			### Reset sentence
			sentence = []
				
