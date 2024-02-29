import json
import os

import boto3
from http import HTTPStatus

TABLE_NAME = os.environ['TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        numero_identificacion = event['queryStringParameters']['numeroIdentificacion']
        print(numero_identificacion)

        # Eliminar usuario
        table.delete_item(Key={'numeroIdentificacion': numero_identificacion})

        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps({'message': 'User deleted successfully'})
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
