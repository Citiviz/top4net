'''
- We've tested two methods to get the edges around nodes of degree 2.
    1. by networkx with mapping to get all data from DB and filter them using graph functions
    2. by sql with simple request to get all data and filter using postgis functions
  The returned results are oddly different. Why ???
  The time is significantly better for the 1 solution.
  ie :
    All edges with nodes of degree 2 by networkx: 370 results in 0.431618 secondes
    All edges with nodes of degree 2 by postgis: 300 results in 8.179485 secondes


- The topology.ST_NewEdgeHeal function raise exception :
    other eges connected(ie:1939)
  But we filter edges for nodes of degree 2, so why ???

'''

from sqlalchemy.sql import update
from model import table_name
from meta import Session, engine
from model import Edge_data, schema

import networkx as nx
import sys
import logging
import time
import re



class RemoveDegree2:
    def __init__(self):
        #logging.basicConfig()
        #logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

        # --- By networkx Graph ---
        #start = time.time()
        #edge2G = list(self.getEdgesDegree2ByNxG())
        #print edge2G
        #print ' >>> All edges with nodes of degree 2 by nx.Graph: %d results in %f secondes' %(len(edge2G), time.time() - start)

        # --- By networkx MultiGraph ---
        #self.getEdgesDegree2ByNxMG()
        start = time.time()
        edge2MG = list(self.getEdgesDegree2ByNxMG())
        ##print edge2MG
        print ' >>> All edges with nodes of degree 2 by nx.MultiGraph: %d results in %f secondes' %(len(edge2MG), time.time() - start)
        #xxx = []
        #for x in edge2MG:
            #xxx.append(sorted(x))
        #print sorted(xxx, key=lambda tup: tup[0])

        # --- By postgis ---
        #self.getEdgesDegree2ByPostgis()
        start = time.time()
        edge2 = list(self.getEdgesDegree2ByPostgis())
        ##print edge2
        print ' >>> All edges with nodes of degree 2 by postgis: %d results in %f secondes' %(len(edge2), time.time() - start)
        #yyy = []
        #for y in edge2:
            #yyy.append(sorted(y))
        #print sorted(yyy, key=lambda tup: tup[0])

        #--- Heal ---
        #start = time.time()
        #self.healEdges(edge2MG)
        #print 'Heal edges in %f secondes' %(time.time() - start)

    #def getEdgesDegree2ByNxG(self):
        #G = nx.Graph()
        #networkG = Edge_data
        #queryG = Session.query(networkG)
        #Session.close()
        #for res in queryG:
            #ed = res.compute_results(['edge_id','start_node','end_node'])
            #G.add_edge(ed['start_node'], ed['end_node'], eid=ed['edge_id'])
        #nodes = G.nodes()
        #for node in nodes:
            #if G.degree(node) == 2:
                #edge1, edge2 = G.edges(node)
                #yield G.get_edge_data(*edge1)['eid'], G.get_edge_data(*edge2)['eid']

    def getEdgesDegree2ByNxMG(self):
        MG = nx.MultiGraph()
        networkMG = Edge_data
        queryMG = Session.query(networkMG)
        Session.close()
        for res in queryMG:
            ed = res.compute_results(['edge_id','start_node','end_node'])
            MG.add_edge(ed['start_node'], ed['end_node'], eid=ed['edge_id'])
        #for node in [2054, 2681, 91]:
            ##print MG.edges(node)
            #edge1, edge2 = MG.edges(node)
            #ed1 = MG.get_edge_data(*edge1)[0]['eid']
            #ed2 = MG.get_edge_data(*edge2)[0]['eid']
            #print 'MG: %s / %s / %s' %(node, ed1, ed2)
        nodes = MG.nodes()
        for node in nodes:
            if MG.degree(node) == 2:
                edge1, edge2 = MG.edges(node)
                ed1 =MG.get_edge_data(*edge1)[0]['eid']
                ed2 = MG.get_edge_data(*edge2)[0]['eid']
                #print '%s / %s / %s' %(node, ed1, ed2)
                yield (ed1, ed2)

    def getEdgesDegree2ByPostgis(self):
        #for node in [2054, 2681, 91]:
            #edges = list(engine.execute("select topology.GetNodeEdges('%s', %d)" %(schema, node)))
            #ed1 = int(re.search(r'\(\d,-?(\d+)\)', edges[0][0]).group(1))
            #ed2 = int(re.search(r'\(\d,-?(\d+)\)', edges[1][0]).group(1))
            #print 'Postgis: %s / %s / %s' %(node, ed1, ed2)
        nodes = list(engine.execute("select node_id from %s.node" %schema))
        for n in nodes:
            nid = n.items()[0][1]
            edges = list(engine.execute("select topology.GetNodeEdges('%s', %d)" %(schema, nid)))
            degree = len(edges)
            if degree == 2:
                ed1 = int(re.search(r'\(\d,-?(\d+)\)', edges[0][0]).group(1))
                ed2 = int(re.search(r'\(\d,-?(\d+)\)', edges[1][0]).group(1))
                #print '%s / %s / %s' %(nid, ed1, ed2)
                yield (ed1, ed2)

    def healEdges(self, seq):
        rmEdges = {}
        connection = engine.connect()
        try:
            for ed0, ed1 in seq:
                if ed0 != ed1: #avoid weired error ticket number ???
                    if ed0 in rmEdges:
                        ed0 = rmEdges[ed0]
                    if ed1 in rmEdges:
                        ed1 = rmEdges[ed1]
                    sql = "select topology.ST_NewEdgeHeal('%s', %s, %s)" %(schema, ed0, ed1)
                    trans = connection.begin()
                    newEdgeId = connection.execute(sql).scalar()
                    trans.commit()
                    rmEdges[ed0] = newEdgeId
                    rmEdges[ed1] = newEdgeId
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