from BipartiteGraph import *
from SpectralBipartiteGraph import *
from MatrixLib import sumRow
from MatrixLib import getDiagonalMatrix
from createGraph import createGraph
import numpy as np

# A cluster, in this spectral instance, is basically
# a sub-bipartite graph of the original bipartite graph 
class Cluster(SpectralBipartiteGraph):

    def __init__(self):
	super(BipartiteGraph, self).__init__()

    """
    Return average CTR of cluster
    """
    def computeCTR(self):
	total = 0.0
	for kw in list_of_kws:
	    # If keyword is in training set, and 
	    # CTR value is returned then factor that
	    # into average
	    avg = kw.averageCTR()
	    if avg != None:
		total += avg
	
	return total/len(self.dict_of_keywords.keys())


if __name__ == '__main__':
    # Create SPECTRAL biparitite graph from existing Advertisement and Keywords 
    (spectralG, list_of_test_sessions) = createGraph(True)
    spectralG.setWeightMatrix()

    cluster1, cluster2 = spectralG.partition()

    print "----CLUSTER 1----"
    print repr(cluster1)
    print "----CLUSTER 2----"
    print repr(cluster2)
    
    
    

