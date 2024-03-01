import json
import os
import boto3
from http import HTTPStatus

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
dynamodb = boto3.resource('dynamodb')

table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)


def delete_user(table, numero_identificacion):
    response = table.delete_item(Key={'numeroIdentificacion': numero_identificacion})
    return response


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
        print(numero_identificacion)

        # Eliminar usuario
        delete_user(table, numero_identificacion)

        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps({'message': 'User deleted successfully'})
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
