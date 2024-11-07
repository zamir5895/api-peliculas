import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Log de entrada
    print(json.dumps({"tipo": "INFO", "log_datos": {"evento": event}}))  # Log json de entrada en formato estándar
    
    # Variables
    nombre_tabla = os.environ["TABLE_NAME"]
    
    try:
        # Extracción de parámetros de entrada
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        
        # Generación de UUID
        uuidv4 = str(uuid.uuid4())
        
        # Construcción del elemento para DynamoDB
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        # Inserción en DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        
        # Log de éxito
        print(json.dumps({"tipo": "INFO", "log_datos": {"mensaje": "Pelicula creada exitosamente", "pelicula": pelicula}}))
        
        # Respuesta de éxito
        return {
            'statusCode': 200,
            'body': json.dumps({"pelicula": pelicula, "response": response})
        }
    
    except Exception as e:
        # Log de error
        error_log = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error al crear la película",
                "error": str(e)
            }
        }
        print(json.dumps(error_log))
        
        # Respuesta de error
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Internal server error", "detalles": str(e)})
        }
