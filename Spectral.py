from BipartiteGraph import *
import numpy as np

# A cluster, in this spectral instance, is basically
# a sub-bipartite graph of the original bipartite graph 
class Cluster(BipartiteGraph):

    def __init__(self):
	super(BipartiteGraph, self).__init__()

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
Subclass of BipartiteGraph that has methods related
to linear algebra necessary to run the spectral 
algorithm for bipartite clustering
"""
class SpectralBipartiteGraph(BipartiteGraph):
    """
    Constructor uses parent constructor
    """
    def __init__(self):
	super(BipartiteGraph, self).__init__()
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
	for advertiser in self.matrix.keys():	
	    row = []
	    for ad in self.dict_of_keywords:
		if matrix[advertiser][ad] == 1:
		    row.append(1)
		else:
		    row.append(0)
	    list_of_rows.append(row)

	
	self.weightMatrix = np.array(list_of_rows)

    """
    Returns the sum of the row (specified by give index)
    of the given matrix
    """
    def sumRow(self, M, r):
	sum = 0
	for i in range(M.shape[1]):
	    sum += M.item(r, i)

	return sum

    """
    Get diagonal matrix D such that M * e = D * e
    where e is the all-1's vector
    """
    def getDiagonalMatrix(self, M):
	list_of_rows = []
	for i in range(0, M.shape[0]):
	    row = []
	    for j in range(0, M.shape[1]):
		if i == j:
		    row.append(sumRow(M,i))
		else:
		    row.append(0)

	    list_of_rows.append(row)
    
	return np.array(list_of_rows)

    """
    Compute scaled weight matrix W^
    """
    def getWeightPrimeMatrix(self):
	# compute D_x^(-1/2)    
	D_x = self.getDiagonalMatrix(self.weightMatrix)
	D_x_powered = np.linalg.matrix_power(D_x, 0.5)
	
	# compute D_y^(-1/2)
	D_y = self.getDiagonalMatrix(np.transpose(self.weightMatrix))
	D_y_powered = np.linalg.matrix_power(D_y, 0.5)

	# multiply matrices
	return np.dot(np.dot(D_x_powered, self.weightMatrix), D_y_powered)

    def getLeftRightSingularVectors(self):
	# perform singular value decomposition
	U, S, V = np.linalg.svd(self.getWeightPrimeMatrix, full_catrices = True)
	    
	# assume eigenvalues/eigenvectors orderered in dec order left to right
	# 2nd-largest left singular vector (derived from U)
	x = U[:,1]
	
	# 2nd-largest right singular vector (derived from V)
	y = V[:,1]

	return (x,y)

    def getPartition(self):
	# get singular vectors
	x,y = self.getLeftRightSingularVectors()

	# compute D_x^(-1/2)    
	D_x = self.getDiagonalMatrix(self.weightMatrix)
	D_x_powered = np.linalg.matrix_power(D_x, 0.5)
	
	# compute D_y^(-1/2)
	D_y = self.getDiagonalMatrix(np.transpose(self.weightMatrix))
	D_y_powered = np.linalg.matrix_power(D_y, 0.5)

	x_new = np.dot(D_x_powered, x)
	y_new = np.dot(D_y_powered, y)


if __name__ == '__main__':
    # Create biparitite graph from existing Advertisement and Ads 
    (g, list_of_test_sessions) = createGraph()

    

