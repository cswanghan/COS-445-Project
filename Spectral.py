from BipartiteGraph import *
from SpectralBipartiteGraph import *
from MatrixLib import sumRow
from MatrixLib import getDiagonalMatrix
from createGraph import createGraph
from MeanSquaredError import evaluator
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

def produceClusters(spectralGraph):
    # produce two clusters
    cluster1, cluster2 = spectralGraph.partition()

    print "cluster1_len", len(cluster1.matrix.keys())
    print "cluster2_len", len(cluster2.matrix.keys())


   
    # recursively produce more clusters from these two if 
    # their size is big enough
    if (len(cluster1.matrix.keys()) < 2 or len(cluster2.matrix.keys()) < 2):
	return spectralGraph
    else:
    	l = []
	list_1 = produceClusters(cluster1)
	list_2 = produceClusters(cluster2)

	if isinstance(list_1, list):
	    for cluster in list_1:
		l.append(cluster)
	else:
	    l.append(list_1)
	
	if isinstance(list_2, list):
	    for cluster in list_2:
		l.append(cluster)
	else:
	    l.append(list_2)

	return l

if __name__ == '__main__':
    # Create SPECTRAL biparitite graph from existing Advertisement and Keywords 
    (spectralG, list_of_test_sessions) = createGraph(True)
    spectralG.setWeightMatrix()

    #cluster1, cluster2 = spectralG.partition()
    list_of_clusters = produceClusters(spectralG)

    # print number of clusters
    print "Number of clusters:", len(list_of_clusters)

    # map each test session to its keyword
    list_test_keywords = map(lambda x : Keyword(x.keyword_id), list_of_test_sessions)

    # compute predictions for CTR
    list_CTR_predictions = []
    count = 0
    for kw in list_test_keywords:
	print kw
	for cluster in list_of_clusters:
	    if cluster.getKeyword(kw) != None:
		print "FOUND"
		list_CTR_predictions.append(cluster.computeCTR())
		count += 1
		break
    
    print "found_ratio", count/float(len(list_test_keywords))
    # Compute Mean Squared Error for predictions
    m_s_e = evaluator(list_CTR_predictions)
    print m_s_e


    
    
    
    

