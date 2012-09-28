from sqlalchemy.sql import update
from model import table_name
from meta import Session, engine
from model import Network

import networkx as nx
import sys

class RemoveDegree2:
    def __init__(self):
        self.G = nx.Graph()
        self.network = Network
        self.query = Session.query(self.network)
        self.node2 = list(self.getNodeDegree2())
        self.healEdges()

    def getNodeDegree2(self):
        for res in self.query:
            ed = res.compute_results(['id','fn_id','tn_id'])
            self.G.add_edge(ed['fn_id'], ed['tn_id'], eid=ed['id'])
        nodes = self.G.nodes()
        for node in nodes:
            if self.G.degree(node) == 2:
                yield node
         
    def healEdges(self):
        i = 1
          
                
RemoveDegree2()
