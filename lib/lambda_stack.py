from aws_cdk import aws_lambda as lambda_


class LambdaStack:

    def __init__(self, stack, database_stack, s3_stack, cloudfront_url, env_props: dict) -> None:

        # Define the Lambda functions
        self.user_register_lambda = lambda_.Function(
            stack, 'UserRegisterFunction',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('LambdaFunction/UserRegister'),
            handler='index.lambda_handler',
            environment={
                'TABLE_NAME': database_stack.table.table_name,
                'ACCESS_TOKEN': env_props['secret']
            }
        )

        self.user_search_lambda = lambda_.Function(
            stack, 'UserSearchFunction',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('LambdaFunction/UserSearch'),
            handler='index.lambda_handler',
            environment={
                'TABLE_NAME': database_stack.table.table_name,
                'ACCESS_TOKEN': env_props['secret']
            }
        )

        self.delete_user_lambda = lambda_.Function(
            stack, 'UserDeleteFunction',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('LambdaFunction/DeleteUser'),
            handler='index.lambda_handler',
            environment={
                'TABLE_NAME': database_stack.table.table_name,
                'ACCESS_TOKEN': env_props['secret']
            }
        )

        self.modify_user_lambda = lambda_.Function(
            stack, 'UserModifyFunction',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('LambdaFunction/ModifyUser'),
            handler='index.lambda_handler',
            environment={
                'TABLE_NAME': database_stack.table.table_name,
                'ACCESS_TOKEN': env_props['secret']
            }
        )

        self.post_image_lambda = lambda_.Function(
            stack, 'PostImageFunction',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('LambdaFunction/PostImage'),
            handler='index.lambda_handler',
            environment={
                'TABLE_NAME': database_stack.table.table_name,
                'BUCKET_NAME': s3_stack.bucket.bucket_name,
                'CLOUDFRONT_URL': cloudfront_url,
                'ACCESS_TOKEN': env_props['secret']
            }
        )

        # Grant the Lambda function the necessary permissions
        database_stack.table.grant_read_write_data(self.user_register_lambda)
        database_stack.table.grant_read_write_data(self.delete_user_lambda)
        database_stack.table.grant_read_write_data(self.modify_user_lambda)
        database_stack.table.grant_read_write_data(self.post_image_lambda)
        database_stack.table.grant_read_data(self.user_search_lambda)

        s3_stack.bucket.grant_put(self.post_image_lambda)
        s3_stack.bucket.grant_put(self.user_register_lambda)  # Grant permissions as necessary for other operations
