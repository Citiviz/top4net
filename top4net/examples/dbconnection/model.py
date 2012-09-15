from sqlalchemy import Column, update
from sqlalchemy.types import Integer, Text, String, Float
from sqlalchemy.ext.declarative import declarative_base

from geoalchemy import Geometry, WKBSpatialElement, GeometryColumn

from meta import engine, metadata

#import networkx as nx
#from networkx.algorithms.centrality.betweenness import *

#import matplotlib.pyplot as plt

table_name = 'topology'

Base = declarative_base(bind=engine)

class BaseObject(object):
    """Add whatever method you need for the service"""

    def compute_results(self, properties):
        results = {}
        # If no properties are passed return all the columns
        for prop in properties:
            # Check if the propeties is in the layer
            if hasattr(self, prop):
                results.update({prop: self.__getattribute__(prop)})
        return results

class RawNetwork(Base, BaseObject):
    __tablename__ = table_name
    __table_args__ = ({'schema': 'public', 'autoload': True})
    id = Column('gid', Integer, primary_key=True)
    geom = GeometryColumn(Geometry)
