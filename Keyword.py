import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

from SearchSession import *

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

    """
    Return the average CTR for keyword using data from
    all search sessions in training set

    Returns None if keyword is not found in DB 
    - means keyword is only in test set
    """
    def averageCTR(self):
	# setup DB connection
        engine = create_engine('sqlite:///ctr.db', echo=False)
	metadata = MetaData()

	# start new session
	Session = sessionmaker(bind=engine)
	session = Session()

	# make query to get all rows from search_sessions table
	# with this specific keyword id
	list_of_matching_search_sessions =  session.query(SearchSession).filter_by(keyword_id = self.keyword_id)

	# compute average CTR over this list
	total = 0.0
	count = 0
	for search_session in list_of_matching_search_sessions:
	    total += float(search_session.clicks)/float(search_session.impressions)
	    count += 1

	if count == 0:
	    return None
	else:
	    return total/count



