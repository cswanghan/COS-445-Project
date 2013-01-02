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
    cluster1, cluster2 = spectralGraph.partition()

    print "c1", len(cluster1.matrix.keys())
    print "c2", len(cluster2.matrix.keys())
    #print "----CLUSTER 1----"
    #print repr(cluster1)
    #print "----CLUSTER 2----"
    #print repr(cluster2)

    if (len(cluster1.matrix.keys()) < 2 or len(cluster2.matrix.keys()) < 2):
	return spectralGraph
    else:
	print "recursing"
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

    #print list_of_clusters

    #for cluster in list_of_clusters:
	#print repr(cluster)

    #print len(list_of_clusters)

    #print "c1", len(cluster1.matrix.keys())
    #print "c2", len(cluster2.matrix.keys())
    #print "----CLUSTER 1----"
    #print repr(cluster1)
    #print "----CLUSTER 2----"
    #print repr(cluster2)

    # map each test session to its keyword
    list_test_keywords = map(lambda x : Keyword(x.keyword_id), list_of_test_sessions)

    # compute predictions for CTR
    list_CTR_predictions = []
    for kw in list_test_keywords:
	for cluster in list_of_clusters:
	    if cluster.getKeyword(kw) != None:
		list_CTR_predictions.append(cluster.computeCTR())
		break
    
    
    # Compute Mean Squared Error for predictions
    m_s_e = evaluator(list_CTR_predictions)
    print m_s_e


    
    
    
    

