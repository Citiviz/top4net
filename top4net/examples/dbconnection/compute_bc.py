from sqlalchemy.sql import update
from model import table_name
from meta import Session, engine
from model import Network, Node

import networkx as nx
from networkx.algorithms.centrality.betweenness import *

#import matplotlib.pyplot as plt
import sys

column_name = 'bc_value'

class ComputeEdgeBC:
    def __init__(self, column_name):
        self.bc = None
        self.G = nx.Graph()
        self.network = Network
        self.column_name = column_name
        self.query = Session.query(Network)
        
        self.ComputeBC()
        self.UpdateTable()
    
    def ComputeBC(self):
        for res in self.query:
            ed = res.compute_results(['id', 'fn_id', 'tn_id', 'length'])
            self.G.add_edge(ed['fn_id'], ed['tn_id'], weight=ed['length'], eid=ed['id'])
    
        print 'Start computing bc values'
        self.bc = edge_betweenness_centrality(self.G, True, 'weight')
        print 'Done...'
    
    def UpdateTable(self):
        print 'Start updating the table'
        ## TODO Make a unique update statement 
        for val in self.bc:
            edge_id = self.G.get_edge_data(val[0],val[1])['eid']
            bc_value = self.network.__table__.columns[self.column_name]
            u = update(self.network.__table__).where(self.network.id == edge_id).values(bc_value = self.bc[val])
            u.execute()
        print 'Table updated'

class ComputeNodeBC:
    def __init__(self, column_name):
        self.bc = None
        self.G = nx.Graph()
        self.network = Network
        self.node = Node
        self.column_name = column_name
        self.query = Session.query(self.network)

        self.ComputeBC()
        self.UpdateTable()

    def ComputeBC(self):
        for res in self.query:
            ed = res.compute_results(['id', 'fn_id', 'tn_id', 'length'])
            self.G.add_edge(ed['fn_id'], ed['tn_id'], weight=ed['length'])

        print 'Start computing bc values'
        self.bc = betweenness_centrality(self.G, True, 'weight')
        print 'Done...'

    def UpdateTable(self):
        print 'Start updating the table'
        ## TODO Make a unique update statement 
        bc_value = self.node.__table__.columns[self.column_name]
        for val in self.bc:
            u = update(self.node.__table__).where(self.node.id == val).values(bc_value = self.bc[val])
            u.execute()
        print 'Table updated'

ComputeNodeBC(column_name)
#ComputeEdgeBC(column_name)

#nx.draw(G)
#plt.savefig("path.png")
#draw_networkx_edges
