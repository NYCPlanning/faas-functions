import json
import datetime
from flask import jsonify
from sqlalchemy import create_engine

def handle(event, context):
    """handle a request to the function
    Args:
        req (str): request body
    """
    with open("/var/openfaas/secrets/recipe-engine","r") as secret:
        recipe_engine = (secret.read())
    
    engine = create_engine(recipe_engine)

    if event.path == '/api': 
        result = engine.execute('''
        select schema_name, config, last_update::text 
        from meta.metadata''').fetchall()
        return {
            'statusCode': 200, 
            'body': {'result': [dict(row) for row in result]}
            }
    elif event.path == '/schema_names': 
        result = engine.execute('''
        select distinct schema_name from meta.metadata''').fetchall()
        return {
            'statusCode': 200, 
            'body': {'result': [dict(row) for row in result]}
            }
    else:
        schema_name = event.path.replace('/api/', '')
        result = engine.execute(f'''
            select schema_name, config, last_update::text 
            from meta.metadata where schema_name ~* '{schema_name}';
            ''').fetchall()
        return {
            'statusCode': 200,
            'body': {'result': [dict(row) for row in result]}
            }