# Faas-Functions

## Description:
Opensource serverless platform --> [Openfaas](https://www.openfaas.com/)

## Endpoints: 
+ /archive
    ```json
    POST {
            "dstSRS": "EPSG:4326",
            "srcSRS": "EPSG:2263",
            "schema_name": "dcp_mih",
            "version_name": "2019/11/14",
            "geometryType": "MULTIPOLYGON",
            "layerCreationOptions": [
                "OVERWRITE=YES",
                "PRECISION=NO"
            ],
            "metaInfo": "s3",
            "path": "https://edm-storage.nyc3.digitaloceanspaces.com/MANDATORY_INCLUSIONARY_HOUSING/20191114/mandatory_inclusionary_housing.zip",
            "srcOpenOptions": [],
            "newFieldNames": []
        }
    ```
+ /import
    ```json
    POST {
        "connection" : {
            "build_engine": "postgresql://XXXXXXXX"
        }, 
        "config" : {
            "schema_name" : "dcp_mih", 
            "version" : "latest"
        }
    }
    ```
+ /upload
    + posts file to digitalocean spaces

+ /recipes
    + `/api/<schema_name>` : retrieve record level info
    + `/api` : retrieve all info
    + `/schema_names` : retrieve all recipe schema names