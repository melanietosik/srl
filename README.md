Edit Distance and Sequence Alignment
====================================

NAME
----

sda - Computes various string metrics (Hamming distance, minimum edit distance, Levenshtein distance) and optimal global sequence alignment

PREREQUISITES
--------

You need [GCC](https://gcc.gnu.org/), [GNU Make](https://www.gnu.org/software/make/), and [Doxygen](http://www.stack.nl/~dimitri/doxygen/) installed.

SYNOPSIS
--------

$ make

$ make test 

$ ./bin/sda [-option] [sequence1] [sequence2]

DESCRIPTION
-----------

### EDIT DISTANCE

The edit distance, defined between two strings of not necessarily equal length, is the minimum number of **edit operations** required to transform one string into the other. An edit operation is either a _deletion_, an _insertion_, or a _substitution_ of a single character in either sequence.

As a way of quantifying how dissimilar two strings are (e.g., words or DNA sequences), edit distances find applications in [Natural Language Processing (NLP)](https://en.wikipedia.org/wiki/Natural_language_processing) and [bioinformatics](https://en.wikipedia.org/wiki/Bioinformatics). While several definitions of edit distance exist, one of the most common variants is called **Levenshtein distance**, named after Vladimir Levenshtein. 

For example, here is the operation list for computing the **Levenshtein distance** between _intention_ and _execution_ (taken from Jurafsky and Martin (2009)):

**intention** <br>&rarr; (_delete i_) <br>&rarr; **ntention** <br>&rarr; (_substitute n by e_) <br>&rarr; **etention** <br>&rarr; (_substitute t by x_) <br>&rarr; **exention** <br>&rarr; (_insert u_) <br>&rarr; **exenution** <br>&rarr; (_substitute n by c_) <br>&rarr; **execution**

Originally, Levenshtein assigned a cost of 1 for each of three operations, defining the **minimum edit distance**. Thus, the minimum edit distance between _intention_ and _execution_ is 5.

Later on, he proposed an alternate version of his metric, assigning a cost of 1 to each deletion or insertion, and a cost of 2 for each substitution. Substitutions are really an insert with a delete, hence the double weight. Using this version, the **Levenshtein distance** between _intention_ and _execution_ is 8.

To compute the edit distances, the **Wagner-Fischer algorithm** is implemented. As an instance of _dynamic programming_, it applies the typical dynamic programming matrix to compute the distance between two full strings by combining the distances between all prefixes of the first and second string. After flood filling the matrix, the edit distance between the input strings can be found in the last cell computed.

If two strings are of _equal length_, the minimum edit distance is obtained by computing the **Hamming distance**, i.e. the number of character positions where they differ. For equal-length strings, the Hamming distance also functions as upper bound on the Levenshtein distance.

See also: 

- [Hamming distance] [0] on Wikipedia
- [Edit distance] [1] on Wikipedia
- [Levenshtein distance] [2] on Wikipedia
- [Wagner-Fischer algorithm] [3] on Wikipedia
- [Dynamic programming] [4] on Wikipedia

### SEQUENCE ALIGNMENT

In bioinformatics, sequence alignment is a way of arranging the sequences of DNA, RNA, or protein, to **identify regions of similarity** that may be a consequence of _functional, structural, or evolutionary relationships_ between the sequences. It is also used for non-biological sequences, such as those present in natural language or financial data.

Generally, there are two classes of computational approaches to sequence alignment: **global alignments** and **local alignments**. While global alignments necessarily span the entire length of all query sequences, local alignments identify regions of similarity within long sequences that are often widely divergent overall.

One global alignment technique, the **Needleman–Wunsch algorithm**, is implemented here. Similar to the Wagner-Fischer algorithm, it uses a _substitution matrix to assign scores_ to amino-acid matches or mismatches, and a gap penalty for matching an amino acid in one sequence to a gap in the other. (A common extension to the standard linear gap cost is the usage of two different gap penalties for opening a gap and for extending a gap. By setting the former much larger than the latter, the number of gaps in an alignment can be reduced and residues and gaps are kept together, which typically makes more sense biologically.) While a weighted scoring matrix for DNA and RNA alignments may be used, here they are simply assigned a **positive match score** (+1), a **negative mismatch score** (-1), and a **negative gap penalty** (-1).

To find the alignment with the highest score, an **F matrix** is allocated. The entry in row _i_ and column _j_ is denoted here by F[_i_,_j_]. There is one row for each character in _sequence A_, and one column for each character in _sequence B_. Following the [principle of optimality](https://en.wikipedia.org/wiki/Bellman_equation#Bellman.27s_Principle_of_Optimality), as the algorithm progresses, F[_i_,_j_] will be assigned the optimal score for the alignment of the first _i = 0..n_ characters in _A_ and the first _j = 0..m_ characters in _B_.

Once the F matrix is computed, the entry F(_n_,_m_) gives the **maximum score** among all possible alignments. To compute one global alignment that actually gives this score, we can _trace back to the original cell_ to obtain the path for the best alignment. Note that there can be multiple best alignments; here we show just one.

Even though dynamic programming can be extended to more than two sequences and is guaranteed to find the optimal global alignment, it is _prohibitively slow for a large numbers of sequences or extremely long sequences_. The alternative are efficient, heuristic algorithms or probabilistic methods designed for large-scale database search, which do not guarantee to find best matches, or semiglobal, hybrid methods.

See also: 

- [Sequence alignment] [5] on Wikipedia
- [Needleman-Wunsch algorithm] [6] on Wikipedia


OPTION
------

**-m** &nbsp; Compute minimum edit distance

**-l** &nbsp;&nbsp;&nbsp; Compute Levenshtein distance

**-a** &nbsp;&nbsp; Compute global sequence alignment
 
**-h** &nbsp;&nbsp; Print help message

INPUT
-----

Edit distances and sequence alignment are computed for any two given strings.

In theory, the strings can of arbitrary length. Practically, you will probably run out of space for very long sequences.

If only one input string is provided, the second string is interpreted as the empty string. 

EXAMPLE
-------

**INPUT**

insertion execution

**COMMAND**

  $ ./bin/sda -m insertion execution

  $ ./bin/sda -a insertion execution
    
**OUTPUT**

  Minimum edit distance: 5
  
  Sequence A: inse-rtion<br>
  Sequence B: -execution<br>
  Maximum alignment score: 0

TO DO
-----

[Some of this, maybe.] [7] And there's many more string metrics out there! I also really want to read a good intro on bioinformatics now.

AUTHOR
------

Melanie Tosik, tosik@uni-potsdam.de

REFERENCES
----------

Jurafsky, Daniel, and James H. Martin. 2009. Speech and Language Processing: An Introduction to Natural Language Processing, Speech Recognition, and Computational Linguistics. 2nd edition. Prentice-Hall.

Needleman, Saul B.; and Wunsch, Christian D. (1970). "A general method applicable to the search for similarities in the amino acid sequence of two proteins". Journal of Molecular Biology 48 (3): 443–53.

Navarro, Gonzalo (2001). "A guided tour to approximate string matching". ACM Computing Surveys 33 (1): 31–88.

[0]: https://en.wikipedia.org/wiki/Hamming_distance
[1]: https://en.wikipedia.org/wiki/Edit_distance
[2]: https://en.wikipedia.org/wiki/Levenshtein_distance
[3]: https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm
[4]: https://en.wikipedia.org/wiki/Dynamic_programming#Dynamic_programming_in_computer_programming
[5]: https://en.wikipedia.org/wiki/Sequence_alignment
[6]: https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
[7]: https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm#Possible_modifications
