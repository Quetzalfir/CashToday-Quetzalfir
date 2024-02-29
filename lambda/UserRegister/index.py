import os
import json
import boto3
from http import HTTPStatus

# Utiliza la variable de entorno para obtener el nombre de la tabla
TABLE_NAME = os.environ['TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        numero_identificacion = body['numeroIdentificacion']

        print(body)
        print(numero_identificacion)

        # Verificar si el usuario ya existe
        response = table.get_item(Key={'numeroIdentificacion': numero_identificacion})
        print(response)
        if 'Item' in response:
            print("'Item' in response")
            return {
                'statusCode': HTTPStatus.CONFLICT,
                'body': json.dumps({'message': 'User already exists.'})
            }

        # Registrar nuevo usuario
        print("put_item attempt")
        table.put_item(Item=body)
        print("put_item passed")
        return {
            'statusCode': HTTPStatus.CREATED,
            'body': json.dumps(body)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
