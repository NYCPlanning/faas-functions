import json

def handle_null(body, engine): 
    body = json.loads(body)
    v = body.get('v')
    condo = body.get('condo', 'TRUE')

    #. first check if the record already exist: 
    existence = engine.execute(f'''
        SELECT EXISTS (SELECT * FROM dcp_pluto.qaqc_null WHERE v = '{v}')
        ''').fetchone()

    if existence[0]:
        result = engine.execute(f'''
            SELECT * FROM dcp_pluto.qaqc_null
            WHERE v = '{v}' and condo::boolean is {condo};
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