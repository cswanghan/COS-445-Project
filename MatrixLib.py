import numpy as np
from math import pow

"""
Returns the sum of the row (specified by give index)
of the given matrix
"""
def sumRow(M, r):
    sum = 0
    for i in range(M.shape[1]):
      	sum += M.item(r, i)

    return sum

"""
Get diagonal SQUARE matrix D such that M * e = D * e
where e is the all-1's vector
"""
def getDiagonalMatrix(M):
    list_of_rows = []
    for i in range(0, M.shape[0]):
    	row = []
    	for j in range(0, M.shape[0]):
    	    if i == j:
    		row.append(sumRow(M,i))
    	    else:
    		row.append(0)

	list_of_rows.append(row)
    
    return np.array(list_of_rows)

"""
Power diagonal values to given power - 
done by just powering values in the diagonal
spot in the matrix
"""
def powDiagonalMatrix(M, power):
    list_of_rows = []
    for i in range(0, M.shape[0]):
	row = []
	for j in range(0, M.shape[0]):
	    if i == j:
		row.append(pow(M.item(i,j), power))
	    else:
		row.append(0)
	
	list_of_rows.append(row)
    
    return np.array(list_of_rows)
    
