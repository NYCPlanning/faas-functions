from cook import Importer
import json

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    req = json.loads(req)
    connection = req['connection']
    config = req['config']

    with open("/var/openfaas/secrets/recipe-engine","r") as secret:
        recipe_engine = (secret.read())
    
    build_engine = connection['build_engine']

    importer = Importer(recipe_engine, build_engine)
    try:
        importer.import_table(
            schema_name = config['schema_name'],
            version = 'latest' if config['version'].strip() == ''\
                             else config['version'].strip())
        return {"status":"success"}
    except: 
        return {"status":"failure"}