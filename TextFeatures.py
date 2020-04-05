# Author: Deena Awny
# Version: 21.03.2020

import numpy as np

class TextFeatures:

 def __init__(self, predicate, document):
  self.predicate= predicate
  self.document = document

# take the average
# improved by genetic algorithm for optimal feature weighting -> future implementation
 def predicateTextFeatureCal(self, predicate, document):
   return (1/5*p_F2(predicate,document))+(1/5*p_F4(predicate,document))+(1/5*p_F5(predicate))+(1/5*p_F6(predicate))+(1/5*p_F7(predicate))

#[1] 2.5.1.1 Title Feature
# This feature is determined by counting the number of matching contents words in the predicate argument structure and the title of the document
# P_F1= Number of title words in PAS/Number of words in document title
# so far documents do not have titles => future implementation
#TODO
def p_F1(predicate,document):
  return 0

#[1] 2.5.1.2 Length of predicate argument structure
# We use the normalize length of the PAS, which is the ratio of number of words in the PAS
# over the number of words in the longest PAS of the document
# P_F2= Number of words occuring in the PAS/ Number of words occuring in the longest PAS
def longestPredicate(document):
  longestpredicate = None
  length=0
  for p in document.getPredicates():
    lengthofpredicate= p.lengthOfPredicate()
    if lengthofpredicate > length:
      length = lengthofpredicate
      longestpredicate = p
  return longestpredicate

def longestPredicateGivenPredicates(predicates):
  longestpredicate = None
  length=0
  for p in predicates:
    lengthofpredicate= p.lengthOfPredicate()
    if lengthofpredicate > length:
      length = lengthofpredicate
      longestpredicate = p
  return longestpredicate

def p_F2(predicate,document):
  return predicate.lengthOfPredicate()/longestPredicate(document).lengthOfPredicate()

print("p_F2 Example")
# p_F2 Examples
# Example 1
'''
d1 = Document("""A city trader who conned millions of pounds from wealthy investors was yesterday ordered to pay back £1.

Nicholas Levene, 48, was jailed for 13 years last November after he admitted orchestrating a lucrative Ponzi scheme which raked in £316million.

He used the money to finance his own lavish lifestyle with private jets, super yachts and round-the-world trips.
""")
for p in d1.getPredicates():
  print(p_F2(p, d1))
'''

#[1] 2.5.1.3 PAS to PAS Similarity
# For each predicate argument structure P, the semantic similarity between P and other predicate argument structures
# in the document collection is computed using Eq.(5). Once the similarity score for each predicate argument structure
# (PAS) is achieved, then the score of this feature is obtained by computing the ratio of sum of similarities of PAS P
# with all other PASs over the maximum of summary in the document collection.
def maximumPASToPASSimilarity(semanticsimilaritymatrix):
  matrix = np.matrix(semanticsimilaritymatrix)
  sum = matrix.sum(axis=1)
  return   sum.max()

# MaximumPASToPASSimilarity Examples
print("MaximumPASToPASSimilarity Examples")
# Example 1
print(maximumPASToPASSimilarity([[1],[4]]))
# Example 2
print(maximumPASToPASSimilarity([[1,2],[3,4]]))
# Example 3
print(maximumPASToPASSimilarity([[ 0,  1,  2,  3],
                                [ 4,  5,  6,  7],
                                [ 8,  9, 10, 11]]))

def p_F3(predicateindex, semanticsimilaritymatrix):
  matrix = np.matrix(semanticsimilaritymatrix)
  sum = matrix.sum(axis=1)
  return sum[predicateindex-1][0,0]/maximumPASToPASSimilarity(semanticsimilaritymatrix)

# P_F3 Examples
print("p_F3 Examples")
# Example 1
print(p_F3(1, [[1],[4]]))
# Example 2
print(p_F3(2,[[1,2],[3,4]]))
# Example 3
print(p_F3(1,[[ 0,  1,  2,  3],
              [ 4,  5,  6,  7],
              [ 8,  9, 10, 11]] ))

#[1] 2.5.1.4 Position of predicate argument structure
# Position of PAS [33] gives importance of the PAS in the text document and is equivalent
# to position of sentence from which PAS is extracted. Consider 10 sentences in the document,
# the score of position feature is 10/10 for the first sentence, 9/10 for the second sentence
# and so on. The score of this feature is computed as follows:
# P_F4= Length of document - PAS position + 1/ Length of document
def p_F4(predicate,document):
  return (document.lengthOfDocument() - predicate.getPosition() + 1)/ document.lengthOfDocument()
'''
d1 = Document("""A city trader who conned millions of pounds from wealthy investors was yesterday ordered to pay back £1.

Nicholas Levene, 48, was jailed for 13 years last November after he admitted orchestrating a lucrative Ponzi scheme which raked in £316million.

He used the money to finance his own lavish lifestyle with private jets, super yachts and round-the-world trips.
""")
print("p_F4 Examples")
for p in d1.getPredicates():
  print(p_F4(p, d1))
'''

#[1] 2.5.1.5 Proper nouns
# The predicate argument structure that contains more proper nouns is considered as significant
# for inclusion in summary generation. This feature identifies proper nouns as words beginning
# with a capital letter. The score of this feature is computed as the ratio of the number of
# proper nouns in the PAS over the length of the PAS [33]. Length of PAS is the number of words/terms
# in the PAS.
def p_F5(predicate):
  return predicate.numberOfProperNouns()
  #return predicate.numberOfProperNouns()/predicate.lengthOfPredicate()
'''
d1 = Document("""A city trader who conned millions of pounds from wealthy investors was yesterday ordered to pay back £1.

Nicholas Levene, 48, was jailed for 13 years last November after he admitted orchestrating a lucrative Ponzi scheme which raked in £316million.

He used the money to finance his own lavish lifestyle with private jets, super yachts and round-the-world trips.
""")
print("p_F5 Examples")
for p in d1.getPredicates():
  print(p.getPredicateAsStringWithTaggedPOS())
  print(p_F5(p))
'''

#[1] 2.5.1.6 Numerical data
# The predicate argument structure containing numerical data such as number of people killed,
# is regarded as important for inclusion in summary generation. The score for this feature
# is calculated as the number of numerical data in the PAS over the length of the PAS [33].
# P_F6 = Number of numerical data in the PAS/Length of PAS

# In case of numerical data this is saved as CD
def p_F6(predicate):
  return len(predicate.getNumericalData())
  #return len(predicate.getNumericalData())/predicate.lengthOfPredicate()
'''
d1 = Document("""A city trader who conned millions of pounds from wealthy investors was yesterday ordered to pay back £1.

Nicholas Levene, 48, was jailed for 13 years last November after he admitted orchestrating a lucrative Ponzi scheme which raked in £316million.

He used the money to finance his own lavish lifestyle with private jets, super yachts and round-the-world trips.
""")
print("p_F6 Examples")
for p in d1.getPredicates():
  print(p.getPredicateAsStringWithTaggedPOS())
  print(p_F6(p))
'''

#[1] 2.5.1.7 Number of nouns and verbs.
# Some sentences may have more than one predicate argument structure associated with them,
# represented by a composite predicate argument structure and considered important for
# summary. The score of this feature [34] is computed as follows:
# P_F7= Total number of nouns and verbs in the PAS/Length of PAS
def p_F7(predicate):
  nounsLen= len(predicate.getNouns())
  if predicate.getVerb() == "":
   verbsLen= 0
  else:
   verbsLen= 1
  totalNounsAndVerbs= nounsLen + verbsLen
  return totalNounsAndVerbs
  #return totalNounsAndVerbs/predicate.lengthOfPredicate()
'''
d1 = Document("""A city trader who conned millions of pounds from wealthy investors was yesterday ordered to pay back £1.

Nicholas Levene, 48, was jailed for 13 years last November after he admitted orchestrating a lucrative Ponzi scheme which raked in £316million.

He used the money to finance his own lavish lifestyle with private jets, super yachts and round-the-world trips.
""")
print("p_F7 Examples")
for p in d1.getPredicates():
  print(p.getPredicateAsStringWithTaggedPOS())
  print(p_F7(p))
'''

#[1] 2.5.1.8 Temporal feature.
# The predicates arguments structure containing time and date information for an event is considered
# as important for summary generation. The score of this feature is computed as ratio of the number of
# temporal information (time and date) in the PAS over the length of PAS[35].
# P_F8= Number of temporal information in the PAS/Length of PAS
#TODO
def p_F8(predicate,document):
  return 0

#[1] 2.5.1.9 Frequent semantic term.
# Frequent terms are most probably related to the topic of the document and in this study we consider
# top 10 as maximum number of frequent semantic terms. Nouns and verbs are considered as frequent
# semantic terms in the predicate argument structure. The score of this feature is calculated as the
# ratio of number of frequent semantic terms in the PAS over the maximum number of frequent semantic terms.
# P_F9= Number of frequent semantic terms in the PAS/Max(Number of frequent semantic terms) [2]
# UNFINISHED
#TODO
def p_F9(predicate,document):
  return 0

#TODO
#[1] 2.5.1.10 Semantic term weight.
# The score of important term Wi can be determined by the TF-IDF method[36]. We apply TF-IDF method
# to the predicate argument structures in the document collection and consider the term weights for
# semantic terms i.e. nouns and verbs in the predicate argument structure.
# The weight of semantic term is calculated as follows:
# Wi = Tfi * Idfi = Tfi * log(N/ni)
# where Tfi is the term frequency of the semantic term i in the document, N is
# the total number of documents, and ni is the number of documents in which the term i occurs.
# This feature is computed as the ratio of sum of weights of all semantic terms in the PAS over
# the maximum summary of the term weights of PAS in the document collection [3].
# P_F10 = ...
def tFi(term, documentContent):
   return documentContent.count(term)

def numberOfdocuments(documentCollection, term):
  documentsCount= 0
  for d in documentCollection:
    if tFi(term,d) > 0:
      documentsCount = documentsCount + 1
  return documentsCount

def termWeight(term, documentContent, documentCollection):
  return tFi(term, documentContent) * np.math.log(documentCollection.totalNumberOfDocument()/numberOfdocuments(documentCollection,term))

def p_F10(predicate, documentContent, documentCollection):
  nouns= predicate.getNouns()
  verb = predicate.getVerb()
  semanticTerms = nouns + verb
  sumOfTFi = 0
  for s in semanticTerms:
    sumOfTFi = sumOfTFi + termWeight(s, documentContent, documentCollection)

  return sumOfTFi

'''
d1 = Document("""A city trader who conned millions of pounds from wealthy investors was yesterday ordered to pay back £1.

Nicholas Levene, 48, was jailed for 13 years last November after he admitted orchestrating a lucrative Ponzi scheme which raked in £316million.

He used the money to finance his own lavish lifestyle with private jets, super yachts and round-the-world trips.
""")

print("p Examples")
for p in d1.getPredicates():
  print(p.getPredicateAsStringWithTaggedPOS())
  print(self.predicateTextFeatureCal(p))
'''

# References
# [1] Khan, Atif, Naomie Salim, and Yogan Jaya Kumar. "A framework for multi-document abstractive summarization based on semantic role labelling." Applied Soft Computing 30 (2015): 737-747.‏
# [2] Aksoy, Cem, et al. "Semantic argument frequency-based multi-document summarization." 2009 24th International Symposium on Computer and Information Sciences. IEEE, 2009.‏
# [3] Suanmali, Ladda, Naomie Salim, and Mohammed Salem Binwahlan. "Fuzzy logic based method for improving text summarization." arXiv preprint arXiv:0906.4690 (2009).‏
