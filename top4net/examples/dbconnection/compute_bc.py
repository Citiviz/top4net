from sqlalchemy.sql import update
from model import table_name
from meta import Session, engine
from model import Network

import networkx as nx
from networkx.algorithms.centrality.betweenness import *

#import matplotlib.pyplot as plt
import sys

class ComputeEdgeBC():
    def __init__(self):
        self.network = Network

        self.G = nx.Graph()
        self.query = Session.query(self.network)
        self.bc = self.ComputeCentralities(self.G,self.query)

        self.UpdateTable(self.G,self.bc,self.network)
    
    def ComputeCentralities(self,G,query):
        for res in query:
            ed = res.compute_results(['id', 'fn_id', 'tn_id', 'length'])
            G.add_edge(ed['fn_id'], ed['tn_id'], weight=ed['length'], eid=ed['id'])
    
        print 'Start computing bc values'
        bc = edge_betweenness_centrality(G, True, 'weight')
        print 'Done...'
    
        return bc
    
    def UpdateTable(self,G,bc,model):
        print 'Start updating the table'
        ## TODO Make a unique update statement 
        for val in bc:
            edge_id = G.get_edge_data(val[0],val[1])['eid']
            u = update(model.__table__).where(model.id == edge_id).values(bc_value_w = bc[val])
            u.execute()
        print 'Table updated'

ComputeEdgeBC()
#nx.draw(g)
#plt.savefig("path.png")
#draw_networkx_edges
