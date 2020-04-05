# Author: Deena Awny
# Version 19.03.2020

# [1] 2.3 Computation of semantic similarity matrix
#The objective of this phrase is to build matrix of semantic similarity scores for each pair of predicate argument strucutre.
#In this phase, similarity of the predicate argument strucutres (PASs) is computed pairwise based on acceptable comparisons
# of noun-noun, verb-verb, location-location and time-time. Based on experimental results in the literature [2], Jiang and Conrath measure has the
# closest correlation with human judgement amongst all the semantic similarity measures. Therefore, this study exploits Jiang's measure
# is information content based measure and consider that each concept in the WordNet [3] hold certain information. According to this measure,
# the similarity of two concepts is dependent on the information that two concepts share.
# Given two sentences Si and Sj, the similarity score between predicate argument structure (PAS) k of sentence Si(vik) and PAS l of sentence
# Sj(vjl) is determined using Eq.(5), where simp(vik,vjl) is the similarity between predicates (verbs) determined using Eq.(2), simarg(vik,vjl) is
# the sum of similarities between the corresponding arguments of the predicates determined using Eq.(1).
# Both equations (1) and (2) exploit Jiang's semantic similarity measure for computing similarity between noun terms in the semantic arguments
# of the predicate argument structures and the verbs of predicate argument structures, respectively. Similarity between corresponding temporal
# arguments i.e. simtmp(vik,vjl) is computed using Eq.(3) and the similarity between corresponding location arguments i.e.simloc(vik,vjl) is calculated
# using Eq.(4). Since Jiang's measure is based on WordNet, the temporal and location arguments may not be found in the WordNet, therefore we use
# edit distance algorithm instead of Jiang's measure in Eqs.(3) and (4) for computing possible match/similarity between temporal and
# location arguments of the predicates.

# The similarity score between the two predicate argument structures is computed using Eqs.(1)-(5).
# simarg(vik,vjl) = sim(A0i,A0j) + sim(A1i,A1j) + sim(A2i,A2j)
# simp(vik,vjl) = (sim(Pi,Pj))
# simtmp(vik,vjl) = (sim(Tmpi,Tmpj))
# simloc(vik,vjl) = (sim(Loci,Locj))

# Eqs.(1)-(4) are combined to give Eq.(5) as follows
# sim(vik,vjl)=simp(vik,vjl)+[simarg(vik,vjl)+simtmp(vik,vjl)+simloc(vik,vjl)]

import nltk
import numpy as np
import math
import itertools

from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic

from AgglomerativeClustering import AgglomerativeClustering
from Cluster import Cluster
from Document import Document
from Predicate import Predicate

class SemanticSimilarityMatrix:
 brown_ic = wn_ic.ic('ic-brown.dat')

def WordnetPOS(partofspeech):
  """This function returns the wordnet POS
  given partofspeech string"""
  if partofspeech == "NN":
    return wn.NOUN
  elif partofspeech == "VB":
    return wn.VERB
  else: return None

# WordnetPOS Examples
# Example 1
print(WordnetPOS("NN"))
# Example 2
print(WordnetPOS("VB"))
# Example 3
print(WordnetPOS("IN"))

#can improve this method to take the first synset with the same word
def ReturnSynset(concept, partofspeech):
  """This function returns the synset given a concept
  and  part of speech"""
  if partofspeech == None:
    return wn.synsets(concept)[0]
  elif len(wn.synsets(concept, pos=partofspeech))>0:
    return wn.synsets(concept, pos=partofspeech)[0]
  else: return None

# ReturnSynset Examples
# Example 1
print(ReturnSynset("dog", WordnetPOS("NN")))
# Example 2
print(ReturnSynset("eat", WordnetPOS("VB")))
# Example 3
print(ReturnSynset("at", WordnetPOS("IN")))

def CalculateJCNSimilarity(synset1, synset2, corpusinformationcontent):
  """This function returns the jcn similarity given"""
  if synset1 is None or synset2 is None:
    return 0
  elif synset1 == synset2:
    return 1
  else:
   return synset1.jcn_similarity(synset2, corpusinformationcontent)

brown_ic = wn_ic.ic('ic-brown.dat')
# CalculateJCNSimilarity Examples
# Example 1
print(CalculateJCNSimilarity(ReturnSynset("dog", WordnetPOS("NN")), ReturnSynset("cat",  WordnetPOS("NN")),brown_ic))
# Example 2
print(CalculateJCNSimilarity(ReturnSynset("kitten", WordnetPOS("NN")), ReturnSynset("cat", WordnetPOS("NN")),brown_ic))
# Example 3
print(CalculateJCNSimilarity(ReturnSynset("horse", WordnetPOS("NN")), ReturnSynset("cat", WordnetPOS("NN")),brown_ic))
# Example 4
print(CalculateJCNSimilarity(ReturnSynset("friend", WordnetPOS("NN")), ReturnSynset("cat", WordnetPOS("NN")),brown_ic))
# Example 5
print(CalculateJCNSimilarity(ReturnSynset("boy", WordnetPOS("NN")), ReturnSynset("girl", WordnetPOS("NN")),brown_ic))
# Example 6
print(CalculateJCNSimilarity(ReturnSynset("house", WordnetPOS("NN")), ReturnSynset("home", WordnetPOS("NN")),brown_ic))
# Example 7
print(CalculateJCNSimilarity(ReturnSynset("entrance", WordnetPOS("NN")), ReturnSynset("home", WordnetPOS("NN")),brown_ic))

# Given two sentences Si and Sj, the similarity score between predicate argument struture (PAS) k of sentence Si(vik) and PAS l of
# sentence Sj(vjl) is determined using Eq.(5), where simp(vik,vjl) is the similarity between predicates (verbs) determined using equation(2).
# simarg(vik,vjl) is the sum of similarities between the corresponding arguments of the predicates determined using Eq.(1). Both equations (1) and (2)
# exploit Jiang's semantic similarity measure for computing similarity between noun terms in the semantic arguments of the predicate argument structures
# and the verbs of the predicate argument structures, respectively.
def JCNSimBetweenArguments(argument1, argument2,corpus_ic):
  """This function returns the similarity measure between two arguments given
   the two arguments in string and the corpus information content"""
  return CalculateJCNSimilarity(ReturnSynset(argument1, WordnetPOS("NN")),ReturnSynset(argument2, WordnetPOS("NN")),corpus_ic)

brown_ic = wn_ic.ic('ic-brown.dat')
# CalculateJCNSimilarity Examples
# Example 1
print(JCNSimBetweenArguments("dog", "cat", brown_ic))
# Example 2
print(JCNSimBetweenArguments("kitten", "cat", brown_ic))
# Example 3
print(JCNSimBetweenArguments("horse","cat", brown_ic))
# Example 4
print(JCNSimBetweenArguments("friend","cat", brown_ic))

#[1] Since Jiang's measure is based on wordnet, the temporal and location arguments may not be found in the WordNet
# therefore we use edit distance algorithm instead of Jiang's measure in Eqs.(3) and (4) for computing
# possible match/similarity between temporal and location arguments of the predicates.
def InverseEditDistSimBetweenArguments(argument1, argument2):
  """This function returns the similarity measure between two arguments given
   the two arguments in string and the corpus information content"""
  editdistance= nltk.edit_distance(argument1, argument2)
  if editdistance==0:
    return 0
  else:
   return 1/editdistance

print("Inverse Edit Distance Similarity Between Arguments")
# InverseEditDistSimBetweenArguments Examples
# Example 1
print(InverseEditDistSimBetweenArguments("dog", "cat"))
# Example 2
print(InverseEditDistSimBetweenArguments("cats", "cat"))
# Example 3
print(InverseEditDistSimBetweenArguments("cat","cat"))

def SimArg(predicate1,predicate2):
  simarg0= JCNSimBetweenListOfArguments(predicate1.getArgument0Nouns(), predicate2.getArgument0Nouns())
  simarg1= JCNSimBetweenListOfArguments(predicate1.getArgument1Nouns(), predicate2.getArgument1Nouns())
  simarg2= JCNSimBetweenListOfArguments(predicate1.getArgument2Nouns(), predicate2.getArgument2Nouns())
  # missing temp and location
  simarg= simarg0 + simarg1 + simarg2
  return simarg

def SimBetweenArgumentsWithArgumentsAppended(argument1, argument2):
  simMatrix=[]
  simMatrix.append(argument2)
  for a in argument1:
    alist=[]
    for b in argument2:
      jcn= JCNSimBetweenArguments(a,b,brown_ic)
      alist.append(jcn)
    alist.insert(0,a)
    simMatrix.append(alist)
  return simMatrix

def JCNSimBetweenListOfArguments(argument1, argument2):
  simMatrix=[]
  for a in argument1:
    alist=[]
    for b in argument2:
      jcn= JCNSimBetweenArguments(a,b,brown_ic)
      alist.append(jcn)
    simMatrix.append(alist)
  x = np.matrix(simMatrix)
  return x.sum()

# http://people.cs.georgetown.edu/nschneid/cosc272/f17/05_EditDistance.pdf
# What is Word Similarity ?
# Synonymy: a binary relation
# Two words are either synonymous or not
# Similarity (or distance): a looser metric
# Two words are more similar if they share more features of meaning
# Similarity is properly a relation between senses
# The word "bank" is not similar to the word "slope"
def InverseEditDistSimBetweenListOfArguments(argument1, argument2):
  simMatrix=[]
  for a in argument1:
    alist=[]
    for b in argument2:
      jcn= InverseEditDistSimBetweenArguments(a,b)
      alist.append(jcn)
    simMatrix.append(alist)
  x = np.matrix(simMatrix)
  return x.sum()

# According to https://www.nltk.org/_modules/nltk/metrics/distance.html
def SimP(predicate1,predicate2):
  editdistance= nltk.edit_distance(predicate1.getVerb(), predicate2.getVerb())
  if editdistance==0:
   return 0
  else:
   return 1/editdistance
# edit_distance should be inverted ?

def SimTemp(predicate1, predicate2):
 return InverseEditDistSimBetweenListOfArguments(predicate1.getArgumentTempTaggedNouns(), predicate2.getArgumentTempTaggedNouns())

def SimLoc(predicate1, predicate2):
  return InverseEditDistSimBetweenListOfArguments(predicate1.getArgumentLocationTaggedNouns(), predicate2.getArgumentLocationTaggedNouns())

def SemanticSimilarityComputation(predicate1,predicate2):
  # should include
  #  + SimTemp(predicate1, predicate2) + SimLoc(predicate1, predicate2)
    return math.exp(0.05*(SimArg(predicate1, predicate2) + SimP(predicate1, predicate2)))

def findCluster(clusters, predicate):
  for c in clusters:
    if c.getPredicates() == predicate:
      return c
  return None

def createClusters(document):
  i = 1
  clusters=[]
  for p1 in document.getPredicates():
    name = "p" + str(i)
    c= Cluster(name,p1,[])
    clusters.append(c)
    i = i + 1
  return clusters

def addAverageLinkages(document, clusters):
  for p1 in document.getPredicates():
    clusterp = findCluster(clusters,p1)
    for p2 in document.getPredicates():
      ssc= SemanticSimilarityComputation(p1,p2)
      if clusterp != findCluster(clusters,p2):
        clusterp.averagelinkages.append((findCluster(clusters,p2),ssc))

def pickHighestPredicate(cluster,document):

  predicates = cluster.getPredicates()
  if isinstance(predicates,list):
    for p in predicates:
      p.setTextFeatureValue(document)
  else:
    predicates.setTextFeatureValue(document)
  maximumpredicate = predicates
  maximum =0

  if isinstance(predicates,list):
    for p in predicates:
      p.setTextFeatureValue(document)
      if p.getTextFeatureValue() > maximum :
        maximum= p.getTextFeatureValue()
        maximumpredicate = p
  else:
    predicates.setTextFeatureValue(document)
    maximum= predicates.getTextFeatureValue()

  return maximumpredicate

'''
print("----------DOCUMENT 1----------")

x = Document("""A city trader who conned millions of pounds from wealthy investors was yesterday ordered to pay back £1.

Nicholas Levene, 48, was jailed for 13 years last November after he admitted orchestrating a lucrative Ponzi scheme which raked in £316million.

He used the money to finance his own lavish lifestyle with private jets, super yachts and round-the-world trips.
""")
#for p in x.getpredicates():
# print(p.getPredicateAsString())

print("----------PREDICATES----------")
for p in x.getPredicates():
  print(p.getPredicateAsString())

print("----------TAGGED----------")
for p1 in x.getPredicates():
  # print(p.getPredicateAsStringWithTaggedPOS())
  #print(p.getArgument0TaggedNouns())

  for p2 in x.getPredicates():
    print("p1")
    print(p1.getPredicateAsStringWithTaggedPOS())
    print("p2")
    print(p2.getPredicateAsStringWithTaggedPOS())
    print("similarity")
    ssc= SemanticSimilarityComputation(p1,p2)
    print(ssc)


print("----------DOCUMENT 2----------")
x2 = Document("""Miami Heat superstar LeBron James gave a touching tribute to one of his biggest fans last night - wearing her name on his sneakers just hours after she lost a grueling six-year battle with cancer.

Bella Rodriguez-Torres, 10, loved nothing more than watching the Heat play basketball with her family. But she passed away yesterday after fighting the disease for more than half her young life.

Bella was diagnosed with an aggressive form of cancer at age four, and astounded doctors when she recovered from the illness - something her parents deemed a miracle.

But last year, her tumors returned, and, despite putting up another fierce fight, her condition deteriorated and she slipped away peacefully surrounded by family and friends.
""")

print("----------PREDICATES----------")
for p in x2.getPredicates():
  print(p.getPredicateAsString())
'''

'''
---------
Expected
---------
VERB:gave AO:Miami Heat superstar LeBron James A1:a touching tribute A2:to one of his biggest fans A-TEMP:last night - wearing her name on his sneakers just hours after she lost a grueling six-year battle with cancer A-LOC:
VERB:wearing AO:Miami Heat superstar LeBron James A1:her name A2: A-TEMP:just hours  after she lost a grueling six-year battle with cancer A-LOC:on his sneakers
VERB:lost AO:she A1:a grueling six-year battle A2:with cancer A-TEMP: A-LOC:
VERB:loved AO:Bella Rodriguez - Torres , 10 , A1:nothing more than watching the Heat play basketball with her family A2: A-TEMP: A-LOC:
VERB:watching AO: A1:the Heat play basketball with her family A2: A-TEMP: A-LOC:
VERB:passed away AO: A1:she A2: A-TEMP:yesterday  after fighting the disease for more than half her young life. A-LOC:
VERB:fighting AO:she A1:the disease A2: A-TEMP:for more than half her young life. A-LOC:
VERB:diagnosed AO: A1:Bella A2:with an aggressive form of cancer at age four A-TEMP: A-LOC:
VERB:astounded AO:Bella A1:doctors A2: A-TEMP:when she recovered from the illness - something her parents deemed a miracle A-LOC:
VERB:recovered AO:she A1: A2:from the illness A-TEMP: A-LOC:
VERB:deemed AO:her parents A1:something  a miracle A2: A-TEMP: A-LOC:
VERB:returned AO: A1:her tumors A2: A-TEMP:last year A-LOC:
VERB:putting up AO: A1:another fierce fight A2: A-TEMP: A-LOC:
VERB:deteriorated AO: A1:her condition A2: A-TEMP:last year A-LOC:
VERB:slipped AO: A1:she A2: A-TEMP: A-LOC:
VERB:surrounded AO:she A1:by family and friends A2: A-TEMP: A-LOC:


print("----------TAGGED----------")
#for each predicate - a cluster
clusters=createClusters(x2)


print("Find clusters")
addAverageLinkages(x2,clusters)
print("Two clusters to merge")
ag =  AgglomerativeClustering(clusters)
twoClustersToMerge = ag.pickTwoClustersToMerge()
print(twoClustersToMerge)
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
print(ag.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1]).name)
print("cluster names")
for c in ag.clusters:
  print(c.name)
  for a in c.averagelinkages:
    print("average linkages")
    print(a)

print("Two clusters to merge 2")
twoClustersToMerge = ag.pickTwoClustersToMerge()
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
print(ag.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1]))
print("length of clusters")
print(len(ag.clusters))
for c in ag.clusters:
  print(c.name)
  for a in c.averagelinkages:
    print("average linkages")
    print(a)
'''
'''
print("Document 3")
x3 = Document("C:/Users/admin/Documents/7lytixTest/dailymail_stories/dailymail/stories/file1.story")

print("---------- Document 3 ----------")
x3clusters=createClusters(x3)
print("Find clusters")
addAverageLinkages(x3,x3clusters)
print("Print clusters")
for c in x3clusters:
  print("cluster")
  print(c)
  print(c.averagelinkages)
ag =  AgglomerativeClustering(x3clusters)
ag.twentyPercentCompression()
for c in ag.clusters:
  print(c.name)
  predicates = c.getPredicates()
 # if isinstance(predicates,list):
   #print(len(c.getPredicates()))
   #print(c.getPredicates())
   #print(c.getPredicates())
   #print("Average linkages")
   #print(c.averagelinkages)

  print("Highest Predicate")
  highestPredicate = pickHighestPredicate(c,x3)
  print(highestPredicate. getPredicateAsStringWithTaggedPOS())
'''
'''
Example of comparing predicates
p1
VERB:loved AO: (Bella NNP)(Rodriguez NNP)(- :)(Torres NNP)(, ,)(10 CD)(, ,) A1: (nothing NN)(more RBR)(than IN)(watching VBG)(the DT)(Heat NN)(play NN)(basketball NN)(with IN)(her PRP$)(family NN) A2:  A-TEMP:  A-LOC: 
p2
VERB:watching AO:  A1: (the DT)(Heat NN)(play NN)(basketball NN)(with IN)(her PRP$)(family NN) A2:  A-TEMP:  A-LOC: 
similarity
similarity between arguments
4.872924515021515
similarity between predicates
1.2838921748281815
'''

#References
# [1] Khan, Atif, Naomie Salim, and Yogan Jaya Kumar. "A framework for multi-document abstractive summarization based on semantic role labelling." Applied Soft Computing 30 (2015): 737-747.‏
# [2] Kupiec, Julian, Jan Pedersen, and Francine Chen. "A trainable document summarizer." Proceedings of the 18th annual international ACM SIGIR conference on Research and development in information retrieval. 1995.‏
# [3] Miller, George A. "WordNet: a lexical database for English." Communications of the ACM 38.11 (1995): 39-41.‏

# Important links
# - see page 134 https://books.google.com.eg/books?id=JMm5BQAAQBAJ&pg=PA135&lpg=PA135&dq=inverse+levenshtein+distance&source=bl&ots=Id-Nact6N1&sig=ACfU3U0PWtFmhlHYjYalhNQSL3odOidFEg&hl=ar&sa=X&ved=2ahUKEwiri7iW97DoAhVSBGMBHf_OBaoQ6AEwDnoECAkQAQ#v=onepage&q=inverse%20levenshtein%20distance&f=false
# Pyramid Score - https://link.springer.com/article/10.1186/s40537-015-0020-5
# https://stackoverflow.com/questions/29846087/microsoft-visual-c-14-0-is-required-unable-to-find-vcvarsall-bat
# links - https://www.nltk.org/howto/wordnet.html
# link 2 - https://www.nltk.org/book/ch07.html
# link 3 - http://nilc.icmc.usp.br/nlpnet/intro.html

# User Verbnet to compare verbs -> future Improvenment
# implement a function that returns the least common subsumer -> future implementation (least common subsumer wordnet - https://www.nltk.org/howto/wordnet.html)
# print semantic similarity matrix -> future Implementation -
# inferring new predicate argument structures from the already computed in the knowledge base.-> future implementation
