import os
from http import HTTPStatus
from unittest import TestCase, mock
from LambdaFunction.DeleteUser.index import lambda_handler
from moto import mock_dynamodb2


class TestDeleteUserLambda(TestCase):

    @mock_dynamodb2
    def test_delete_user_success(self):
        from moto import mock_dynamodb2
        import boto3

        mock_dynamodb2().start()

        os.environ['TABLE_NAME'] = 'TestTable'
        table_name = os.environ['TABLE_NAME']

        # Crea una tabla mock
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'numeroIdentificacion',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'numeroIdentificacion',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

        event = {
            'queryStringParameters': {
                'numeroIdentificacion': '123'
            }
        }
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], HTTPStatus.OK)
        self.assertIn('User deleted successfully', response['body'])

        mock_dynamodb2().stop()

    @mock.patch('my_lambda_function.table.delete_item', side_effect=Exception('Error'))
    def test_delete_user_failure(self, mock_delete_item):
        event = {
            'queryStringParameters': {
                'numeroIdentificacion': '123'
            }
        }
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], HTTPStatus.INTERNAL_SERVER_ERROR)
