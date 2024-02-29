from aws_cdk import aws_s3 as s3, Duration


class S3Stack:
    def __init__(self, stack, env_props: dict) -> None:

        # Define the S3 bucket
        self.bucket = s3.Bucket(
            stack, "UserImages", versioned=False,
            bucket_name=env_props['s3_bucket_name'],
            lifecycle_rules=[
                s3.LifecycleRule(
                    expiration=Duration.days(3),
                    id="AutoDeleteAfter3Days"
                )
            ]
        )
