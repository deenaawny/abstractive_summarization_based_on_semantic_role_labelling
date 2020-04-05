# Author: Deena Awny
# Version: 26.03.2020

import glob
class DocumentCollection:

  def __init__(self, documents):
    self.documents = documents

  def setDocuments(self, documents):
    self.documents

  def getDocuments(self, documents):
    self.documents

  def totalNumberOfDocuments(self):
    return len(self.documents)

  def getFilePaths(directoryname):
    return glob.glob(directoryname)

'''
print("Document Collection Example")
dc = DocumentCollection
files = dc.getFilePaths("C:/Users/admin/Documents/7lytixTest/dailymail_stories/dailymail/stories/*.story")
print("file 1")
print(files[0])
print("file 2")
print(files[1])
print("file 3")
print(files[2])
'''
