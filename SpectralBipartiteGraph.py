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
	#print "spectral initiating"
	super(SpectralBipartiteGraph, self).__init__()
	self.weightMatrix = None
	
    
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
		if self.matrix[advertiser][ad] == 1:
		    row.append(1)
		else:
		    row.append(0)
	    list_of_rows.append(row)

	
	self.weightMatrix = np.array(list_of_rows)
	#print "weight Matrix", self.weightMatrix

    """
    Compute scaled weight matrix W^
    """
    def getWeightPrimeMatrix(self):
	# compute D_x^(-1/2)    
	D_x = getDiagonalMatrix(self.weightMatrix)
	#D_x_powered = np.linalg.matrix_power(D_x, 0.5)
	#D_x_powered = np.power(D_x, -0.5)
	D_x_powered = powDiagonalMatrix(D_x, -0.5)	

	# compute D_y^(-1/2)
	D_y = getDiagonalMatrix(np.transpose(self.weightMatrix))
	#D_y_powered = np.linalg.matrix_power(D_y, 0.5)
	#D_y_powered = np.power(D_y, -0.5)
	D_y_powered = powDiagonalMatrix(D_y, -0.5)	

	# multiply matrices
	w_prime = np.dot(np.dot(D_x_powered, self.weightMatrix), D_y_powered)
	#print "weight Matrix Prime", w_prime
    
	return w_prime

    def getLeftRightSingularVectors(self):
	# perform singular value decomposition
	U, S, V = np.linalg.svd(self.getWeightPrimeMatrix(), full_matrices = True)
	    
	# assume eigenvalues/eigenvectors orderered in dec order left to right
	# 2nd-largest left singular vector (derived from U)
	
	#print "S"
	#print S
	#print "U"
	#print U
	x = U[:,1]
	#print "x"
	#print x
	
	# 2nd-largest right singular vector (derived from V)
	#print "V"
	#print V
	y = V[:,1]

	return (x,y)

    """
    Returns two partitions using the spectral method 
    """
    def partition(self):
	# get singular vectors
	x,y = self.getLeftRightSingularVectors()

	# compute D_x^(-1/2)    
	D_x = getDiagonalMatrix(self.weightMatrix)
	#D_x_powered = np.linalg.matrix_power(D_x, 0.5)
	#D_x_powered = np.power(D_x, -0.5)
	D_x_powered = powDiagonalMatrix(D_x, -0.5)	
	
	# compute D_y^(-1/2)
	D_y = getDiagonalMatrix(np.transpose(self.weightMatrix))
	#D_y_powered = np.linalg.matrix_power(D_y, 0.5)
	#D_y_powered = np.power(D_y, -0.5)
	D_y_powered = powDiagonalMatrix(D_y, -0.5)	


	x_new = np.dot(D_x_powered, x)
	y_new = np.dot(D_y_powered, y)

	A = []
	A_c = []
	B = []
	B_c = []

	# Partition advertisements
	index = 0
	c_x = 0.0
	#print "y"
	#print y
	#print "y_new"
	#print y_new
	for adv in sorted(self.matrix.keys(), key = lambda adv : adv.advertiser_id):
	    if x_new.item(index) >= c_x:
		A.append(adv)
	    else:
		A_c.append(adv)

	    index += 1

	# Partition ads
	index = 0
	c_y = 0.0
	for ad in sorted(self.dict_of_keywords.keys(), key = lambda ad : ad.keyword_id):
	    if y_new.item(index) >= c_y:
		B.append(ad)
	    else:
		B_c.append(ad)

	    index += 1

	# Build new partitioned bipartite graphs
	# where G = (A,B) and G_c = (A_c,B_c)

	partition = SpectralBipartiteGraph()
	partition_c = SpectralBipartiteGraph()

	#print "A", len(A)
	#print "Ac", len(A_c)
	#print "B", len(B)
	#print "Bc", len(B_c)

	for adv in A:
	    for ad in B:
		if self.matrix[adv][ad] == 1:
		    partition.add(adv,ad)

	for adv in A_c:
	    for ad in B_c:
		if self.matrix[adv][ad] == 1:
		    partition_c.add(adv, ad)

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


