import os
import json
import uuid
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def handler(event, context):
    """
    Expected POST JSON body:
    {
      "userId": "user123",
      "amount": 250.0,
      "category": "food",
      "date": "2025-11-03",    # optional; fallback to today
      "description": "lunch",
      "receiptKey": "some-s3-key"   # optional (if used)
    }
    """
    try:
        body = json.loads(event.get('body') or "{}")
        expense_id = str(uuid.uuid4())
        date = body.get('date') or datetime.utcnow().strftime("%Y-%m-%d")

        # item = {
        #     'expenseId': expense_id,
        #     'userId': body['userId'],
        #     'amount': str(body['amount']),
        #     'category': body.get('category','uncategorized'),
        #     'date': date,
        #     'description': body.get('description',''),
        # }
        item = {
            'UserId': body['userId'],
            'ExpenseDate': date,
            'ExpenseId': expense_id,
            'Amount': str(body['amount']),
            'Category': body.get('category','uncategorized'),
            'Description': body.get('description',''),
        }

        if 'receiptKey' in body:
            item['receiptKey'] = body['receiptKey']

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps({"expenseId": expense_id})
        }
    except Exception as e:
        print("Error:", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
