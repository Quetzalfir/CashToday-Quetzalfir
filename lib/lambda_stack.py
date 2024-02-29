from aws_cdk import aws_lambda as lambda_


class LambdaStack:

    def __init__(self, stack, database_stack, s3_stack) -> None:

        # Define the Lambda functions
        self.user_register_lambda = lambda_.Function(
            stack, 'UserRegisterFunction',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('lambda/UserRegister'),
            handler='index.lambda_handler',
            environment={
                'TABLE_NAME': database_stack.table.table_name
            }
        )

        self.user_search_lambda = lambda_.Function(
            stack, 'UserSearchFunction',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('lambda/UserSearch'),
            handler='index.lambda_handler',
            environment={
                'TABLE_NAME': database_stack.table.table_name
            }
        )

        self.delete_user_lambda = lambda_.Function(
            stack, 'UserDeleteFunction',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('lambda/DeleteUser'),
            handler='index.lambda_handler',
            environment={
                'TABLE_NAME': database_stack.table.table_name
            }
        )

        self.modify_user_lambda = lambda_.Function(
            stack, 'UserModifyFunction',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('lambda/ModifyUser'),
            handler='index.lambda_handler',
            environment={
                'TABLE_NAME': database_stack.table.table_name
            }
        )

        # Grant the Lambda function the necessary permissions
        database_stack.table.grant_read_write_data(self.user_register_lambda)
        database_stack.table.grant_read_write_data(self.delete_user_lambda)
        database_stack.table.grant_read_write_data(self.modify_user_lambda)
        database_stack.table.grant_read_data(self.user_search_lambda)

        s3_stack.bucket.grant_put(self.user_register_lambda)  # Grant permissions as necessary for other operations
