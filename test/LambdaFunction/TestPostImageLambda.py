import base64
import json
from http import HTTPStatus

import pytest
from moto import mock_dynamodb2, mock_s3
from LambdaFunction.PostImage.index import lambda_handler, upload_image_to_s3, update_dynamodb_record
import boto3
import os

# Configurar las variables de entorno para las pruebas
os.environ['TABLE_NAME'] = 'test-table'
os.environ['BUCKET_NAME'] = 'test-bucket'
os.environ['CLOUDFRONT_URL'] = 'https://test.cloudfront.net'


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def dynamodb(aws_credentials):
    with mock_dynamodb2():
        yield boto3.resource('dynamodb', region_name="us-east-1")


@pytest.fixture
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client('s3', region_name="us-east-1")


def test_upload_image_to_s3(s3):
    bucket = os.environ['BUCKET_NAME']
    s3.create_bucket(Bucket=bucket)
    image_key = "test.jpg"
    image_data = b'test data'
    upload_image_to_s3(bucket, image_key, image_data)

    obj = s3.get_object(Bucket=bucket, Key=image_key)
    assert obj['Body'].read() == image_data


def test_update_dynamodb_record(dynamodb):
    table = dynamodb.create_table(
        TableName=os.environ['TABLE_NAME'],
        KeySchema=[
            {
                'AttributeName': 'numeroIdentificacion',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'numeroIdentificacion',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )

    numero_identificacion = "123"
    cloudfront_image_url = "https://test.cloudfront.net/test.jpg"
    update_dynamodb_record(table, numero_identificacion, cloudfront_image_url)

    response = table.get_item(
        Key={'numeroIdentificacion': numero_identificacion}
    )
    assert 'Item' in response
    assert response['Item']['imageUrl'] == cloudfront_image_url


def test_lambda_handler(aws_credentials, dynamodb, s3):
    s3.create_bucket(Bucket=os.environ['BUCKET_NAME'])
    dynamodb.create_table(
        TableName=os.environ['TABLE_NAME'],
        KeySchema=[{'AttributeName': 'numeroIdentificacion', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'numeroIdentificacion', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    event = {
        'queryStringParameters': {'numeroIdentificacion': '123'},
        'body': base64.b64encode(b'test image data').decode('utf-8'),
        'isBase64Encoded': True
    }
    context = {}

    response = lambda_handler(event, context)

    assert response['statusCode'] == HTTPStatus.CREATED
    body = json.loads(response['body'])
    assert 'imageUrl' in body
    assert body['imageUrl'].startswith(os.environ['CLOUDFRONT_URL'])
