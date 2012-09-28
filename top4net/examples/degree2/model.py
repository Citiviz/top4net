from sqlalchemy import Column, update
from sqlalchemy.types import Integer, Text, String, Float
from sqlalchemy.ext.declarative import declarative_base

from geoalchemy import Geometry, WKBSpatialElement, GeometryColumn

from meta import engine, metadata

schema = 'topoyverdon'
table_name = 'edge_data'
table_name_node = 'node'

__all__ = ['table_name']

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

class Edge_data(Base, BaseObject):
    __tablename__ = table_name
    __table_args__ = ({'schema': schema, 'autoload': True})
    edge_id = Column('edge_id', Integer, primary_key=True)
    geom = GeometryColumn(Geometry)

'''class Node(Base, BaseObject):
    __tablename__ = table_name_node
    __table_args__ = ({'schema': schema, 'autoload': True})
    node_id = Column('node_id', Integer, primary_key=True)
    geom = GeometryColumn(Geometry)'''
