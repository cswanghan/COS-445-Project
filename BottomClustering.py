from BipartiteGraph import *
from createGraph import createGraph
from MeanSquaredError import evaluator

class Node:
    def __init__(self, kw):
	self.kw = kw
	self.adj_list = []

    def add(self, n, weight):
	self.adj_list.append((n, weight))

    def __eq__(self, other):
	return (self.kw == other.kw)

    def __repr__(self):
	return repr(self.kw)

    def __hash__(self):
	return hash(self.kw)

class Cluster:
    def __init__(self, node):
	self.node_list = [node]

    def isSingleton(self):
	return (len(self.node_list) == 1)
    
    def hasNode(self, n):
	for n_ext in self.node_list:
	    if n_ext == n:
		return True

	return False

    def merge(self, c):
	for node in c.node_list:
	    self.node_list.append(node)
	
    def __repr__(self):
	string = ""
	for node in self.node_list:
	    string += repr(node) + "\n"
	
	string += "--------------------"
	    
	return string

    def __eq__(self, other):
	return (self.node_list == other.node_list)

    """
    Return average CTR of cluster
    """
    def computeCTR(self):
	total = 0.0
	for node in self.node_list:
	    # If keyword is in training set, and 
	    # CTR value is returned then factor that
	    # into average
	    avg = node.kw.averageCTR()
	    if avg != None:
		total += avg
	
	return total/len(self.node_list)

    
class Graph(object):
    def __init__(self):
	self.node_list = []

    def findNode(self, kw):
	for node in self.node_list:
	    if node.kw == kw:
		return node
	    
	return None

    """
    Defines a similarity score for two ads - is 
    based on the linear coefficient of the two
    """
    def similarityScore(self, kw1, kw2, g):
	# total number of advertisers in the market
	total_advs = len(g.matrix.keys())
    
	# total number of advertisers that bid for ad1 and ad2
	num_kw1 = g.numberOfAdvertisersForKeyword(kw1)
	num_kw2 = g.numberOfAdvertisersForKeyword(kw2)
	
	# total number of advertisers that bid for both
	num_both = g.numberOfAdvertisersForTwoKeywords(kw1, kw2)
	    
	# return similarity score
	return (total_advs * num_both - num_kw1 * num_kw2) / math.sqrt(num_kw1 * num_kw2 * (total_advs - num_kw1) * (total_advs - num_kw2))

    """
    Convert bipartite graph containing sets of Advertisers
    and Ads to direct graph of Ads according to 
    similarity function of Ads
    """
    def bipartiteConversion(self, g):
	# Create empty Nodes corresponding to ads 
	for kw in g.dict_of_keywords.keys():
	    node = Node(kw)
	    self.node_list.append(node)
	
	# For each node, connect to every other node with 
	# edge weight being equal to similarity score of two nodes
	for node1 in self.node_list:	    
	    for node2 in self.node_list:
		if node1 != node2:
		    #print self.similarityScore(node1.kw, node2.kw, g)
		    node1.add(node2, self.similarityScore(node1.kw, node2.kw, g))

    """
    Get sorted list of edges (where weight is in dec. order)
    """
    def sortedListOfEdges(self):
	edge_list = []
	
	# Add all edges to list 
	for node in self.node_list:
	    for (nbhr, w) in node.adj_list:
		edge_list.append((node, nbhr, w))

	# Sort list using edge weight as key and return in reverse of asc. order
	return sorted(edge_list, key = lambda edge : edge[2], reverse=True)
	    
	
if __name__ == '__main__':
    # Create biparitite graph from existing Advertisement and Keywords
    (g, list_of_test_sessions) = createGraph()
			
    # Convert bipartite graph to directed graph using similarity function
    # of ads
    g_new = Graph()
    g_new.bipartiteConversion(g)

    # Get list of sorted edges by weight
    sorted_edge_list = g_new.sortedListOfEdges()

    # create list of singleton clusters
    cluster_list = [] 
    node_cluster_dict = {}
    for node in g_new.node_list:
	cluster = Cluster(node)
	node_cluster_dict[node] = cluster
	cluster_list.append(cluster)

    # run linkage algorithm to finalize clusters

    for (node1, node2, w) in sorted_edge_list:
	
	firstCluster = node_cluster_dict[node1]
	secondCluster = node_cluster_dict[node2]

	# Rules for clusters
	if firstCluster == secondCluster:
	    continue

	elif firstCluster.isSingleton() == True or secondCluster.isSingleton() == True:
	    firstCluster.merge(secondCluster)

	    # update every node in cluster
	    for node in secondCluster.node_list:
		node_cluster_dict[node] = firstCluster

	    # remove the cluster we merged in
	    cluster_list.remove(secondCluster)	

	else:
	    continue

    # Compute predictions for keywords in test set 
    list_test_keywords = map(lambda x : Keyword(x.keyword_id), list_of_test_sessions)
    list_CTR_predictions = []
    for kw in list_test_keywords:
	corresponding_cluster = node_cluster_dict[g_new.findNode(kw)]
	list_CTR_predictions.append(corresponding_cluster.computeCTR())

    # Compute Mean Squared Error for predictions
    m_s_e = evaluator(list_CTR_predictions)
    print m_s_e
	
