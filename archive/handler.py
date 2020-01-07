from cook import Archiver
import sys
import json
import datetime
import os
import sys
from sqlalchemy import create_engine

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    with open("/var/openfaas/secrets/ftp-prefix","r") as secret:  
        ftp_prefix = (secret.read())

    with open("/var/openfaas/secrets/recipe-engine","r") as secret:
        recipe_engine = (secret.read())

    config = json.loads(req)
    config['version_name'] = datetime.datetime.today().strftime("%Y/%m/%d")\
                                if config['version_name'] == '' \
                                    else config['version_name']
    archiver=Archiver(engine=recipe_engine, ftp_prefix=ftp_prefix)
    try:
        archiver.archive_table(config)
        log_config(config, recipe_engine)
        return {"status":"success"}
    except: 
        return {"status":"failure", "error": f"{sys.exc_info()}", }

def log_config(config, recipe_engine):
    engine = create_engine(recipe_engine)
    table_in_db = engine.execute(f'''
        select exists(
            select * from meta.metadata 
            where schema_name='{config['schema_name']}');
        ''').fetchone()[0]
    if table_in_db: # if table already exists, then update config
        engine.execute(f'''
            UPDATE meta.metadata
            SET config='{json.dumps(config)}'::jsonb,
                last_update=now()
            WHERE schema_name='{config['schema_name']}';
        ''')
    else: # if table is new, then insert new record
        engine.execute(f'''
            INSERT INTO meta.metadata (schema_name, config)
            VALUES 
                ('{config['schema_name']}', 
                '{json.dumps(config)}'::jsonb);
        ''')