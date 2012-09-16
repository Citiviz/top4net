from sqlalchemy.sql import update
from model import table_name
from meta import Session, engine
from model import Network

import networkx as nx
from networkx.algorithms.centrality.betweenness import *

#import matplotlib.pyplot as plt
import sys

class ComputeEdgeBC:
    def __init__(self):
        self.bc = None
        self.network = Network
        self.G = nx.Graph()
        self.query = Session.query(self.network)
        
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
            u = update(self.network.__table__).where(self.network.id == edge_id).values(bc_value_w = self.bc[val])
            u.execute()
        print 'Table updated'

ComputeEdgeBC()
#nx.draw(g)
#plt.savefig("path.png")
#draw_networkx_edges
