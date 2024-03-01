import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from http import HTTPStatus

TABLE_NAME = os.environ['TABLE_NAME']
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def search_in_dynamodb(search_key, search_value):
    if search_key == 'numeroIdentificacion':
        response = table.get_item(Key={'numeroIdentificacion': search_value})
    else:
        response = table.query(
            IndexName=search_key,
            KeyConditionExpression=Key(search_key).eq(search_value)
        )
    return response

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

        params = event['queryStringParameters']
        search_key = list(params.keys())[0]
        search_value = params[search_key]

        response = search_in_dynamodb(search_key, search_value)

        items = response.get('Items', []) if 'Items' in response else [response.get('Item')] if 'Item' in response else []
        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps(items)
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
