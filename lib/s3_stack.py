from aws_cdk import aws_s3 as s3, Duration, RemovalPolicy
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_iam as iam


class S3Stack:
    def __init__(self, stack, env_props: dict) -> None:

        # Obtener el valor del ambiente del contexto
        env = stack.node.try_get_context('env')

        # Define the S3 bucket
        self.bucket = s3.Bucket(
            stack, "UserImages", versioned=False,
            bucket_name=env_props['s3_bucket_name'],
            removal_policy=RemovalPolicy.DESTROY if env != 'prod' else RemovalPolicy.RETAIN,
            lifecycle_rules=[
                s3.LifecycleRule(
                    expiration=Duration.days(3),
                    id="AutoDeleteAfter3Days"
                )
            ]
        )

        # Crear una OAI para el bucket de S3 y darle acceso a CloudFront
        oai = cloudfront.OriginAccessIdentity(stack, "OAI", comment=f"OAI for {env_props['s3_bucket_name']}")

        # Asignar la política del bucket para permitir el acceso de CloudFront
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[self.bucket.arn_for_objects("*")],
                principals=[oai.grant_principal]
            )
        )

        # Crear la distribución de CloudFront para el bucket de S3
        self.distribution = cloudfront.Distribution(stack, f"Distribution-{env_props['s3_bucket_name']}",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(self.bucket, origin_access_identity=oai),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
                )
            )

        self.cloudfront_url = f"https://{self.distribution.distribution_domain_name}"
