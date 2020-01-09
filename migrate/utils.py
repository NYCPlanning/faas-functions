from sqlalchemy import create_engine
import os
from osgeo import gdal
from urllib.parse import urlparse

def migrate_table(src_engine, dst_engine, 
                src_schema_name, dst_schema_name,
                src_version, dst_version):
    con = create_engine(dst_engine)

    src = parse_engine(src_engine)
    dst = parse_engine(dst_engine)
    srcDS = gdal.OpenEx(src, gdal.OF_VECTOR)
    dstDS = gdal.OpenEx(dst, gdal.OF_VECTOR)

    con.execute(f'CREATE SCHEMA IF NOT EXISTS {dst_schema_name}')
    print(f'Migrating {src_schema_name}."{src_version}" to {dst_schema_name}."{dst_version}" ...\n')

    gdal.VectorTranslate(
        dstDS,
        srcDS,
        SQLStatement=f'SELECT * FROM {src_schema_name}."{src_version}"',
        format='PostgreSQL',
        layerName=f'{dst_schema_name}.{dst_version}',
        accessMode='overwrite',
        callback=gdal.TermProgress)
    # except:
    #     print(f'Migrating {src_schema_name}."{src_version}" to {dst_schema_name}."{dst_version}" failed...\n')

def parse_engine(engine):
    result = urlparse(engine)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    portnum = result.port
    return f'PG:host={hostname} port={portnum} user={username} dbname={database} password={password}'
