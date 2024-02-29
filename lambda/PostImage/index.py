import json
import uuid
import boto3
import os
from http import HTTPStatus

TABLE_NAME = os.environ['TABLE_NAME']
BUCKET_NAME = os.environ['BUCKET_NAME']
CLOUDFRONT_URL = os.environ['CLOUDFRONT_URL']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        numero_identificacion = event['pathParameters']['numeroIdentificacion']
        image_data = event['body']
        image_key = f"{numero_identificacion}/{uuid.uuid4()}.jpg"

        # Subir la imagen al bucket de S3
        s3.put_object(Bucket=BUCKET_NAME, Key=image_key, Body=image_data)

        # Construir la URL de CloudFront para la imagen
        cloudfront_image_url = f"{CLOUDFRONT_URL}/{image_key}"

        # Actualizar el registro del usuario con la URL de CloudFront
        table.update_item(
            Key={'numeroIdentificacion': numero_identificacion},
            UpdateExpression='SET imageUrl = :url',
            ExpressionAttributeValues={':url': cloudfront_image_url},
            ReturnValues='UPDATED_NEW'
        )

        return {
            'statusCode': HTTPStatus.CREATED,
            'body': json.dumps({'imageUrl': cloudfront_image_url})
        }

    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
