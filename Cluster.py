# Author: Deena Awny
# Version: 20.03.2020

class Cluster:

 def __init__(self, name, predicates, avergaelinkages):
     self.name= name
     self.predicates= predicates
     self.averagelinkages= avergaelinkages

 def getPredicates(self):
  return self.predicates

 def getAverageLinkages(self):
   return self.averagelinkages

# References
# [1] Khan, Atif, Naomie Salim, and Yogan Jaya Kumar. "A framework for multi-document abstractive summarization based on semantic role labelling." Applied Soft Computing 30 (2015): 737-747.‏