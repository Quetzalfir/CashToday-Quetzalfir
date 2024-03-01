import json
import os
from http import HTTPStatus
import boto3
from LambdaFunction.UserSearch.index import lambda_handler, dynamodb
import pytest
from moto import mock_dynamodb2


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['TABLE_NAME'] = 'test-table'


@pytest.fixture(scope='function')
def dynamodb_mock(aws_credentials):
    with mock_dynamodb2():
        yield boto3.client('dynamodb', region_name='us-west-2')


@pytest.fixture(scope='function')
def create_table(dynamodb_mock):
    dynamodb_mock.create_table(
        TableName=os.environ['TABLE_NAME'],
        KeySchema=[
            {'AttributeName': 'numeroIdentificacion', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'numeroIdentificacion', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )


def test_lambda_handler_search_by_id(create_table):
    event = {
        'queryStringParameters': {'numeroIdentificacion': '123'}
    }
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == HTTPStatus.OK
    assert json.loads(response['body']) == []
