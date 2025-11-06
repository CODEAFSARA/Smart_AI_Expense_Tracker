import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    # Optional query param userId to filter results
    try:
        params = event.get('queryStringParameters') or {}
        user_id = params.get('userId')

        if user_id:
            resp = table.scan(
                FilterExpression="userId = :u",
                ExpressionAttributeValues={":u": user_id}
            )
            items = resp.get('Items', [])
        else:
            resp = table.scan()
            items = resp.get('Items', [])

        return {"statusCode": 200, "body": json.dumps({"items": items})}
    except Exception as e:
        print("Error:", e)
        return {"statusCode":500, "body": json.dumps({"error": str(e)})}

    # Optional query param userId to filter results
    try:
        params = event.get('queryStringParameters') or {}
        user_id = params.get('userId')

        if user_id:
            resp = table.scan(
                FilterExpression="userId = :u",
                ExpressionAttributeValues={":u": user_id}
            )
            items = resp.get('Items', [])
        else:
            resp = table.scan()
            items = resp.get('Items', [])

        return {"statusCode": 200, "body": json.dumps({"items": items})}
    except Exception as e:
        print("Error:", e)
        return {"statusCode":500, "body": json.dumps({"error": str(e)})}
