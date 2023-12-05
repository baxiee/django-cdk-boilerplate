import json

import boto3


def get_secret(secret_id, region=None):
    secretsmanager = boto3.client("secretsmanager", region_name=region)

    response = secretsmanager.get_secret_value(SecretId=secret_id)

    return json.loads(response["SecretString"])


def get_db_connection_params(secret_variables):
    """Returns django db settings."""
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": secret_variables.get("dbname", "postgres"),
        "USER": secret_variables["username"],
        "HOST": secret_variables["host"],
        "PASSWORD": secret_variables["password"],
        "PORT": secret_variables["port"],
        "OPTIONS": {"connect_timeout": 60},
    }
