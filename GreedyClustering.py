from BottomClustering import *

node_cluster_dict = {}

def recursiveCluster(cluster, g, g_new):
    # Get two random nodes with weak links between them
    similarityScore = 1.0
    node1 = None
    node2 = None
    maxIter = 4.75 * len(cluster.node_list)
    count = 0
    while (similarityScore > -0.002):
	node1 = cluster.getRandomNode()
	node2 = cluster.getRandomNode()

	
	if node1.kw != node2.kw:
	    similarityScore = g_new.similarityScore(node1.kw, node2.kw, g)
    
	count += 1

	if (count > maxIter):
	    return cluster


    cluster1 = Cluster(node1)
    cluster2 = Cluster(node2)
    node_cluster_dict[node1] = cluster1
    node_cluster_dict[node2] = cluster2

    # add each node to the cluster in which there is the least cut value
    count = 0
    for node in cluster.node_list:
	if (node.kw != node1. kw and node.kw != node2.kw):
	    cutvalue2 = cluster1.cut(node, g, g_new)
	    cutvalue1 = cluster2.cut(node, g, g_new)
	    
	    """
	    if count == 0:
		print "node1 kw", node1.kw
		print "node2 kw", node2.kw
		print "node kw", node.kw
		print "cut value 2", cutvalue2
		print "cut value 1", cutvalue1
	    """

	    if (cutvalue1 > cutvalue2):
		cluster2.node_list.append(node)
		node_cluster_dict[node] = cluster2
	    else:
		cluster1.node_list.append(node)
		node_cluster_dict[node] = cluster1

	    count += 1

    print "cluster 1 len:", len(cluster1.node_list)
    print "cluster 2 len:", len(cluster2.node_list)

    # recursively produce more clusters from these two if 
    # their size is big enough
    if (len(cluster1.node_list) < 2 or len(cluster2.node_list) < 2):
	return cluster
    else:
    	l = []
	list_1 = recursiveCluster(cluster1, g, g_new)
	list_2 = recursiveCluster(cluster2, g, g_new)

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
    # Create biparitite graph from existing Advertisement and Keywords
    (g, list_of_test_sessions) = createGraph()
			
    # Convert bipartite graph to directed graph using similarity function
    # of ads
    g_new = Graph()
    g_new.bipartiteConversion(g)

    """
    similarityScore = 1.0
    node1 = None
    node2 = None
    while (similarityScore > -0.003):
	node1 = g_new.getRandomNode()
	node2 = g_new.getRandomNode()
	similarityScore = g_new.similarityScore(node1.kw, node2.kw, g)
	print similarityScore

    
    cluster1 = Cluster(node1)
    cluster2 = Cluster(node2)
    for node in g_new.node_list:
	if (node.kw != node1. kw and node.kw != node2.kw):
	    cutvalue1 = cluster1.cut(node, g, g_new)
	    cutvalue2 = cluster2.cut(node, g, g_new)

	    if (cutvalue1 < cutvalue2):
		cluster2.node_list.append(node)
	    else:
		cluster1.node_list.append(node)
    """

    c = Cluster(None)
    for node in g_new.node_list:
	c.node_list.append(node)
    cluster_list = recursiveCluster(c, g, g_new)
    
    print cluster_list 
    print len(cluster_list)

    # Compute predictions for keywords in test set 
    list_test_keywords = map(lambda x : Keyword(x.keyword_id), list_of_test_sessions)
    list_CTR_predictions = []
    #list_CTR_weighted_predictions = []
    for kw in list_test_keywords:
	node = g_new.findNode(kw)
	corresponding_cluster = node_cluster_dict[node]
	list_CTR_predictions.append(corresponding_cluster.computeCTR())
	#list_CTR_weighted_predictions.append(corresponding_cluster.weightedCTR(node, g, g_new))


    # Compute Mean Squared Error for predictions
    m_s_e = evaluator(list_CTR_predictions)
    print m_s_e
	
    # Compute Mean Squared Error for predictions
    #m_s_e = evaluator(list_CTR_weighted_predictions)
    #print m_s_e

