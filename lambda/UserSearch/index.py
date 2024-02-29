import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from http import HTTPStatus

TABLE_NAME = os.environ['TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        params = event['queryStringParameters']
        search_key = list(params.keys())[0]
        search_value = params[search_key]

        print(params)
        print(search_key)
        print(search_value)

        # Realizar la búsqueda en DynamoDB usando GSI si es necesario
        if search_key == 'numeroIdentificacion':
            print("Found by id")
            response = table.get_item(Key={'numeroIdentificacion': search_value})
        else:
            print("Not Found by id")
            print(Key(search_key).eq(search_value))
            response = table.query(
                IndexName=search_key,
                KeyConditionExpression=Key(search_key).eq(search_value)
            )

        print(response)

        items = response.get('Item', [])
        print("items")
        print(items)
        print(json.dumps(items))

        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps(items)
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
