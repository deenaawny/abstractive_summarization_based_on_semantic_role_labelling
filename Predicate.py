# Author: Deena Awny
# Version: 20.03.2020

# PREDICATE ARGUMENT STRUCTURE

# CORE ARGUMENTS
# V Verb
# A0 Subject
# A1 Object
# A2 Indirect Object
# A3 Start point
# A4 End point
# A5 Direction

# ADJUNCTIVE ARGUMENTS
# ArgM-DIR Direction
# ArgM-MNR Manner
# ArgM-LOC Location
# ArgM-TMP Temporal marker
# ArgM-PRP Purpose
# ArgM-NEG Negation
# ArgM-REC Reciprocal
# AM-DIS Discourse marker
import nltk
from SennaSRL import SennaSRL as srl
from TextFeatures import TextFeatures


class Predicate:

 def __init__(self, verb, argument0, argument1, argument2, argumentTemp, argumentLocation, position, textfeaturevalue):
   self.verb = verb
   self.argument0 = argument0
   self.argument1 = argument1
   self.argument2 = argument2
   self.argumentTemp = argumentTemp
   self.argumentLocation = argumentLocation
   self.position = position
   self.textfeaturevalue = textfeaturevalue

 def __init__(self,predicate,position):
   self.setVerb(predicate)
   self.setArgument0(predicate)
   self.setArgument1(predicate)
   self.setArgument2(predicate)
   self.setArgumentTemp(predicate)
   self.setArgumentLocation(predicate)
   self.setVerbTagged()
   self.setArgument0Tagged()
   self.setArgument1Tagged()
   self.setArgument2Tagged()
   self.setArgumentTempTagged()
   self.setArgumentLocationTagged()
   self.setPosition(position)

# takes a list and sets the argument0 etc.

 def setVerb(self,predicate):
  try:
    self.verb = predicate['V']
  except KeyError as e:
    self.verb = ""

 def setVerbTagged(self):
   self.verbTagged= srl.posTagged(srl, self.verb)

 def getVerbTagged(self):
   return self.verbTagged

 def getVerb(self):
     return self.verb

 def setArgument0(self, predicate):
  try:
    self.argument0 = predicate['A0']
  except KeyError as e:
    self.argument0 = ""

 def getArgument0(self):
   return self.argument0

 def setArgument0Tagged(self):
   self.argument0Tagged= srl.posTagged(srl, self.argument0)

 def getArgument0Tagged(self):
    return self.argument0Tagged

 def getArgument0Nouns(self):
   return self.getNounsGivenTaggedContent(self.argument0Tagged)

 def setArgument1(self, predicate):
   try:
     self.argument1 = predicate['A1']
   except KeyError as e:
     self.argument1 = ""

 def getArgument1(self):
   return self.argument1

 def setArgument1Tagged(self):
   self.argument1Tagged= srl.posTagged(srl, self.argument1)

 def getArgument1Tagged(self):
   return self.argument1Tagged

 def getArgument1Nouns(self):
   return self.getNounsGivenTaggedContent(self.argument1Tagged)

 def setArgument2(self, predicate):
   try:
     self.argument2 = predicate['A2']
   except KeyError as e:
     self.argument2 = ""

 def getArgument2(self):
   return self.argument2

 def setArgument2Tagged(self):
   self.argument2Tagged= srl.posTagged(srl, self.argument2)

 def getArgument2Tagged(self):
   return self.argument2Tagged;

 def getArgument2Nouns(self):
   return self.getNounsGivenTaggedContent(self.argument2Tagged)

 def setArgumentTemp(self,predicate):
   try:
     self.argumentTemp = predicate['AM-TMP']
   except KeyError as e:
     self.argumentTemp = ""

 def getArgumentTemp(self):
   return self.argumentTemp

 def setArgumentTempTagged(self):
   self.argumentTempTagged= srl.posTagged(srl, self.argumentTemp)

 def getArgumentTempTagged(self):
   return self.argumentTempTagged

 def getArgumentTempNouns(self):
   return self.getNounsGivenTaggedContent(self.argumentTempTagged)

 def setArgumentLocation(self,predicate):
   try:
     self.argumentLocation = predicate['AM-LOC']
   except KeyError as e:
     self.argumentLocation = ""

 def getArgumentLocation(self):
   return self.argumentLocation

 def setArgumentLocationTagged(self):
   self.argumentLocationTagged= srl.posTagged(srl, self.argumentLocation)

 def getArgumentLocationTagged(self):
   return self.argumentLocationTagged

 def getArgumentLocationNouns(self):
   return self.getNounsGivenTaggedContent(self.argumentLocationTagged)

 def setPosition(self, position):
   self.position = position

 def getPosition(self):
   return self.position

 def setTextFeatureValue(self, document):
   textFeatureCalculation = TextFeatures(self, document)
   self.textfeaturevalue = textFeatureCalculation.predicateTextFeatureCal(self,document)

 def getTextFeatureValue(self):
   return self.textfeaturevalue

 def getWords(self):
   return nltk.word_tokenize(self.verb + " " + self.argument0 + " " + self.argument1 + " " + self.argument2 + " " + self.argumentTemp + " " + self.argumentLocation)

 def lengthOfPredicate(self):
   return len(self.getWords())

 def getPredicateTagged(self):
   return self.verbTagged +self.argument0Tagged + self.argument1Tagged + self.argument2Tagged + self.argumentTempTagged + self.argumentLocationTagged
 # are NNP's included ?
 # NNP's are not included in the list of nouns (wordnet does not include them)
 # how will we deal with the NNS?
 # difference between NN and NNP etc?
 def getSingularNounsAndMassNouns(self):
   nouns=[]
   for t in self.getPredicateTagged():
    if t[1] == "NN" or t[1] == "NNS":
     nouns.append(t[0])
   return nouns

 def getProperNouns(self):
   nouns=[]
   for t in self.getPredicateTagged():
     if t[1] == "NNP":
       nouns.append(t[0])
   return nouns

 def numberOfProperNouns(self):
   return len(self.getProperNouns())

 def getNouns(self):
  nouns=[]
  for t in self.getPredicateTagged():
    if t[1] == "NN" or t[1] == "NNS" or t[1] == "NNP":
      nouns.append(t[0])
  return nouns

 def getNounsGivenTaggedContent(self, taggedcontent):
   nouns=[]
   for t in taggedcontent:
     if t[1] == "NN" or t[1] == "NNS" or t[1] == "NNP":
       nouns.append(t[0])
   return nouns

 def getNumericalData(self):
  numericals=[]
  for t in self.getPredicateTagged():
    if t[1] == "CD":
      numericals.append(t[0])
  return numericals

 def getPredicateAsString(self):
  return "VERB:"+ self.verb + " AO:" + self.argument0 + " A1:" + self.argument1 + " A2:" + self.argument2 +" A-TEMP:" + self.argumentTemp + " A-LOC:" + self.argumentLocation

 # Copied function
 # Python program to convert a list
 # to string using join() function
  # Function to convert
 def listOfTuplesToString(self, s):
  # initialize an empty string
  str1 = " "
  for t in s:
    str = "("+t[0] + " " + t[1]+")"
    str1 = str1 + str
  # return string
  return (str1)

 def getPredicateAsStringWithTaggedPOS(self):
  return "VERB:" + self.verb + " AO:" + self.listOfTuplesToString(self.argument0Tagged) + " A1:" + self.listOfTuplesToString(self.argument1Tagged) + " A2:" + self.listOfTuplesToString(self.argument2Tagged) +  " A-TEMP:" + self.listOfTuplesToString(self.argumentTempTagged) + " A-LOC:" + self.listOfTuplesToString(self.argumentLocationTagged)
'''
# Predicate Example
p = Predicate({'A0': 'Sky', 'V': 'won', 'A1': 'the bidding war', 'A3': 'for the rights to screen Floyd Mayweather v Manny Pacquiao in the UK', 'AM-ADV': 'as revealed by Sportsmail last Friday'},1)

# getVerb Example
print('getVerb Example')
print(p.getVerb())
# getArgument0 Example
print('getArgument0 Example')
print(p.getArgument0())
# getArgument0Tagged Example
print('getArgument0Tagged Example')
print(p.getArgument0Tagged())
# getArgument0Nouns Example
print('getArgument0Nouns Example')
print(p.getArgument0Nouns())
# getArgument1 Example
print('getArgument1 Example')
print(p.getArgument1())
# getArgument1Tagged Example
print('getArgument1Tagged Example')
print(p.getArgument1Tagged())
print('getArgument1Nouns Example')
print(p.getArgument1Nouns())
# getArgument2 Example
print('getArgument2 Example')
print(p.getArgument2())
# getArgument2Tagged Example
print('getArgument2Tagged Example')
print(p.getArgument2Tagged())
print('getArgument2Nouns Example')
print(p.getArgument2Nouns())
# getArgumentTemp Example
print('getArgumentTemp Example')
print(p.getArgumentTemp())
# getArgumentTempTagged Example
print('getArgumentTempTagged Example')
print(p.getArgumentTempTagged())
print('getArgumentTempNouns Example')
print(p.getArgumentTempNouns())
# getArgumentLocation Example
print('getArgumentLocation Example')
print(p.getArgumentLocation())
# getArgumentLocationTagged Example
print('getArgumentLocationTagged Example')
print(p.getArgumentLocationTagged())
print('getArgumentLocationNouns Example')
print(p.getArgumentLocationNouns())
# getPosition Example
print('getPosition Example')
print(p.getPosition())
# getWords Example
print('getWords Example')
print(p.getWords())
# lengthOfPredicate Example
print('lengthOfPredicate Example')
print(p.lengthOfPredicate())
# getPredicateTagged Example
print('getPredicateTagged Example')
print(p.getPredicateTagged())
# getSingularNounsAndMassNouns Example
print('getSingularNounsAndMassNouns Example')
print(p.getSingularNounsAndMassNouns())
# getProperNouns Example
print('getProperNouns Example')
print(p.getProperNouns())
# numberOfProperNouns Example
print('numberOfProperNouns Example')
print(p.numberOfProperNouns())
# getNouns Example
print('getNouns Example')
print(p.getNouns())
# getNounsGivenTaggedContext Example
print('getNounsGivenTaggedContext Example')
print(p.getNounsGivenTaggedContent(p.argument0Tagged))
print(p.getNounsGivenTaggedContent(p.argument1Tagged))
# getNumericalData Example
print('getNumbericalData Example')
print(p.getNumericalData())
# getPredicateAsString Example
print('getPredicateAsString Example')
print(p.getPredicateAsString())
# getPredicateAsStringWithTaggedPOS Example
print('getPredicateAsStringWithTaggedPOS Example')
print(p.getPredicateAsStringWithTaggedPOS())
'''

# References
# [1] Khan, Atif, Naomie Salim, and Yogan Jaya Kumar. "A framework for multi-document abstractive summarization based on semantic role labelling." Applied Soft Computing 30 (2015): 737-747.‏