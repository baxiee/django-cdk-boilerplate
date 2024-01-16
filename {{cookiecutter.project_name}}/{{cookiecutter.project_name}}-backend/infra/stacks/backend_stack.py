import aws_cdk as cdk
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_certificatemanager as certificatemanager
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as logs
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from constructs import Construct


class BackendStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        params: dict,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        account_id = params["account_id"]
        certificate_arn = params["certificate_arn"]
        domain = params["domain"]
        env = params["env"]
        credentials_secret = params["credentials_secret"]
        prefix = self.stack_name
        prereq = "prereq"
        project_name = params["project_name"]
        region = params["region"]

        rds_secret_name = cdk.Fn.import_value(
            shared_value_to_import=f"{project_name}-{env}-{prereq}-rds-secret-name"
        )
        static_bucket_name = cdk.Fn.import_value(
            shared_value_to_import=f"{project_name}-{env}-{prereq}-bucket-name"
        )

        lambda_policy_statements = self.create_lambda_policy_statements(
            region,
            account_id,
            credentials_secret,
            rds_secret_name,
            static_bucket_name,
        )
        handler = self.create_lambda(
            prefix,
            credentials_secret,
            lambda_policy_statements,
            rds_secret_name,
            static_bucket_name,
        )

        if domain and certificate_arn:
            self.create_api_gateway_with_domain(
                prefix, handler, domain, certificate_arn
            )
        else:
            self.create_api_gateway(prefix, handler)

    def create_lambda_policy_statements(
        self,
        region,
        account_id,
        credentials_secret,
        rds_secret_name,
        static_bucket_name,
    ):
        lambda_policy_statements = [
            iam.PolicyStatement(
                actions=["secretsmanager:*"],
                effect=iam.Effect.ALLOW,
                resources=[
                    (
                        f"arn:aws:secretsmanager:{region}:{account_id}:"
                        f"secret:{rds_secret_name}-*"
                    ),
                    (
                        f"arn:aws:secretsmanager:{region}:{account_id}:"
                        f"secret:{credentials_secret}-*"
                    ),
                ],
            ),
            iam.PolicyStatement(
                actions=["s3:*"],
                effect=iam.Effect.ALLOW,
                resources=[
                    f"arn:aws:s3:::{static_bucket_name}",
                    f"arn:aws:s3:::{static_bucket_name}/*",
                ],
            ),
        ]

        return lambda_policy_statements

    def create_lambda(
        self,
        prefix,
        credentials_secret,
        lambda_policy_statements,
        rds_secret_name,
        static_bucket_name,
    ):
        handler = _lambda.DockerImageFunction(
            self,
            f"{prefix}-lambda",
            function_name=f"{prefix}-lambda",
            code=_lambda.DockerImageCode.from_image_asset("./lambda"),
            environment=dict(
                CREDENTIALS_SECRET=credentials_secret,
                SETTINGS_PATH="settings.prod",
                POSTGRES_SECRET_NAME=rds_secret_name,
                STATIC_BUCKET_NAME=static_bucket_name,
            ),
            timeout=cdk.Duration.seconds(60),
            initial_policy=lambda_policy_statements,
            memory_size=3008,
            log_retention=logs.RetentionDays.ONE_DAY,
        )

        return handler

    def create_api_gateway(
        self,
        prefix: str,
        handler: _lambda.Function,
    ) -> None:
        base_api = apigateway.RestApi(
            self,
            f"{prefix}-rest-api",
            binary_media_types=["*/*"],
        )

        get_widgets_integration = apigateway.LambdaIntegration(handler)
        resource = base_api.root.add_resource("{proxy+}")
        resource.add_method(
            "ANY",
            get_widgets_integration,
        )

        cdk.CfnOutput(self, f"{prefix}-raw-url", value=base_api.url)

    def create_api_gateway_with_domain(
        self,
        prefix: str,
        handler: _lambda.Function,
        domain: str,
        certificate_arn: str,
    ) -> None:
        base_api = apigateway.RestApi(
            self,
            f"{prefix}-rest-api",
            binary_media_types=["*/*"],
            domain_name=apigateway.DomainNameOptions(
                certificate=certificatemanager.Certificate.from_certificate_arn(
                    self,
                    f"{prefix}-certificate",
                    certificate_arn=certificate_arn,
                ),
                domain_name=f"api.{domain}",
                endpoint_type=apigateway.EndpointType.EDGE,
            ),
        )

        get_widgets_integration = apigateway.LambdaIntegration(handler)
        resource = base_api.root.add_resource("{proxy+}")
        resource.add_method(
            "ANY",
            get_widgets_integration,
        )

        zone = route53.HostedZone.from_lookup(
            self, f"{prefix}-hosted-zone", domain_name=domain
        )
        route53.ARecord(
            self,
            f"{prefix}-dns-record",
            record_name="api",
            zone=zone,
            target=route53.RecordTarget.from_alias(
                route53_targets.ApiGateway(base_api)
            ),
        )

        cdk.CfnOutput(self, f"{prefix}-raw-url", value=base_api.url)
        cdk.CfnOutput(self, f"{prefix}-url", value=f"api.{domain}")
