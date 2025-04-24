from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    urls = relationship('URL', back_populates='user')

class URL(Base):
    __tablename__ = 'urls'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String(255), nullable=False)
    title = Column(String(255))
    seo_score = Column(Float)
    indexing_status = Column(String(50))
    last_analyzed = Column(DateTime)
    analysis_results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='urls')
    keywords = relationship('Keyword', secondary='url_keywords')

class Keyword(Base):
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    keyword = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    urls = relationship('URL', secondary='url_keywords')

url_keywords = Table('url_keywords', Base.metadata,
    Column('url_id', Integer, ForeignKey('urls.id'), primary_key=True),
    Column('keyword_id', Integer, ForeignKey('keywords.id'), primary_key=True)
)

class MetaTemplate(Base):
    __tablename__ = 'meta_templates'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100), nullable=False)
    title_template = Column(String(255))
    description_template = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)