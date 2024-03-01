import json
import os
from http import HTTPStatus

from LambdaFunction.UserRegister.index import lambda_handler
import pytest
from moto import mock_dynamodb2
import boto3


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture
def dynamodb(aws_credentials):
    with mock_dynamodb2():
        yield boto3.client('dynamodb', region_name='us-east-1')


@pytest.fixture
def create_table(dynamodb):
    dynamodb.create_table(
        TableName='DefaultTableName',
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
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def test_lambda_handler_user_exists(create_table):
    event = {
        'body': json.dumps({'numeroIdentificacion': '123'})
    }
    context = {}
    # Pre-popula la tabla DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('DefaultTableName')
    table.put_item(Item={'numeroIdentificacion': '123'})

    response = lambda_handler(event, context)

    assert response['statusCode'] == HTTPStatus.CONFLICT
    assert json.loads(response['body'])['message'] == 'User already exists.'


def test_lambda_handler_add_user(create_table):
    event = {
        'body': json.dumps({'numeroIdentificacion': '456'})
    }
    context = {}

    response = lambda_handler(event, context)

    assert response['statusCode'] == HTTPStatus.CREATED
    assert json.loads(response['body'])['numeroIdentificacion'] == '456'
