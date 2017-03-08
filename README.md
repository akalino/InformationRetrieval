# InformationRetrieval

The goal of this project is to implement an information retrieval
system and extend it to utilize part-of-speech tagging.
The part-of-speech (POS) tagging is used to reduce the size of the
index which needs to be created for the documents. The assumption
being tested is that nouns contain most of the relevant information
in a document, thus by removing all other parts of speech in the
indexing process I would expect to see a retrieval system have a
slight decrease in recall (fewer documents retrieved) but may
potentially have an increase in precision (only relevant documents
retrieved). The base recommender system was constructed,
implementing both cosing similarity and the Okapi BM25 ranking system,
with the choice of similarity measure left to the end user.
To extend this recommender system to include part-of-speech tagging
in the construction of the index, a Hidden Markov Model (HMM) was
built and trained on the Brown corpus, available in Python's NLTK
package. This model utilizes the Viterbi algorithm for decoding of
the hidden states and prediction of new unseen instances. The end
user then has four options for retrieval system – with and without
POS tagging using either cosine or Okapi as the similarity measure.
The data set chosen for evaluation of the system was from the
Cranfield experiments, a set of 1,400 documents along with queries
and relevance judgments.

A comparison of the four retrieval methods was done for a handful of
the provided queries to determine which system was most effective.
