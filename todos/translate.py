import os
import json
import boto3


from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    translate = boto3.client(service_name='translate', region_name='es', use_ssl=True)

    
    result['Item']['text'] = translate.translate_text(Text=result['Item']['text'],  SourceLanguageCode="es", TargetLanguageCode=event['pathParameters']['language'])

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
