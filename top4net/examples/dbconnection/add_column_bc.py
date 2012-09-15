from meta import engine
from model import table_name

def AddColumnBC():
    try:
        sql = 'ALTER TABLE %s ADD COLUMN bc_value_w double precision' %(table_name)
        engine.execute(sql)
        print 'Column bc_value_w has been created'
        # Pause code before loading the model
    except:
        print 'Column bc_value_w exists already'

AddColumnBC()
