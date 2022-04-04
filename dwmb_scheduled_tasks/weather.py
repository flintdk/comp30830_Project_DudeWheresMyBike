# NOT USED YET NOT USED YET NOT USED YET NOT USED YET 

# SQLAlchemy ORM Definition for a Weather DB table
# 
# Resources used when building this file (for the dev):
# https://amercader.net/blog/beware-of-json-fields-in-sqlalchemy/
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy_json import mutable_json_type

Base = declarative_base()

class Document(Base):

    __tablename__ = 'import_log'

    id = Column(Integer, primary_key=True)
    jcdecaux = Column(MutableDict.as_mutable(JSONB))
    openweather = Column(MutableDict.as_mutable(JSONB))