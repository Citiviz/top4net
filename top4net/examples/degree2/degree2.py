'''
- We've tested two methods to get the edges around nodes of degree 2.
    1. by networkx with mapping to get all data from DB and filter them using graph functions
    2. by sql with simple request to get all data and filter using postgis functions
  The returned results are oddly different. Why ???
  The time is significantly better for the 1 solution.
  ie :
    All edges with nodes of degree 2 by networkx: 370 results in 0.431618 millisec
    All edges with nodes of degree 2 by postgis: 300 results in 8.179485 millisec


- The topology.ST_NewEdgeHeal function raise exception :
    other eges connected(ie:1939)
  But we filter edges for nodes of degree 2, so why ???

'''

from sqlalchemy.sql import update
from model import table_name
from meta import Session, engine
from model import Edge_data

import networkx as nx
import sys
import logging
import time



class RemoveDegree2:
    def __init__(self):
        #logging.basicConfig()
        #logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

        # --- By networkx ---
        #self.G = nx.Graph()
        #self.network = Edge_data
        #self.query = Session.query(self.network)
        #start = time.time()
        #self.edge2 = list(self.getEdgesDegree2ByNx())
        #print 'All edges with nodes of degree 2 by networkx: %d results in %f millisec' %(len(self.edge2), time.time() - start)
        #Session.close()

        # --- By postgis ---
        start = time.time()
        self.edge2 = list(self.getEdgesDegree2ByPostgis())
        print 'All edges with nodes of degree 2 by postgis: %d results in %f millisec' %(len(self.edge2), time.time() - start)

        # --- Heal ---
        start = time.time()
        self.healEdges()
        print 'Heal edges in %f millisec' %(time.time() - start)

    def getEdgesDegree2ByNx(self):
        for res in self.query:
            ed = res.compute_results(['edge_id','start_node','end_node'])
            self.G.add_edge(ed['start_node'], ed['end_node'], eid=ed['edge_id'])
        nodes = self.G.nodes()
        for node in nodes:
            if self.G.degree(node) == 2:
                edge1, edge2 = self.G.edges(node)
                yield self.G.get_edge_data(*edge1)['eid'], self.G.get_edge_data(*edge2)['eid']

    def getEdgesDegree2ByPostgis(self):
        import re
        nodes = engine.execute("select node_id from topoyverdon.node")
        for n in nodes:
            nid = n.items()[0][1]
            edges = list(engine.execute("select topology.GetNodeEdges('topoyverdon', %d)" %nid))
            degree = len(edges)
            if degree == 2:
                yield (re.search(r'\(\d,-?(\d+)\)', edges[0][0]).group(1), re.search(r'\(\d,-?(\d+)\)', edges[1][0]).group(1))

    def healEdges(self):
        rmEdges = {}
        connection = engine.connect()
        try:
            for ed0, ed1 in self.edge2:
                if ed0 in rmEdges:
                    ed0 = rmEdges[ed0]
                if ed1 in rmEdges:
                    ed1 = rmEdges[ed1]
                sql = "select topology.ST_NewEdgeHeal('%s', %s, %s)" %('topoyverdon', ed0, ed1)
                trans = connection.begin()
                newEdgeId = connection.execute(sql).scalar()
                trans.commit()
                rmEdges[ed0] = newEdgeId
                rmEdges[ed1] = newEdgeId
            print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        except:
            print rmEdges
            trans.rollback()
            raise

RemoveDegree2()




# OLD FUNCTION TO KEEP TO REMEMBER CODE IF WE NEED


    #def xxxhealEdges(self):
        #counter = 0
        #connection = engine.connect()
        #trans = connection.begin()
        #prec = [-1, -1]
        #try:
            #for ed in self.edge2:
                #print 'prec = %s, %s' %(prec[0],prec[1])
                #print 'ed = %s, %s' %(ed[0],ed[1])
                #if prec[1] == ed[0]:
                    #print 'if'
                    #sql = "select topology.ST_ModEdgeHeal('%s', %s, %s)" %('topoyverdon', prec[0], ed[1])
                #elif prec[1] == ed[1]:
                    #print 'elif'
                    #sql = "select topology.ST_ModEdgeHeal('%s', %s, %s)" %('topoyverdon', prec[0], ed[0])
                #else:
                    #print 'else'
                    #sql = "select topology.ST_ModEdgeHeal('%s', %s, %s)" %('topoyverdon', ed[0], ed[1])
                #nid = connection.execute(sql).scalar()
                #print 'deletedNode = %s edge = %s' %(str(nid),ed)
                #prec = [min(ed), max(ed)]
                #trans.commit()
            #except:
            #counter += 1
            #trans.rollback()
            #raise
        #print 'counter = %s' %counter