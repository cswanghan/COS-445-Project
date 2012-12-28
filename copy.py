import os

"""
Since training set is too large, copy N
lines of it to new training set
"""

N = 100000
originalFile = 'training.txt'
newFile = "training" + str(N) + ".txt"


files = os.listdir('.')
if originalFile in files:

    read = open(originalFile, 'r')

    lines = [read.readline() for x in xrange(N)]	 

    write = open(newFile, 'w')
    for line in lines:
	write.write(line)
   
