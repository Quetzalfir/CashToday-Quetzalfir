import base64
import json
import uuid
import boto3
import os
from http import HTTPStatus

TABLE_NAME = os.environ['TABLE_NAME']
BUCKET_NAME = os.environ['BUCKET_NAME']
CLOUDFRONT_URL = os.environ['CLOUDFRONT_URL']
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
s3 = boto3.client('s3')

def upload_image_to_s3(bucket_name, image_key, image_data):
    s3.put_object(Bucket=bucket_name, Key=image_key, Body=image_data)

def update_dynamodb_record(table, numero_identificacion, cloudfront_image_url):
    table.update_item(
        Key={'numeroIdentificacion': numero_identificacion},
        UpdateExpression='SET imageUrl = :url',
        ExpressionAttributeValues={':url': cloudfront_image_url},
        ReturnValues='UPDATED_NEW'
    )

def lambda_handler(event, context):
    try:
        # Obtener el token del header
        token = event['headers'].get('Authorization')

        # Verificar si el token coincide
        if token != ACCESS_TOKEN:
            return {
                'statusCode': HTTPStatus.UNAUTHORIZED,
                'body': json.dumps({'message': 'Unauthorized'})
            }

        numero_identificacion = event['queryStringParameters']['numeroIdentificacion']
        image_key = f"{numero_identificacion}/{uuid.uuid4()}.jpg"

        if event.get('isBase64Encoded', False):
            image_data = base64.b64decode(event['body'])
        else:
            image_data = event['body'].encode()

        upload_image_to_s3(BUCKET_NAME, image_key, image_data)

        cloudfront_image_url = f"{CLOUDFRONT_URL}/{image_key}"

        update_dynamodb_record(table, numero_identificacion, cloudfront_image_url)

        return {
            'statusCode': HTTPStatus.CREATED,
            'body': json.dumps({'imageUrl': cloudfront_image_url})
        }

    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
