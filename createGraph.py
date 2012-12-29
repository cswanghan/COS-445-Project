import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

from SearchSession import *
#from Ad import *
from Keyword import *
from Advertiser import *
from BipartiteGraph import *


def createGraph():
    # setup DB connection 
    engine = create_engine('sqlite:///ctr.db', echo=True)
    metadata = MetaData()

    # start new session
    Session = sessionmaker(bind=engine)
    session = Session()

    # make query to get all rows from search_sessions table
    g = BipartiteGraph()
    firstAdv = None
    count = 0

    for searchSession in session.query(SearchSession).all():
	#ad = Ad(searchSession.ad_id, searchSession.keyword_id, searchSession.desc_id)
	keyword = Keyword(searchSession.keyword_id)
	advertiser = Advertiser(searchSession.advertiser_id)
	g.add(advertiser, keyword)

	if count == 0:
	    firstAdv = advertiser
    
	count += 1

    print repr(g)
    return g

# Test Main
if __name__ == '__main__':
    createGraph()
