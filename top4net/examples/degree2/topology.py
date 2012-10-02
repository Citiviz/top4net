#topology.py

from meta import engine
import sys
import time
import re


class Topology:

    def create(self, topo='topoyverdon', projection=21781, tolerance=2, geom='geom', db='yverdon'):
        conn = engine.connect()

        trans = conn.begin()
        toposql = "select topology.CreateTopology('%s', %d, %d)" %(topo, projection, tolerance)
        conn.execute(toposql)
        trans.commit()

        # TODO : Find a better way
        while True:
            try:
                engine.execute('select * from yverdon')
                sys.stdout.write('\n')
                sys.stdout.flush()
                break
            except:
                sys.stdout.write('.')
                sys.stdout.flush()
                time.sleep(.1)

        trans = conn.begin()
        geosql = "select topology.ST_CreateTopoGeo('%s',ST_Collect(%s)) from %s" %(topo, geom, db)
        conn.execute(geosql)
        trans.commit()


    def cleanDegree2Nodes(self)
        # getEdgesDegree2ByPostgis
        nodes = engine.execute("select node_id from topoyverdon.node")
        edge2 = for n in nodes:
            nid = n.items()[0][1]
            edges = list(engine.execute("select topology.GetNodeEdges('topoyverdon', %d)" %nid))
            degree = len(edges)
            if degree == 2:
                yield (re.search(r'\(\d,-?(\d+)\)', edges[0][0]).group(1), re.search(r'\(\d,-?(\d+)\)', edges[1][0]).group(1))

        # healEdges
        rmEdges = {}
        connection = engine.connect()
        try:
            for ed0, ed1 in list(edge2):
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
        except:
            print rmEdges
            trans.rollback()
            raise