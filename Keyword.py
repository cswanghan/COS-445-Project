
class Keyword(object):
    def __init__(self, keyword_id):
	self.keyword_id = keyword_id 

    def __eq__(self, other):
	if other == None:
	    return False
	else:
	    return (self.keyword_id == other.keyword_id)

    def __repr__(self):
	return "<Keyword('%s')>" % (self.keyword_id)

