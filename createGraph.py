import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

from SearchSession import *
from TestSession import *
from Keyword import *
from Advertiser import *
from BipartiteGraph import *
from SpectralBipartiteGraph import *

"""
Creates bipartite graph out of training set and test set (read from database)
Returns the bipartite graph & list of session from test set
"""
def createGraph(spectralGraph = False):
    # setup DB connection 
    engine = create_engine('sqlite:///ctr.db', echo=True)
    metadata = MetaData()

    # start new session
    Session = sessionmaker(bind=engine)
    session = Session()

    # create empty bipartite graph
    if spectralGraph == False:
	g = BipartiteGraph()
    else:
	g = SpectralBipartiteGraph()

    if spectralGraph == False:
	# make query to get all rows from search_sessions table
	for searchSession in session.query(SearchSession).all():
	    keyword = Keyword(searchSession.keyword_id)
	    advertiser = Advertiser(searchSession.advertiser_id)
	    g.add(advertiser, keyword)
    

	# make query to get all rows from test_sessions table (order by primary_id to 
	# maintain order in test set)
	list_of_test_sessions = session.query(TestSession).order_by(TestSession.primary_id)
	for testSession in list_of_test_sessions:
	    keyword = Keyword(testSession.keyword_id)
	    advertiser = Advertiser(testSession.advertiser_id)
	    g.add(advertiser, keyword)

    else:
	# make query to get all rows from search_sessions table
	for searchSession in session.query(SearchSession).all():
	    keyword = Keyword(searchSession.keyword_id)
	    advertiser = Advertiser(searchSession.advertiser_id)
	    g.add(advertiser, keyword, int(searchSession.position))
    

	# make query to get all rows from test_sessions table (order by primary_id to 
	# maintain order in test set)
	list_of_test_sessions = session.query(TestSession).order_by(TestSession.primary_id)
	for testSession in list_of_test_sessions:
	    keyword = Keyword(testSession.keyword_id)
	    if testSession.keyword_id == '394':
		print "Found advertiser:", testSession.advertiser_id
	    advertiser = Advertiser(testSession.advertiser_id)
	    g.add(advertiser, keyword, int(searchSession.position))

	
    #print repr(g)
    return (g, list_of_test_sessions)

# Test Main
if __name__ == '__main__':
    createGraph()
