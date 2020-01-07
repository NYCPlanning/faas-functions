from flask import jsonify
import json
import boto3


with open("/var/openfaas/secrets/s3-endpoint-url","r") as secret: 
        endpoint_url = secret.read()
with open("/var/openfaas/secrets/s3-access-key-id","r") as secret: 
        aws_access_key_id = secret.read()
with open("/var/openfaas/secrets/s3-secret-access-key","r") as secret: 
        aws_secret_access_key = secret.read()
with open("/var/openfaas/secrets/s3-bucket","r") as secret: 
        bucket = secret.read()

def make_client():
    session = boto3.session.Session()
    client = session.client('s3',
                                region_name='S3_REGION',
                                endpoint_url=endpoint_url,
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
    return client

client = make_client()

def handle(event, context):
        file = event.files['file']
        config = event.form
        key = config.get('key')
        acl = config.get('acl', 'private')
        x = client.put_object(ACL=acl, Body=file.read(), Bucket=bucket, Key=key)
        if acl == 'public-read':
                return {'statusCode': 200,
                        'body': {
                                'response': x,
                                'url': f'https://{bucket}.{endpoint_url.replace("https://", "")}/{key}'
                                }
                        }
        else: 
                return {'statusCode': 200,
                        'body': {
                                'response': x,
                                'url': ''
                                }
                        }