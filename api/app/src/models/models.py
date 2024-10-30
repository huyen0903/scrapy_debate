from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
Base = declarative_base()
import datetime

class House(Base):
    __tablename__ = 'house'

    id = Column(Integer, primary_key=True, index=True, name='index')
    motion = Column(String, nullable=True)
    topic_name = Column(String, nullable=True)
    post_type = Column(String, nullable=True)
    formatted_date = Column(String, nullable=True)
    describe = Column(String, nullable=True)
    points_for = Column(ARRAY(String), nullable=True) 
    points_against = Column(ARRAY(String), nullable=True) 
    bibliography = Column(ARRAY(String), nullable=True) 

class HouseVI(Base):
    __tablename__ = 'house_vi'

    id = Column(Integer, primary_key=True, index=True, name='house_index')
    motion = Column(String, nullable=True)
    topic_name = Column(String, nullable=True)
    post_type = Column(String, nullable=True)
    formatted_date = Column(String, nullable=True)
    describe = Column(String, nullable=True)
    points_for = Column(ARRAY(String), nullable=True) 
    points_against = Column(ARRAY(String), nullable=True) 
    bibliography = Column(ARRAY(String), nullable=True) 

class Competition(Base):
    __tablename__ = 'competition_data'

    id = Column(Integer, primary_key=True, index=True, name='index')
    motion = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    date = Column(DateTime, nullable=True)
    infoslide = Column(String, nullable=True)
    level = Column(String, nullable=True)
    region = Column(String, nullable=True)
    round = Column(String, nullable=True)
    tournament = Column(String, nullable=True)
    types = Column(ARRAY(String), nullable=True) 
    # adjudicator = Column(ARRAY(String), nullable=True) 

    
from pydantic import BaseModel
from typing import List

class Response(BaseModel):
    id : int = None
    motion:  str = None

    
class HouseResponse(BaseModel):
    id : int = None
    motion:  str = None
    topic_name:  str = None
    post_type:  str = None
    describe:  str = None
    points_for: List[str] = []
    points_again: List[str] = []
    bibliography: List[str] = []
    formatted_date: str
    
class CompetitionResponse(BaseModel):

    id  : int = None
    motion: str = None
    city:str = None
    country : str = None
    infoslide : str = None
    level: str = None
    region: str = None
    round : str = None
    tournament : str = None
    types : List[str] = [] 