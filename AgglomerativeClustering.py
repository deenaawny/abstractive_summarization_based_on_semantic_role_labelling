# Author: Deena Awny
# Version: 20.03.2020
from Cluster import Cluster

# [1] Semantic clustering of predicate argument structures
# Agglomerative hierarchical clustering is a well-known method in the hierarchical clustering method, which is quite old but has been found
# useful in the range of applications [2]. There are five well-known linkage methods of agglomerative hierarchical clustering (HAC) i.e. single linkage,
# complete linkage, average linkage, word and centroid method.
# Based on different meausres (Entropuy and F-score and Kendall W Test), it was found from the literature studies in [3-5] that average linkage is the most suitable
# method for document clustering. Therefore this study exploits HAC algorithm based on average linkage method. This phase takes semantic similarity matrix as input
# from previous phase in which the value at position (i,j) is the semantic similarity between ith and jth predicate argument structures. We consider the value at
# position (i,j) ith and jth clusters, assuming that the construction of similarity matrix begins with each predicate argument structure as a single cluster.
# The psuedo code for clustering similar predicate argument structures is given below

# Pseudo code for agglomerative clustering algorithms
# Input: Semantic Similarity Matrix
# Output: Clusters of similar predicate argument structures
# a. Merge the two clusters that are more similar
# b. Update the semantic similarity matric to represent the pair wise similarity
# between the newest cluster and the original cluster based on average linkage method.
# c. Repeat step 1 and 2 until the compression rate of summary is reached.

# averge linkage method:
# average-linkage is where the distance between each pair of observations, in each cluster is added up and divided by the number of pairs
# to get an average inter-clustering distance.

# average linkage clustering - the distance between two clusters is defined as the average distance between all pairs of objects, where each pair is made up
# of one object from each group.

class AgglomerativeClustering:

 def __init__(self, clusters):
    self.clusters= clusters

 # returns the number of clusters
 def numberOfClusters(self):
   return len(self.clusters)

 # merges two clusters given cluster1 and cluster2
 def mergeTwoClusters(self, cluster1, cluster2):
  newname = cluster1.name + cluster2.name
  c = Cluster(newname,[],[])
  self.clusters.remove(cluster1)
  self.clusters.remove(cluster2)

  newpredicates = []
  if isinstance(cluster1.predicates,list):
    for predicate in cluster1.predicates:
      newpredicates.append(predicate)
  else:
   newpredicates.append(cluster1.predicates)

  if isinstance(cluster2.predicates,list):
    for predicate in cluster2.predicates:
      newpredicates.append(predicate)
  else:
    newpredicates.append(cluster2.predicates)
  c.predicates = newpredicates

  newAverageLinkages = []
  for a1 in cluster1.averagelinkages:
    for a2 in cluster2.averagelinkages:
      if a1[0] == a2[0]:
        newAverageLinkages.append((a1[0],(a1[1]+a2[1])/2))
  c.averagelinkages = newAverageLinkages

  for cluster in self.clusters:
    newavgl = []
    for a in cluster.averagelinkages:
      if a[0] == cluster1:
        for x, y in c.averagelinkages:
          if x == cluster :
            newavgl.append((c,y))
      elif a[0] != cluster2 and a[0] != cluster1:
        newavgl.append(a)
    cluster.averagelinkages = newavgl
  self.clusters.append(c)
  return c

 # from the clusters, picks the two clusters to merge based on average linkage method
 def pickTwoClustersToMerge(self):
  maximum = self.clusters[0].averagelinkages[0][1]
  cluster1 = self.clusters[0]
  cluster2 = self.clusters[0].averagelinkages[0][0]
  for c in self.clusters:
    for averagelinkage in c.averagelinkages:
      if averagelinkage[1] > maximum:
       maximum = averagelinkage[1]
       cluster1= c
       cluster2 = averagelinkage[0]
  return (cluster1,cluster2)

 # applies agglomerative hierarchical clustering until the compression rate of summary is 20%
 # changed to numberOfExpectedClusters to 4
 def twentyPercentCompression(self):
   initialSize = self.numberOfClusters()
   numberOfExpectedClusters = 4
   while self.numberOfClusters()> numberOfExpectedClusters:
     twoClustersToMerge = self.pickTwoClustersToMerge()
     print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
     self.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1])

'''
 print("----------Agglomerative Clustering Tests----------")

 print("----------Example 1 - Cluster containing One Cluster----------")
e1 = AgglomerativeClustering([])
p1 = Cluster("p1",[],[])
p1.averagelinkages = []
e1.clusters.append(p1)
# In this case of clusters with one cluster - cannot pick two clusters to merge or merge two clusters
print("----------Example 2 - Cluster containing Two Clusters----------")
e2 = AgglomerativeClustering([])
p1 = Cluster("p1",[],[])
p2 = Cluster("p2",[],[])
p1.averagelinkages = [(p2,0.6)]
p2.averagelinkages = [(p1,0.6)]
e2.clusters.append(p1)
e2.clusters.append(p2)
print("Two clusters to merge")
twoClustersToMerge = e2.pickTwoClustersToMerge()
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
newcluster = e2.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1])
print(newcluster.name)
print(newcluster)

print("----------Example 3 - Cluster containing Three Clusters----------")
e3= AgglomerativeClustering([])
p1 = Cluster("p1",[],[])
p2 = Cluster("p2",[],[])
p3 = Cluster("p3",[],[])
p1.averagelinkages = [(p2,0.8),(p3,0.7)]
p2.averagelinkages = [(p1,0.8),(p3,0.3)]
p3.averagelinkages = [(p1,0.7),(p2,0.3)]
e3.clusters.append(p1)
e3.clusters.append(p2)
e3.clusters.append(p3)
print("Two clusters to merge")
twoClustersToMerge = e3.pickTwoClustersToMerge()
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
print(e3.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1]))
#print cluster average linkages
for c in e3.clusters:
  print("Average linkages")
  print(c.averagelinkages)
print("length of clusters")
print(len(e3.clusters))

print("----------Example 4 - Cluster containing Four Clusters----------")
e4= AgglomerativeClustering([])
p1 = Cluster("p1",[],[])
p2 = Cluster("p2",[],[])
p3 = Cluster("p3",[],[])
p4 = Cluster("p4",[],[])
p1.averagelinkages = [(p2,0.8),(p3,0.7),(p4,0.5)]
p2.averagelinkages = [(p1,0.8),(p3,0.3),(p4,0.3)]
p3.averagelinkages = [(p1,0.7),(p2,0.3),(p4,0.2)]
p4.averagelinkages = [(p1,0.5),(p2,0.3),(p3,0.2)]
e4.clusters.append(p1)
e4.clusters.append(p2)
e4.clusters.append(p3)
e4.clusters.append(p4)
print("Two clusters to merge")
twoClustersToMerge = e4.pickTwoClustersToMerge()
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
print(e4.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1]))
#print cluster average linkages
for c in e4.clusters:
  print(c.name)
  print("Average linkages")
  print(c.averagelinkages)
print("length of clusters")
print(len(e4.clusters))

print("Two clusters to merge (Second Round)")
twoClustersToMerge = e4.pickTwoClustersToMerge()
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
print(e4.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1]))
#print cluster average linkages
for c in e4.clusters:
  print(c.name)
  print("Average linkages")
  print(c.averagelinkages)
print("length of clusters")
print(len(e4.clusters))

print("----------Example 5 - Cluster containing Five Clusters----------")
e5= AgglomerativeClustering([])
p1 = Cluster("p1",[],[])
p2 = Cluster("p2",[],[])
p3 = Cluster("p3",[],[])
p4 = Cluster("p4",[],[])
p5 = Cluster("p5",[],[])
p1.averagelinkages = [(p2,0.8),(p3,0.7),(p4,0.5),(p5,0.1)]
p2.averagelinkages = [(p1,0.8),(p3,0.3),(p4,0.3),(p5,0.8)]
p3.averagelinkages = [(p1,0.7),(p2,0.3),(p4,0.2),(p5,0.6)]
p4.averagelinkages = [(p1,0.5),(p2,0.3),(p3,0.2),(p5,0.5)]
p5.averagelinkages = [(p1,0.1),(p2,0.8),(p3,0.6),(p4,0.5)]
e5.clusters.append(p1)
e5.clusters.append(p2)
e5.clusters.append(p3)
e5.clusters.append(p4)
e5.clusters.append(p5)
print("Two clusters to merge")
twoClustersToMerge = e5.pickTwoClustersToMerge()
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
print(e5.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1]))
#print cluster average linkages
for c in e5.clusters:
  print(c.name)
  print("Average linkages")
  print(c.averagelinkages)

print("Two clusters to merge (Second Round)")
twoClustersToMerge = e5.pickTwoClustersToMerge()
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
print(e5.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1]))
#print cluster average linkages
for c in e5.clusters:
  print(c.name)
  print("Average linkages")
  print(c.averagelinkages)

print("Two clusters to merge (Third Round)")
twoClustersToMerge = e5.pickTwoClustersToMerge()
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
print(e5.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1]))
#print cluster average linkages
for c in e5.clusters:
  print(c.name)
  print("Average linkages")
  print(c.averagelinkages)

print("Two clusters to merge (Fourth Round)")
twoClustersToMerge = e5.pickTwoClustersToMerge()
print(twoClustersToMerge[0].name, twoClustersToMerge[1].name)
print(e5.mergeTwoClusters(twoClustersToMerge[0],twoClustersToMerge[1]))
#print cluster average linkages
for c in e5.clusters:
  print(c.name)
  print("Average linkages")
  print(c.averagelinkages)

print("----------Example 5 - Cluster containing Five Clusters Using 20% Compression Function----------")
e5= AgglomerativeClustering([])
p1 = Cluster("p1",[],[])
p2 = Cluster("p2",[],[])
p3 = Cluster("p3",[],[])
p4 = Cluster("p4",[],[])
p5 = Cluster("p5",[],[])
p1.averagelinkages = [(p2,0.8),(p3,0.7),(p4,0.5),(p5,0.1)]
p2.averagelinkages = [(p1,0.8),(p3,0.3),(p4,0.3),(p5,0.8)]
p3.averagelinkages = [(p1,0.7),(p2,0.3),(p4,0.2),(p5,0.6)]
p4.averagelinkages = [(p1,0.5),(p2,0.3),(p3,0.2),(p5,0.5)]
p5.averagelinkages = [(p1,0.1),(p2,0.8),(p3,0.6),(p4,0.5)]
e5.clusters.append(p1)
e5.clusters.append(p2)
e5.clusters.append(p3)
e5.clusters.append(p4)
e5.clusters.append(p5)
e5.twentyPercentCompression()
for c in e5.clusters:
  print(c.name)
  print("Average linkages")
  print(c.averagelinkages)
'''

# References
# [1] Khan, Atif, Naomie Salim, and Yogan Jaya Kumar. "A framework for multi-document abstractive summarization based on semantic role labelling." Applied Soft Computing 30 (2015): 737-747.‏
# [2] Murtagh, Fionn, and Pedro Contreras. "Methods of hierarchical clustering." arXiv preprint arXiv:1105.0121 (2011).‏
# [3] Karypis, Michael Steinbach George, Vipin Kumar, and Michael Steinbach. "A comparison of document clustering techniques." TextMining Workshop at KDD2000 (May 2000). 2000.‏
# [4] Zhao, Ying, George Karypis, and Usama Fayyad. "Hierarchical clustering algorithms for document datasets." Data mining and knowledge discovery 10.2 (2005): 141-168.‏
# [5] El-Hamdouchi, Abdelmoula, and Peter Willett. "Comparison of hierarchic agglomerative clustering methods for document retrieval." The Computer Journal 32.3 (1989): 220-227.‏