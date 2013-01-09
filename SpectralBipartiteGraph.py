from BipartiteGraph import *
from MatrixLib import sumRow
from MatrixLib import getDiagonalMatrix
from MatrixLib import powDiagonalMatrix
import numpy as np

"""
Subclass of BipartiteGraph that has methods related
to linear algebra necessary to run the spectral 
algorithm for bipartite clustering
"""
class SpectralBipartiteGraph(BipartiteGraph):
    """
    Constructor uses parent constructor
    """
    def __init__(self):
    	super(SpectralBipartiteGraph, self).__init__()
	self.weightMatrix = None
	
    """
    Records that an ad edge exists from advertiser to keyword
    """
    def add(self, advertiser, kw, position):
	# The adv is in the matrix
	if self.getAdv(advertiser) != None:
	    advertiser = self.getAdv(advertiser)
	    # If we have not recorded this ad before, we add edge from
	    # specific adv to ad and no edge from all other advs to this ad
	    actualKw = self.getKeyword(kw)
	    if actualKw == None:
		self.dict_of_keywords[kw] = [advertiser]
		#self.list_of_keywords.add(kw)
		for adv in self.matrix.keys():
		    self.matrix[adv][kw] = 0

		self.matrix[advertiser][kw] = position

	    # Since we have seen this ad before, just record that there
	    # exists edge from specific adv to ad    
	    else:
		self.matrix[advertiser][actualKw] = position
		self.dict_of_keywords[actualKw].append(advertiser)			

	# The adv is not in the matrix
	else:
	    # If we have not recorded this ad before, we add no edge from
	    # existing advs to this ad and then add the adv to the matrix
	    actualKw = self.getKeyword(kw)
	    if actualKw == None:
		for adv in self.matrix.keys():
		    self.matrix[adv][kw] = 0
		
		#self.list_of_keywords.add(kw)
		self.dict_of_keywords[kw] = [advertiser]

	    # Add adv to matrix - add no edge from this adv to existing ads
	    # and record edge from this adv to given ad
	    self.matrix[advertiser] = {}
	    for old_kw in self.dict_of_keywords.keys():
		self.matrix[advertiser][old_kw] = 0

	    if actualKw == None:
		self.matrix[advertiser][kw] = position
	    else:
		self.matrix[advertiser][actualKw] = position
		self.dict_of_keywords[actualKw].append(advertiser)

    
    """
    Returns edge weight matrix (in numpy format) of 
    the bipartite graph
    """
    def setWeightMatrix(self):
	list_of_rows = []

	# Go through each advertiser and ad 
	# and note '1' if connection exists and '0'
	# otherwise
	#print sorted(self.matrix.keys(), key = lambda adv : adv.advertiser_id)
	for advertiser in sorted(self.matrix.keys(), key = lambda adv : adv.advertiser_id):	
	    row = []
	    for ad in sorted(self.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		if self.matrix[advertiser][ad] >= 1:
		    if ad.keyword_id == '394' and advertiser.advertiser_id == '27961':
			print "w matrix:", self.matrix[advertiser][ad] 
		    row.append(self.matrix[advertiser][ad])
		else:
		    row.append(0)
	    list_of_rows.append(row)

	
	self.weightMatrix = np.array(list_of_rows)

    """
    Compute scaled weight matrix W^
    """
    def getWeightPrimeMatrix(self):
	# compute D_x^(-1/2)    
	D_x = getDiagonalMatrix(self.weightMatrix)
	D_x_powered = powDiagonalMatrix(D_x, -0.5)	

	# compute D_y^(-1/2)
	D_y = getDiagonalMatrix(np.transpose(self.weightMatrix))
	D_y_powered = powDiagonalMatrix(D_y, -0.5)	

	# multiply matrices
	w_prime = np.dot(np.dot(D_x_powered, self.weightMatrix), D_y_powered)
    
	return w_prime

    def getLeftRightSingularVectors(self):
	# perform singular value decomposition
	U, S, V = np.linalg.svd(self.getWeightPrimeMatrix(), full_matrices = True)
	    
	# assume eigenvalues/eigenvectors orderered in dec order left to right
	# 2nd-largest left singular vector (derived from U)
	x = U[:,1]
    	
	# 2nd-largest right singular vector (derived from V)
	y = V[:,1]

	return (x,y)

    """
    Returns two partitions using the spectral method 
    """
    def partition(self):
	print len(self.matrix.keys())
	print self.weightMatrix

	# get singular vectors
	x,y = self.getLeftRightSingularVectors()

	# compute D_x^(-1/2)    
	D_x = getDiagonalMatrix(self.weightMatrix)
    	D_x_powered = powDiagonalMatrix(D_x, -0.5)	
	
	# compute D_y^(-1/2)
	D_y = getDiagonalMatrix(np.transpose(self.weightMatrix))
	D_y_powered = powDiagonalMatrix(D_y, -0.5)	

    	#print "weight_matrix", self.weightMatrix
	#print "D_x", D_x

	x_new = np.dot(D_x_powered, x)
	y_new = np.dot(D_y_powered, y)

	print "x'", x_new
	print "y'", y_new

	A = []
	A_c = []
	B = []
	B_c = []

	c_x = 0.0
    	# Partition advertisements
	index = 0
    	print "c_x", c_x
	for adv in sorted(self.matrix.keys(), key = lambda adv : adv.advertiser_id):
	    if x_new.item(index) >= c_x:
		A.append(adv)
	    else:
		A_c.append(adv)

		if adv.advertiser_id == '27961':
		    print "c_x specific", x_new.item(index)

	    index += 1

	c_y = 0.0
	# Partition ads
	index = 0
	print "c_y", c_y
	for ad in sorted(self.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
	    if y_new.item(index) >= c_y:
		B.append(ad)
	    else:
		B_c.append(ad)

	    if ad.keyword_id == '394':
		print "c_y_specific", y_new.item(index)

	    index += 1

	# Build new partitioned bipartite graphs
	# where G = (A,B) and G_c = (A_c,B_c)
	partition = SpectralBipartiteGraph()
	partition_c = SpectralBipartiteGraph()

	for adv in sorted(A, key = lambda adv : adv.advertiser_id):
	    for ad in sorted(B, key = lambda ad : ad.keyword_id):
		if self.matrix[adv][ad] >= 1:
		    partition.add(adv,ad, self.matrix[adv][ad])

	for adv in sorted(A_c, key = lambda adv : adv.advertiser_id):
	    for ad in sorted(B_c, key = lambda ad : ad.keyword_id):
		if self.matrix[adv][ad] >= 1:
		    partition_c.add(adv, ad, self.matrix[adv][ad])

	# Do check for partitions to ensure no keyword is left out
	for kw in sorted(self.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
	    if partition.getKeyword(kw) == None and partition_c.getKeyword(kw) == None:
		for ad in self.dict_of_keywords[kw]:
		    if partition.getAdv(ad) != None:
			partition.add(ad, kw, self.matrix[ad][kw])
		    else:
			partition_c.add(ad, kw, self.matrix[ad][kw])


	partition.setWeightMatrix()
	partition_c.setWeightMatrix()
	return (partition, partition_c)

    """
    Return average CTR of cluster
    """
    def computeCTR(self):
	total = 0.0
	for kw in self.dict_of_keywords.keys():
	    # If keyword is in training set, and 
	    # CTR value is returned then factor that
	    # into average
	    avg = kw.averageCTR()
	    if avg != None:
		total += avg
	
	return total/len(self.dict_of_keywords.keys())

"""
def score(cluster1, cluster2):
	total_score = 0
	num = 0
	denom = 0
	for advertiser in sorted(cluster1.matrix.keys(), key = lambda adv : adv.advertiser_id):	
    	    for ad in sorted(cluster1.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		num += cluster1.matrix[advertiser][ad]

	print "num", num

	for advertiser in sorted(cluster1.matrix.keys(), key = lambda adv : adv.advertiser_id):	
    	    for ad in sorted(cluster1.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
    		denom += cluster1.matrix[advertiser][ad]
	    for ad in sorted(cluster2.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		denom += cluster1.matrix[advertiser][ad]

	for advertiser in sorted(cluster1.matrix.keys(), key = lambda adv : adv.advertiser_id):	
    	    for ad in sorted(cluster1.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		denom += cluster1.matrix[advertiser][ad]
	for advertiser in sorted(cluster2.matrix.keys(), key = lambda adv : adv.advertiser_id):	
    	    for ad in sorted(cluster1.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		denom += cluster2.matrix[advertiser][ad]

	print num
	total_score += float(num)/float(denom)
	num = 0
	denom = 0

	for advertiser in sorted(cluster2.matrix.keys(), key = lambda adv : adv.advertiser_id):	
    	    for ad in sorted(cluster2.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		num += cluster2.matrix[advertiser][ad]

	for advertiser in sorted(cluster2.matrix.keys(), key = lambda adv : adv.advertiser_id):	
    	    for ad in sorted(cluster1.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		denom += cluster2.matrix[advertiser][ad]
	    for ad in sorted(cluster2.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		denom += cluster2.matrix[advertiser][ad]

	for advertiser in sorted(cluster1.matrix.keys(), key = lambda adv : adv.advertiser_id):	
    	    for ad in sorted(cluster2.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		denom += cluster1.matrix[advertiser][ad]
	for advertiser in sorted(cluster2.matrix.keys(), key = lambda adv : adv.advertiser_id):	
    	    for ad in sorted(cluster2.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
		denom += cluster2.matrix[advertiser][ad]

	
	total_score += float(num)/float(denom)	
	print score, "total_score"	
	return 1.0/total_score
"""



