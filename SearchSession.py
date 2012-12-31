from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

Base = declarative_base()

# Session object that defines 'search_sessions' table
class SearchSession(Base):
    __tablename__ = 'search_sessions'

    primary_id = Column(Integer, primary_key=True)
    clicks = Column(Integer)
    impressions = Column(Integer)
    display_URL = Column(String(40))
    ad_id = Column(String(40))
    advertiser_id = Column(String(40))
    depth = Column(Integer)
    position = Column(Integer)
    query_id = Column(String(40))
    keyword_id = Column(String(40))
    title_id = Column(String(40))
    desc_id = Column(String(40))
    user_id = Column(String(40))

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

