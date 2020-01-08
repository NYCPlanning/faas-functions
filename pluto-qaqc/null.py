from .sql import null_sql
import json

def handle_null(body, engine): 
    body = json.loads(body)
    v = body.get('v')
    condo = body.get('condo', 'TRUE')
    cached = body.get('cached', 'TRUE')

    #. first check if the record already exist: 
    existence = engine.execute(f'''
        SELECT EXISTS (SELECT * FROM dcp_pluto.qaqc_null WHERE v = '{v}')
        ''').fetchone()
    
    # Finalize SQL query
    if condo == 'TRUE':
        sql = null_sql.format(v, condo, "WHERE right(bbl, 4) LIKE '75%%'")
    else:
        sql = null_sql.format(v, condo, '')
    
    # if record exisit, drop, else insert
    if existence[0] and cached == 'TRUE':
        pass
    elif existence[0] and cached == 'FALSE':
        engine.execute(f'''
        DELETE FROM dcp_pluto.qaqc_null WHERE v = '{v}'; 
        {sql};
        ''')
    else:
        engine.execute(sql)

    result = engine.execute(f'''
        SELECT * FROM dcp_pluto.qaqc_null
        WHERE v = '{v}' and condo::boolean is {condo};
        ''').fetchall()
    return {
        'statusCode': 200,
        'body': {'result': [dict(row) for row in result]}
        }