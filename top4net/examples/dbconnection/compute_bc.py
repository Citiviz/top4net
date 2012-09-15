from sqlalchemy.sql import update
from meta import Session, engine

import networkx as nx
from networkx.algorithms.centrality.betweenness import *

import matplotlib.pyplot as plt
import sys

try:
    #Session.close()
    sql = 'ALTER TABLE topology ADD COLUMN bc_value_w double precision'
    engine.execute(sql)
except:
    print 'Column bc_value_w exists already'

# Import model after column creation to be able to access bc_value_w
try:
    from model import RawNetwork
except:
    print 'No model RawNetwork'
    sys.exit(1)

query = Session.query(RawNetwork)

g = nx.Graph()

for res in query:
     ed = res.compute_results(['id', 'fn_id', 'tn_id', 'length'])
     g.add_edge(ed['fn_id'], ed['tn_id'], weight=ed['length'], eid=ed['id'])

## Compute BC 
centralities_b = edge_betweenness_centrality(g, True, 'weight')

if Session.is_active == False:
    Session.new()

## TODO Make one unique update statement 
for val in centralities_b:
    edge_id = g.get_edge_data(val[0],val[1])['eid']
    u = update(RawNetwork.__table__).where(RawNetwork.id == edge_id).values(bc_value_w = centralities_b[val])
    u.execute()

#nx.draw(g)
#plt.savefig("path.png")
#draw_networkx_edges
