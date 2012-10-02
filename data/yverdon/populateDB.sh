#!/bin/bash

WHICH="roads"
REPROJ="_reproj"
S_SRS="4326" # "27700"
T_SRS="21781"
TABLE="yverdon"

# clean old execution files
rm $WHICH$REPROJ.*

# reproject from British National Grid (27700) to Swiss lv3 (21781)
ogr2ogr -s_srs EPSG:$S_SRS -t_srs EPSG:$T_SRS -a_srs EPSG:$T_SRS -f "ESRI Shapefile" $WHICH$REPROJ.shp $WHICH.shp 

# shape to sql
sh -c "shp2pgsql -s $T_SRS -W LATIN1 $WHICH$REPROJ.shp $TABLE" > $WHICH$REPROJ.sql

# sql to postgresql
psql -U postgres -d top4net -h localhost -f $WHICH$REPROJ.sql
