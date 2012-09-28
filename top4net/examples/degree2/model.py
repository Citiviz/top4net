from sqlalchemy import Column, update
from sqlalchemy.types import Integer, Text, String, Float
from sqlalchemy.ext.declarative import declarative_base

from geoalchemy import Geometry, WKBSpatialElement, GeometryColumn

from meta import engine, metadata

table_name = 'syria_network_epsg32636_c_t4n'
table_name_node = 'syria_nodes_epsg32636_c_t4n'

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

class Network(Base, BaseObject):
    __tablename__ = table_name
    __table_args__ = ({'schema': 'public', 'autoload': True})
    id = Column('gid', Integer, primary_key=True)
    the_geom = GeometryColumn(Geometry)
    #bc_value_w = Column('bc_value_w', Float)

"""class Node(Base, BaseObject):
    __tablename__ = table_name_node
    __table_args__ = ({'schema': 'public', 'autoload': True})
    id = Column('gid', Integer, primary_key=True)
    the_geom = GeometryColumn(Geometry)"""
