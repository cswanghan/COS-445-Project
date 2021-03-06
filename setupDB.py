import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from SearchSession import *
from TestSession import *

if __name__ == '__main__':
    # setup DB connection 
    engine = create_engine('sqlite:///ctr.db', echo=False)
    metadata = MetaData()

    # define search session table
    sessions_table = Table('search_sessions', metadata, 
	   Column('primary_id', Integer, primary_key=True),
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

    # define test sessions table
    test_sessions_table = Table('test_sessions', metadata, 
	   Column('primary_id', Integer, primary_key=True),
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

    # start new session 
    Session = sessionmaker(bind=engine)
    session = Session()

    # read each instance from training set and 
    # add to database as row
    f = open('training1000.txt', 'r')
    l = []
    id = 1

    for line in f.readlines():
	fields = line.split()
	l.append(SearchSession(id, int(fields[0]),
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
    f.close()

    # reach each instance from test set and 
    # add to database as row
    f = open('test100.txt', 'r')
    l = []
    id = 1

    for line in f.readlines():
	print "keyword_read", fields[6]
	fields = line.split()
	l.append(TestSession(id, 
		     fields[0],
		     fields[1],
		     fields[2],
		     int(fields[3]),
		     int(fields[4]),
		     fields[5],
		     fields[6],
		     fields[7],
		     fields[8],
		     fields[9]))
	id += 1
    
    session.add_all(l)
    f.close()
    
    session.commit()
