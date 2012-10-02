#topology.py

from meta import engine
import sys
import time


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