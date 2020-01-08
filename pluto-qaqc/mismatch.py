from .sql import mismatch_sql
import json

def handle_mismatch(body, engine): 
    body = json.loads(body)
    v1 = body.get('v1')
    v2 = body.get('v2')
    condo = body.get('condo', 'TRUE')
    cached = body.get('cached', 'TRUE')

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
    if existence[0] and cached == 'TRUE':
        pass
    elif existence[0] and cached == 'FALSE':
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