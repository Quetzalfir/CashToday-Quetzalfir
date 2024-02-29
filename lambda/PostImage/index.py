import json
import boto3
import os
from http import HTTPStatus

s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        numero_identificacion = event['pathParameters']['numeroIdentificacion']
        image_data = event['body']
        image_key = f"{numero_identificacion}/{uuid.uuid4()}.jpg"

        # Subir la imagen al bucket de S3
        s3.put_object(Bucket=bucket_name, Key=image_key, Body=image_data)

        # Generar URL presignada para la imagen
        presigned_url = s3.generate_presigned_url('get_object',
                                                  Params={'Bucket': bucket_name, 'Key': image_key},
                                                  ExpiresIn=3600)

        # Actualizar el registro del usuario con la nueva URL de la imagen
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Clients')
        table.update_item(
            Key={'numeroIdentificacion': numero_identificacion},
            UpdateExpression='SET imageUrl = :url',
            ExpressionAttributeValues={':url': presigned_url},
            ReturnValues='UPDATED_NEW'
        )

        return {
            'statusCode': HTTPStatus.CREATED,
            'body': json.dumps({'imageUrl': presigned_url})
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
