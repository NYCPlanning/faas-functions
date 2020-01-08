import json
from sqlalchemy import create_engine
from .mismatch import handle_mismatch
from .null import handle_null
from .aggregate import handle_aggregate

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
        return handle_mismatch(event.body, engine)
    
    # path for generating null comparison:
    elif event.path == '/null':
        return handle_null(event.body, engine)
    
    # path for generating aggregate variables:
    elif event.path == '/aggregate':
        return handle_aggregate(event.body, engine)