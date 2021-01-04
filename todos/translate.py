import os
import json


from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
clienttx = boto3.client('translate') 
comprehend = boto3.client('comprehend')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Recuperamos el elemento a traducir de la base de datos
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    #recuperamos el idioma que queremos usar para traducir
    target_language = event['pathParameters']['language']
    
    
    # Y llamamos a la funcion que nos va a traducir el texto de la etiqueta Todo al idioma seleccionado
    resultTx = clienttx.translate_text(Text=result['Item']['text'], SourceLanguageCode="auto", TargetLanguageCode=target_language)
    
    #Ahora actualizamos el resultado con el texto traducido
    result['Item']['text'] = resultTx["TranslatedText"] 

    # cY devolvemos el item ya traducido
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                          cls=decimalencoder.DecimalEncoder)
    }

    return response
