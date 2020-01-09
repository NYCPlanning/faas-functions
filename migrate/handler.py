import json 
from .utils import migrate_table

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    config=json.loads(req)
    schema_name=config.get('schema_name')
    try:
        migrate_table(**config)
        config.pop('src_engine')
        config.pop('dst_engine')
        return json.dumps({
            'status': 'success', 
            'config': config
            })
    except:
        config.pop('src_engine')
        config.pop('dst_engine')
        return json.dumps({
            'status': 'failure', 
            'config': config, 
        })