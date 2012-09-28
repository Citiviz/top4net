from sqlalchemy.sql import update
from model import table_name
from meta import Session, engine
from model import Edge_data

import networkx as nx
import sys
import logging



class RemoveDegree2:
    def __init__(self):
        #logging.basicConfig()
        #logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        self.G = nx.Graph()
        self.network = Edge_data
        self.query = Session.query(self.network)
        self.edge2 = list(self.getEdgesDegree2())
	Session.close()
        self.healEdges()

    def getEdgesDegree2(self):
        for res in self.query:
            ed = res.compute_results(['edge_id','start_node','end_node'])
            self.G.add_edge(ed['start_node'], ed['end_node'], eid=ed['edge_id'])
        nodes = self.G.nodes()
        for node in nodes:
            if self.G.degree(node) == 2:
                edge1, edge2 = self.G.edges(node)
                yield self.G.get_edge_data(*edge1)['eid'], self.G.get_edge_data(*edge2)['eid']
                
    def xxxhealEdges(self):
        counter = 0
	connection = engine.connect()
	trans = connection.begin()
	prec = [-1, -1]
	try:
    	    for ed in self.edge2:
	        print 'prec = %s, %s' %(prec[0],prec[1])
	        print 'ed = %s, %s' %(ed[0],ed[1])
		if prec[1] == ed[0]:
		    print 'if'
		    sql = "select topology.ST_ModEdgeHeal('%s', %s, %s)" %('topoyverdon', prec[0], ed[1])
		elif prec[1] == ed[1]:
		    print 'elif'
                    sql = "select topology.ST_ModEdgeHeal('%s', %s, %s)" %('topoyverdon', prec[0], ed[0])
		else:
		    print 'else'
                    sql = "select topology.ST_ModEdgeHeal('%s', %s, %s)" %('topoyverdon', ed[0], ed[1])
                nid = connection.execute(sql).scalar()
                print 'deletedNode = %s edge = %s' %(str(nid),ed)
	        prec = [min(ed), max(ed)]
	    trans.commit()
	except:
	    counter += 1
	    trans.rollback()
	    raise
	print 'counter = %s' %counter
          
           

        def healEdges(self):
	    rmEdges = {}
	    connection = engine.connect()
	    trans = connection.begin()
	    try:
	        for ed in self.edge2:
	            if rmEdges.has_key(str(ed[0])):
		        ed[0] = rmEdges[ed[0]]
		    elif rmEdges.has_key(str(ed[1])):
		        ed[1] = rmEdges[ed[1]]
                    sql = "select topology.ST_NewEdgeHeal('%s', %s, %s)" %('topoyverdon', ed[0], ed[1])
		    newEdgeId = connection.execute(sql).scalar()
		    rmEdges.update(str(ed[0])=newEdgeId)
		    rmEdges.update(str(ed[1])=newEdgeId)
	        trans.commit()
	    except:
	        trans.rollback()
		raise

RemoveDegree2()
