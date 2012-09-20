from meta import engine
from model import table_name, table_name_node

column_name = 'bc_value'

def AddColumn(table_name, column_name):
    try:
        sql = 'ALTER TABLE %s ADD COLUMN %s double precision' %(table_name, column_name)
        engine.execute(sql)
        print 'Column %s has been created' %i(column_name)
        # Pause code before loading the model
    except:
        print 'Column %s exists already' %(column_name)

# AddColumn(table_name, column_name)
AddColumn(table_name_node, column_name)
