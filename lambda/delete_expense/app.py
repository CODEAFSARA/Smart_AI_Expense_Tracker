import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    # expenseId comes from path parameter
    try:
        expense_id = event['pathParameters']['expenseId']
        table.delete_item(Key={'expenseId': expense_id})
        return {"statusCode": 200, "body": json.dumps({"deleted": expense_id})}
    except Exception as e:
        print("Error:", e)
        return {"statusCode":500, "body": json.dumps({"error": str(e)})}
