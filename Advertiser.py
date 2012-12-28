
class Advertiser(object):
    def __init__(self, advertiser_id):
	self.advertiser_id = advertiser_id

    def __eq__(self, other):
	if other == None:
	    return False
	else:
	    return self.advertiser_id == other.advertiser_id

    def __repr__(self):
	return "<Advertiser('%s')>" % (self.advertiser_id)

