import json
import os
import boto3
from http import HTTPStatus

TABLE_NAME = os.environ['TABLE_NAME']
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)


def update_user(numero_identificacion, updates):
    update_expression = []
    expression_attribute_values = {}
    for key, value in updates.items():
        update_expression.append(f"{key} = :{key}")
        expression_attribute_values[f":{key}"] = value

    response = table.update_item(
        Key={'numeroIdentificacion': numero_identificacion},
        UpdateExpression='SET ' + ', '.join(update_expression),
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='UPDATED_NEW'
    )

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

        body = json.loads(event['body'])
        numero_identificacion = event['queryStringParameters']['numeroIdentificacion']

        response = update_user(numero_identificacion, body)

        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps(response['Attributes'])
        }
    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
