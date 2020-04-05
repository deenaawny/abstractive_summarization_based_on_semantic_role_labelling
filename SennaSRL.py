# Author: Deena Awny
# Version: 20.03.2020

import annotator as annotator
from practnlptools.tools import Annotator

class SennaSRL:

 annotator= Annotator()
 def getSRL(self, content):
  return self.annotator.getAnnotations(content)['srl']

 def posTagged(self, content):
  return self.annotator.getAnnotations(content)['pos']

 def getNumberOfPredicateArgumentStructures(srl):
  return srl.__len__()

#References
# [1] Khan, Atif, Naomie Salim, and Yogan Jaya Kumar. "A framework for multi-document abstractive summarization based on semantic role labelling." Applied Soft Computing 30 (2015): 737-747.‏
# [2] practNLPTools, computer library, downloaded 20 March 2020,
# <https://pypi.org/project/practnlptools/>.

#shall pronouns be resolved ? -> future implementation