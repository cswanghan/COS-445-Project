import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker

# Session object that defines 'search_sessions' table
class SearchSession(object):
    def __init__(self, primary_id, clicks, impressions, display_URL, ad_id, 
		advertiser_id, depth, position, query_id, keyword_id,
		title_id, desc_id, user_id):
	self.primary_id = primary_id
	self.clicks = clicks
	self.impressions = impressions
	self.display_URL = display_URL
	self.ad_id = ad_id
	self.advertiser_id = advertiser_id
	self.depth = depth
	self.position = position
	self.query_id = query_id
	self.keyword_id = keyword_id
	self.title_id = title_id
	self.desc_id = desc_id
	self.user_id = user_id

    def __repr__(self):
	return "<SearchSession('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
			       str(self.clicks), str(self.impressions), self.display_URL, self.ad_id, self.advertiser_id,
			       str(self.depth), str(self.position), self.query_id, self.keyword_id, self.title_id, self.desc_id, 
			       self.user_id
			       )


if __name__ == '__main__':
    # setup DB connection 
    engine = create_engine('sqlite:///ctr2.db', echo=True)
    metadata = MetaData()

    # define search session table
    sessions_table = Table('search_sessions', metadata, 
	   Column('primary_id', String, primary_key=True),
	   Column('clicks', Integer), 
	   Column('impressions', Integer),
	   Column('display_URL', String(40)),
	   Column('ad_id', String(40)), 
	   Column('advertiser_id', String(40)),
	   Column('depth', Integer),
	   Column('position', Integer),
	   Column('query_id', String(40)),
	   Column('keyword_id', String(40)),
	   Column('title_id', String(40)),
	   Column('desc_id', String(40)),
	   Column('user_id', String(40)))

    # drop existing tables
    metadata.drop_all(engine)

    # create table
    metadata.create_all(engine) 

    # creat mapping 
    mapper(SearchSession, sessions_table)

    # start new session 
    Session = sessionmaker(bind=engine)
    session = Session()

    sessions_table.delete()

    # read each instance from training set and 
    # add to database as row
    f = open('training1000.txt', 'r')
    l = []
    id = 1

    for line in f.readlines():
	print "HELLO", id
	fields = line.split()
	l.append(SearchSession(str(id), int(fields[0]),
	             int(fields[1]),
		     fields[2],
		     fields[3],
		     fields[4],
		     int(fields[5]),
		     int(fields[6]),
		     fields[7],
		     fields[8],
		     fields[9],
		     fields[10],
		     fields[11]))

	id += 1
    
    session.add_all(l)
    session.commit()
