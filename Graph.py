from Advertiser import *
from Ad import *

class Graph(object):
    def __init__(self):
	self.matrix = {}
	self.list_of_ads = []

    def getAdv(self, adv):
	existingAdv = None
	for a in self.matrix.keys():
	    if a == adv:
		existingAdv = a
		break

	return existingAdv

    def getAd(self, ad):
	existingAd = None
	for a in self.list_of_ads:
	    if a == ad:
		existingAd = a
		break
	
	return existingAd

    """
    Records that an ad edge exists from advertisder to ed
    """
    def add(self, advertiser, ad):
	# The adv is in the matrix
	if self.getAdv(advertiser) != None:
	    advertiser = self.getAdv(advertiser)
	    # If we have not recorded this ad before, we add edge from
	    # specific adv to ad and no edge from all other advs to this ad
	    if self.getAd(ad) == None:
		self.list_of_ads.append(ad)
		for adv in self.matrix.keys():
		    self.matrix[adv][ad] = 0

		self.matrix[advertiser][ad] = 1

	    # Since we have seen this ad before, just record that there
	    # exists edge from specific adv to ad    
	    else:
		self.matrix[advertiser][ad] = 1			

	# The adv is not in the matrix
	else:
	    # If we have not recorded this ad before, we add no edge from
	    # existing advs to this ad and then add the adv to the matrix
	    if self.getAd(ad) == None:
		for adv in self.matrix.keys():
		    self.matrix[adv][ad] = 0
		
		self.list_of_ads.append(ad)

	    # Add adv to matrix - add no edge from this adv to existing ads
	    # and record edge from this adv to given ad
	    self.matrix[advertiser] = {}
	    for old_ad in self.list_of_ads:
		self.matrix[advertiser][old_ad] = 0

	    self.matrix[advertiser][ad] = 1

    def getAds(self, advertiser):
	string = repr(advertiser) + " => "
	for ad in self.matrix[advertiser].keys():
	    if self.matrix[advertiser][ad] == 1:
		string += repr(ad) + ", "

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
	    string += self.getAds(adv)
	
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
