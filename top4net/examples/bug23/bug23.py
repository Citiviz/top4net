'''

'''

from meta import Session, engine
from model import Edge_data, schema

import networkx as nx
import time
import re



class Bug23:
    def __init__(self):

        # The three nodes that returns wrong edges
        self.errorNodes = [2054, 2681, 91]

        # --- By networkx MultiGraph ---
        start = time.time()
        edge2NxMG = list(self.getEdgesDegree2ByNxMG())
        print ' >>> All edges with nodes of degree 2 by nx.MultiGraph: %d results in %f secondes' %(len(edge2NxMG), time.time() - start)
        oltNxMG = orderListOfTuple(edge2NxMG)

        # --- By postgis ---
        start = time.time()
        edge2Postgis = list(self.getEdgesDegree2ByPostgis())
        print ' >>> All edges with nodes of degree 2 by postgis: %d results in %f secondes' %(len(edge2Postgis), time.time() - start)
        oltPostgis = orderListOfTuple(edge2Postgis)

        print list(diffListOfTuple(oltPostgis, oltNxMG))

    #---------------------------
    #--- networkx MultiGraph ---
    #---------------------------
    def printErrorEdgesNxMG(self):
        for node in self.errorNodes:
            edge1, edge2 = MG.edges(node)
            ed1 = MG.get_edge_data(*edge1)[0]['eid']
            ed2 = MG.get_edge_data(*edge2)[0]['eid']
            print 'MG: %s / %s / %s' %(node, ed1, ed2)

    def getEdgesDegree2ByNxMG(self):
        MG = nx.MultiGraph()
        networkMG = Edge_data
        queryMG = Session.query(networkMG)
        Session.close()
        for res in queryMG:
            ed = res.compute_results(['edge_id','start_node','end_node'])
            MG.add_edge(ed['start_node'], ed['end_node'], eid=ed['edge_id'])
        nodes = MG.nodes()
        for node in nodes:
            if MG.degree(node) == 2:
                edge1, edge2 = MG.edges(node)
                ed1 =MG.get_edge_data(*edge1)[0]['eid']
                ed2 = MG.get_edge_data(*edge2)[0]['eid']
                #print '%s / %s / %s' %(node, ed1, ed2)
                yield (ed1, ed2)


    #---------------
    #--- Postgis ---
    #---------------
    def printErrorEdgesPostgis(self):
        for node in self.errorNodes:
            edges = list(engine.execute("select topology.GetNodeEdges('%s', %d)" %(schema, node)))
            ed1 = int(re.search(r'\(\d,-?(\d+)\)', edges[0][0]).group(1))
            ed2 = int(re.search(r'\(\d,-?(\d+)\)', edges[1][0]).group(1))
            print 'Postgis: %s / %s / %s' %(node, ed1, ed2)

    def getEdgesDegree2ByPostgis(self):
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


def orderListOfTuple(xxx):
    yyy = []
    for x in xxx:
        yyy.append(sorted(x))
    return sorted(yyy, key=lambda tup: tup[0])

def diffListOfTuple(xxx, yyy):
    if len(xxx) == len(yyy):
        i = 0
        for x in xxx:
            y = yyy[i]
            if x != y:
                if (i+1) < len(xxx):
                    if not((x == yyy[i+1]) & (xxx[i+1] == y)): # TODO : correct
                        yield (x, y)
                yield (x, y)
            i += 1
    else:
        yield 'Lists must have the same length !'


Bug23()

