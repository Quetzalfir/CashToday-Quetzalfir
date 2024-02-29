from lib.apigateway_stack import ApiGatewayStack
from lib.database_stack import DatabaseStack
from lib.lambda_stack import LambdaStack
from lib.s3_stack import S3Stack
from aws_cdk import Stack
from aws_cdk import App

app = App()
env = app.node.try_get_context('env')

if env == 'prod':
    env_props = {
        'dynamodb_table_name': 'CashToday-Clients-Prod',
        's3_bucket_name': 'cashtoday-user-images-prod'
    }
elif env == 'uat':
    env_props = {
        'dynamodb_table_name': 'CashToday-Clients-UAT',
        's3_bucket_name': 'cashtoday-user-images-uat'
    }
else:  # Default to dev
    env_props = {
        'dynamodb_table_name': 'CashToday-Clients-Dev',
        's3_bucket_name': 'cashtoday-user-images-dev'
    }

stack = Stack(app, f"CashTodayStack-{env.capitalize()}")

database_stack = DatabaseStack(stack, env_props)
s3_stack = S3Stack(stack, env_props)
lambda_stack = LambdaStack(stack, database_stack, s3_stack, s3_stack.distribution.distribution_domain_name)
apigateway_stack = ApiGatewayStack(stack, lambda_stack)

app.synth()
