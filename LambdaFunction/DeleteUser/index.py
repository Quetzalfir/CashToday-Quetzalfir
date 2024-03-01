import json
import os
import boto3
from http import HTTPStatus

dynamodb = boto3.resource('dynamodb')


def delete_user(table, numero_identificacion):
    response = table.delete_item(Key={'numeroIdentificacion': numero_identificacion})
    return response


def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    table = dynamodb.Table(table_name)

    try:
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
