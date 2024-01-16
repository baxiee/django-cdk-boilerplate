import io
import json
import os
import sys

import awsgi
import boto3
import django

sys.path.insert(0, os.path.join(os.getcwd(), "backend"))


def load_app_credentials():
    client = boto3.client("secretsmanager")
    credentials = json.loads(
        client.get_secret_value(SecretId=os.environ["CREDENTIALS_SECRET"])[
            "SecretString"
        ]
    )
    for key, value in credentials.items():
        os.environ[key] = value


def load_rds_credentials():
    client = boto3.client("secretsmanager")
    credentials = json.loads(
        client.get_secret_value(SecretId=os.environ["POSTGRES_SECRET_NAME"])[
            "SecretString"
        ]
    )
    for key, value in credentials.items():
        os.environ[f"RDS_{key.upper()}"] = str(value)


def load_environment_variables():
    load_app_credentials()
    load_rds_credentials()


load_environment_variables()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")

from backend.wsgi import application  # noqa

django.setup()


# Everything above runs only once on cold start
# so it is good to keep handler as small as possible
def handler(event, context):
    if "manage" in event:
        from django.core import management

        output = io.StringIO()
        try:
            management.call_command(
                *event["manage"].split(" "), stdout=output, interactive=False
            )
        except:  # noqa: E722
            management.call_command(*event["manage"].split(" "), stdout=output)

        return {"output": output.getvalue()}

    else:
        return awsgi.response(application, event, context)
