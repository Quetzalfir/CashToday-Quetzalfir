import json
import os
import boto3
from http import HTTPStatus

TABLE_NAME = os.environ['TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        numero_identificacion = event['queryStringParameters']['numeroIdentificacion']
        print(numero_identificacion)

        # Construir la expresión de actualización dinámicamente
        update_expression = []
        expression_attribute_values = {}
        for key, value in body.items():
            update_expression.append(f"{key} = :{key}")
            expression_attribute_values[f":{key}"] = value

        print(update_expression)
        print(expression_attribute_values)

        # Actualizar datos del usuario
        response = table.update_item(
            Key={'numeroIdentificacion': numero_identificacion},
            UpdateExpression='SET ' + ', '.join(update_expression),
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='UPDATED_NEW'
        )

        print(response)

        return {
            'statusCode': HTTPStatus.OK,
            'body': json.dumps(response['Attributes'])
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': str(e)})
        }
