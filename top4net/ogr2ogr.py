# ogr2ogr.py
import os
import glob

def clip_shp_to_shp(directory, shpclippath, pref="", suf="_clip"):
    # List shp file in a directory (not recursive)
    listResults = glob.glob(os.path.join(directory, '*.shp'))
    # call ogr2ogr to clip with shpclip var
    import subprocess
    for source in listResults:
        subprocess.call(["ogr2ogr", "-f", "ESRI Shapefile", "-clipsrc", shpclippath, os.path.basename(source) + "_clip.shp", source])

# set clipping shp path
# shpclip = "/home/loic/clipping_area.shp"
# set dir where searching shp to clip
# directory = os.getcwd()
# clip_shp_to_shp(directory, shpclip)

# TODO Test Encoding
def shp_2_sql(path_2_shape, srs, table_name, path_2_sql, encoding='LATIN1'):
    import subprocess
    try:
        subprocess.call(["sh", "-c", "shp2pgsql -s "+srs+" "+"-W"+" "+encoding+" "+path_2_shape+" "+table_name+" > "+path_2_sql])
    except:
        encoding = 'UTF-8'
        try:
            subprocess.call(["sh", "-c", "shp2pgsql -s "+srs+" "+"-W"+" "+encoding+" "+path_2_shape+" "+table_name+" > "+path_2_sql])
        except:
            print 'An error occured during the conversion of the shapefile to sql'
            sys.exit(1)

def sql_2_postgresql(database, path_2_sql, user='postgres', host='localhost'):
    from subprocess import Popen, PIPE
    psql_pass = dict(PGPASSWORD = 'postgres')
    su_process = Popen("psql -U "+user+" "+"-d "+database+" "+"-h "+host+" "+"-f "+path_2_sql, shell=True, env=psql_pass, stdout=PIPE, stderr=PIPE)
    #data = su_process.stdout.read()
    #err = su_process.stderr.read()

def reproject(s_srs, t_srs, path2_s_shp, path2_t_shp):
    import subprocess
    s_srs = "EPSG:"+s_srs
    t_srs = "EPSG:"+t_srs
    subprocess.call(["ogr2ogr","-s_srs", s_srs, "-t_srs", t_srs, "-a_srs", t_srs, "-f", "ESRI Shapefile", path2_t_shp, path2_s_shp])
