import json

import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from aws_cdk import aws_rds as rds
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_secretsmanager as secretsmanager
from constructs import Construct


class PrereqStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        params: dict,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        prefix = self.stack_name

        self.create_rds(prefix)
        self.create_bucket(prefix)
        self.create_ecr(prefix)

    def create_bucket(self, prefix: str) -> None:
        bucket = s3.Bucket(
            self,
            f"{prefix}-bucket",
            bucket_name=f"{prefix}-bucket",
            versioned=False,
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_policy=False,
                block_public_acls=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
        )

        cdk.CfnOutput(
            self,
            f"{prefix}-bucket-name",
            export_name=f"{prefix}-bucket-name",
            value=bucket.bucket_name,
        )

    def create_ecr(self, prefix: str) -> None:
        repo = ecr.Repository(
            self,
            f"{prefix}-backend-repository",
            repository_name=f"{prefix}-backend-repository",
            lifecycle_rules=[
                ecr.LifecycleRule(
                    description="Removal of images older than latest 2 versions.",
                    max_image_count=2,
                )
            ],
        )
        repo.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["*"],
                effect=iam.Effect.ALLOW,
                principals=[iam.AnyPrincipal()],
            )
        )

    def create_rds(self, prefix: str) -> None:
        rds_secret = secretsmanager.Secret(
            self,
            f"{prefix}-rds-credentials",
            secret_name=f"{prefix}-rds-credentials",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "postgres"}),
                exclude_punctuation=True,
                include_space=False,
                generate_string_key="password",
            ),
        )
        credentials = rds.Credentials.from_secret(rds_secret)
        vpc = ec2.Vpc.from_lookup(self, f"{prefix}-rds-vpc", is_default=True)
        rds_security_group = ec2.SecurityGroup(
            self,
            f"{prefix}-rds-sg",
            security_group_name=f"{prefix}-rds-sg",
            vpc=vpc,
        )
        rds_instance = rds.DatabaseInstance(
            self,
            f"{prefix}-rds-instance",
            instance_identifier=f"{prefix}-rds-instance",
            database_name=prefix.replace("-", ""),
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_13_11
            ),
            instance_type=ec2.InstanceType("t3.micro"),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            storage_type=rds.StorageType.GP2,
            deletion_protection=True,
            port=5432,
            credentials=credentials,
            security_groups=[rds_security_group],
            publicly_accessible=True,
            allocated_storage=20,
            cloudwatch_logs_retention=logs.RetentionDays.ONE_DAY,
        )
        rds_instance.connections.allow_default_port_from_any_ipv4()
        rds_instance.connections.allow_default_port_internally()

        cdk.CfnOutput(
            self,
            f"{prefix}-rds-secret-name",
            export_name=f"{prefix}-rds-secret-name",
            value=rds_secret.secret_name,
        )
        cdk.CfnOutput(
            self,
            f"{prefix}-rds-name",
            export_name=f"{prefix}-rds-name",
            value=rds_instance.instance_identifier,
        )
