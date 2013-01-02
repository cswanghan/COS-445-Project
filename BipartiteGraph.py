from Advertiser import *
#from Ad import *
from Keyword import *
import math

class BipartiteGraph(object):
    def __init__(self):
	# Maintains which advertiser is connected to which keyword
	self.matrix = {}
	self.dict_of_keywords = {}

    """
    Returns the number of total advertisers that 
    bid for this specific ad
    """
    def numberOfAdvertisersForKeyword(self, kw):
	return len(self.dict_of_keywords[kw])
	
	"""
	kw = self.getKeyword(kw)
	count = 0

	if kw == None:
	    count = 0
	else:
	    count = 0
	    for adv in self.matrix.keys():
		if self.matrix[adv][kw] == 1:	
		    count += 1	

	return count
	"""

    """
    Returns the number of total advertisers that 
    bid for both specific ads
    """
    def numberOfAdvertisersForTwoKeywords(self, kw1, kw2):
	interSet = set(self.dict_of_keywords[kw1]).intersection( set(self.dict_of_keywords[kw2] ))
	if interSet == None:
	    return 0
	else:
	    return len(interSet)

	"""
	kw1 = self.getKeyword(kw1)
	kw2 = self.getKeyword(kw2)
	count = 0

	if kw1 == None or kw2 == None:
	    count = 0
	else:
	    count = 0
	    for adv in self.matrix.keys():
		if self.matrix[adv][kw1] == 1 and self.matrix[adv][kw2] == 1:	
		    count += 1	

	return count
	"""

	
    """
    Get the corresponding advertiser (if it exists) in the bipartite graph
    """
    def getAdv(self, adv):
	existingAdv = None
	for a in self.matrix.keys():
	    if a == adv:
		existingAdv = a
		break

	return existingAdv

    """
    Get the corresponding ad (if it exists) in the bipartite graph
    """
    def getKeyword(self, kw):
	existingKw = None
	for k in self.dict_of_keywords.keys():
	    if k == kw:
		existingKw = k
		break
	
	return existingKw

    """
    Records that an ad edge exists from advertiser to keyword
    """
    def add(self, advertiser, kw):
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

		self.matrix[advertiser][kw] = 1

	    # Since we have seen this ad before, just record that there
	    # exists edge from specific adv to ad    
	    else:
		self.matrix[advertiser][actualKw] = 1
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
		self.matrix[advertiser][kw] = 1
	    else:
		self.matrix[advertiser][actualKw] = 1
		self.dict_of_keywords[actualKw].append(advertiser)

    def getKeywords(self, advertiser):
	string = repr(advertiser) + " => "
	for kw in self.matrix[advertiser].keys():
	    if self.matrix[advertiser][kw] == 1:
		string += repr(kw) + ", "

	string += "\n"
	return string

    """
    def getAds(self,advertiser):
	l = []
	for ad in self.matrix[advertiser].keys():
	    if self.matrix[advertiser][ad] == 1:
		l.append(ad)
	return l
    """

    def __repr__(self):
	string = ""
	for adv in self.matrix.keys():
	    string += self.getKeywords(adv)
	
	return string

	"""
	string = ""
	for adv in self.matrix.keys():
	    if adv.advertiser_id == '385':
		print 'hello'
	    l = self.getAds(adv)
	    if len(l) > 1:
		string += repr(adv) + "\n"

	return string
	"""
