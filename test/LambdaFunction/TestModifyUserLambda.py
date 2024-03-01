import os
import pytest
from moto import mock_dynamodb2
import boto3
from LambdaFunction.ModifyUser.index import update_user


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
        yield boto3.resource('dynamodb', region_name='us-east-1')


def test_update_user(dynamodb):
    table_name = "TestTable"
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'numeroIdentificacion', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'numeroIdentificacion', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    os.environ['TABLE_NAME'] = table_name  # Asegurarse de que la función use esta tabla
    response = update_user("123", {"nombre": "Test User"})

    assert response['Attributes']['nombre'] == "Test User"
