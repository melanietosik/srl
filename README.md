Semantic Role Labeling using Linear-Chain CRF
=============================================

NAME
----

srl_v*.py - Extracts SRL features in CRFsuite format

PREREQUISITES
--------

Get [training and test data for German](https://ufal.mff.cuni.cz/conll2009-st/data/traindev.html). You also need [CRFsuite](http://www.chokkan.org/software/crfsuite/) installed.

SYNOPSIS
--------

Specify the features you want to use in the source code (ugly, I know). Run srl_v*.py on test and training data to get output files in CRFsuite format. Note that in the paper, the development set is used as test set.

```
$ python srl_v*.py <data file>
```

Learn a CRF model from the output of the training data.

```
$ crfsuite learn -m <model name> <training data file>
```

Test the model on the test data.

```
$ crfsuite tag -qt -m <model name> <test data file>
```

Previous results on the models descriped in the paper can be found in [res.all.txt](https://github.com/melanietosik/srl/blob/master/res.all.txt).

DESCRIPTION
-----------

The task is to identify semantic arguments of sentence predicates and classify them into their semantic roles.

For example:

[ John ]<sub>AGENT</sub> hits [ Mary ]<sub>PATIENT</sub> [ with a stick ]<sub>INSTRUMENT</sub> .

Find details on the [CoNLL-2009 Shared Task website](https://ufal.mff.cuni.cz/conll2009-st/task-description.html). 

DATA FORMAT
-----------

Dependency representations following SRL [CoNLL-2009 Shared Task](https://ufal.mff.cuni.cz/conll2009-st/task-description.html).

AUTHOR
------
Melanie Tosik, tosik@uni-potsdam.de
