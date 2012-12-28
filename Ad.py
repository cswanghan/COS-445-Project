
class Ad(object):
    def __init__(self, ad_id, keyword_id, desc_id):
	self.ad_id = ad_id
	self.keyword_id = keyword_id
	self.desc_id = desc_id	

    def __eq__(self, other):
	if other == None:
	    return False
	else:
	    return (self.ad_id == other.ad_id and self.keyword_id == other.keyword_id and 
		self.desc_id == other.desc_id)

    def __repr__(self):
	return "<Ad('%s', '%s', '%s')>" % (self.ad_id, self.keyword_id, self.desc_id)

    
