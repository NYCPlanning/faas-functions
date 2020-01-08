import json
import datetime
from sqlalchemy import create_engine
from .sql import mismatch_sql

def handle(event, context):
    with open("/var/openfaas/secrets/edm-data","r") as secret:
        edm_data = secret.read()
    
    engine = create_engine(edm_data)

    # path for retreiving versions
    if event.path == '/versions': 
        result = engine.execute('''
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'dcp_pluto'
        ''').fetchall()
        return {
            'statusCode': 200,
            'body': {'result': [dict(row) for row in result]}
            }
    # path for generating mismatches:
    elif event.path == '/mismatch':
        body = json.loads(event.body)
        v1 = body.get('v1') # e.g. 19v1
        v2 = body.get('v2') # e.g. 19v2
        condo = body.get('condo', 'FALSE') # NULL or condo
        #. first check if the record already exist: 
        existence = engine.execute(f'''
            SELECT EXISTS (SELECT * FROM dcp_pluto.qaqc_mismatch WHERE pair = '{v1} - {v2}')
            ''').fetchone()
        
        # Finalize SQL query
        if condo == 'TRUE':
            sql = mismatch_sql.format(v1, v2, condo, "WHERE right(bbl, 4) LIKE '75%%'")
        else:
            sql = mismatch_sql.format(v1, v2, condo, '')
        
        # if record exisit, drop, else insert
        if existence[0]: 
            engine.execute(f'''
            DELETE FROM dcp_pluto.qaqc_mismatch WHERE pair = '{v1} - {v2}'; 
            {sql};
            ''')
        else: 
            engine.execute(sql)

        result = engine.execute(f'''
            SELECT * FROM dcp_pluto.qaqc_mismatch 
            WHERE pair = '{v1} - {v2}' and condo::boolean is {condo};
            ''').fetchall()
        return {
            'statusCode': 200,
            'body': {'result': [dict(row) for row in result]}
            }