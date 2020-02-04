import json

def handle_mismatch(body, engine): 
    body = json.loads(body)
    v1 = body.get('v1')
    v2 = body.get('v2')
    condo = body.get('condo', 'TRUE')

    #. first check if the record already exist: 
    existence = engine.execute(f'''
        SELECT EXISTS (SELECT * FROM dcp_pluto.qaqc_mismatch WHERE pair = '{v1} - {v2}')
        ''').fetchone()
    
    if existence[0]:
        result = engine.execute(f'''
            SELECT * FROM dcp_pluto.qaqc_mismatch 
            WHERE pair = '{v1} - {v2}' and condo::boolean is {condo};
            ''').fetchall()
        return {
            'statusCode': 200,
            'body': {'result': [dict(row) for row in result]}
            }
    else: 
        return {
            'statusCode': 404,
            'body': {'result': []}
            }