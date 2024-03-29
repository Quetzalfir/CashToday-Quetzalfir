import os
import json
import boto3
from http import HTTPStatus

TABLE_NAME = os.environ.get('TABLE_NAME', 'DefaultTableName')  # Añadido valor por defecto para pruebas
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def check_user_exists(numero_identificacion):
    response = table.get_item(Key={'numeroIdentificacion': numero_identificacion})
    return 'Item' in response

def add_user(body):
    table.put_item(Item=body)

def lambda_handler(event, context):
    try:
        print(event)
        # Obtener el token del header
        token = event['headers'].get('Authorization')

        print(token)
        print(ACCESS_TOKEN)

        # Verificar si el token coincide
        if token != ACCESS_TOKEN:
            return {
                'statusCode': HTTPStatus.UNAUTHORIZED,
                'body': json.dumps({'message': 'Unauthorized'})
            }

        body = json.loads(event['body'])
        numero_identificacion = body['numeroIdentificacion']

        # Verificar si el usuario ya existe
        if check_user_exists(numero_identificacion):
            return {
                'statusCode': HTTPStatus.CONFLICT,
                'body': json.dumps({'message': 'User already exists.'})
            }

        # Registrar nuevo usuario
        add_user(body)
        return {
            'statusCode': HTTPStatus.CREATED,
            'body': json.dumps(body)
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
