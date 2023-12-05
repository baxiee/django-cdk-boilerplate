import os

import aws_cdk as cdk
from stacks.backend_stack import BackendStack

app = cdk.App()

env = app.node.try_get_context("env")
project_name = app.node.try_get_context("project_name")
stack_name = app.node.try_get_context("stack_name")

params = {
    "account_id": os.environ["CDK_DEFAULT_ACCOUNT"],
    "certificate_arn": app.node.try_get_context("certificate_arn"),
    "domain": app.node.try_get_context("domain"),
    "env": env,
    "credentials_secret": app.node.try_get_context("credentials_secret"),
    "project_name": project_name,
    "region": os.environ["CDK_DEFAULT_REGION"],
    "stack_name": stack_name,
}

if not params["env"]:
    raise ValueError("No env")


BackendStack(
    app,
    f"{project_name}-{env}-{stack_name}",
    params=params,
    env=cdk.Environment(account=params["account_id"], region=params["region"]),
    synthesizer=cdk.DefaultStackSynthesizer(
        image_assets_repository_name=app.node.try_get_context("assets-ecr-repository-name"),
    ),
)

app.synth()
