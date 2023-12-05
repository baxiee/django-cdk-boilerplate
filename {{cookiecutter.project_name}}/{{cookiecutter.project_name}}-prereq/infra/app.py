import os

import aws_cdk as cdk
from stacks.prereq_stack import PrereqStack

app = cdk.App()

env = app.node.try_get_context("env")
project_name = app.node.try_get_context("project_name")
stack_name = app.node.try_get_context("stack_name")

params = {
    "account_id": os.environ["CDK_DEFAULT_ACCOUNT"],
    "env": env,
    "region": os.environ["CDK_DEFAULT_REGION"],
    "stack_name": stack_name,
    "project_name": project_name,
}

if not params["env"]:
    raise ValueError("No env")

PrereqStack(
    app,
    f"{project_name}-{env}-{stack_name}",
    params=params,
    env=cdk.Environment(account=params["account_id"], region=params["region"]),
)

app.synth()
