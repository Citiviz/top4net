from top4net.ogr2ogr import populate
from top4net.examples.degree2.topology import Topology
import time


def install():
    ''' Works only one time !

        The following data will be created:
          - reprojected shape files
          - sql file from reprojected files
          - database in public schema
          - topo schema

        Try to run with these previous data already created will fail.
    '''

    start = time.time()
    populate()
    print ' >>> Populate: %f [ms]' %(time.time() - start)

    topo = Topology()
    start = time.time()
    topo.create()
    print ' >>> Create topology: %f [ms]' %(time.time() - start)



install()