import io
import json
import os
import sys

import boto3


def set_credentials():
    client = boto3.client("secretsmanager")
    credentials = json.loads(
        client.get_secret_value(SecretId=os.environ["CREDENTIALS_SECRET"])["SecretString"]
    )
    for key, value in credentials.items():
        os.environ[key] = value


def handler(event, context):
    set_credentials()

    sys.path.insert(0, os.path.join(os.getcwd(), "backend"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")

    if "manage" in event:
        import django
        from django.core import management

        django.setup()
        output = io.StringIO()
        try:
            management.call_command(*event["manage"].split(" "), stdout=output, interactive=False)
        except:  # noqa: E722
            management.call_command(*event["manage"].split(" "), stdout=output)

        return {"output": output.getvalue()}

    else:
        import awsgi
        from backend.wsgi import application

        return awsgi.response(application, event, context)
