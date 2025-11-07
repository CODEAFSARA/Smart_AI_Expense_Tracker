# import os
# import json
# import uuid
# import boto3
# import requests
# from datetime import datetime

# dynamodb = boto3.resource('dynamodb')
# table_name = os.environ.get('TABLE_NAME')
# table = dynamodb.Table(table_name)

# HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
# HF_TOKEN = os.environ.get('HF_TOKEN')

# def categorize_expense(description):
#     """Use Hugging Face API to predict expense category"""
#     headers = {
#         "Authorization": f"Bearer {HF_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     #
#     payload = {
#         "inputs": description,
#         "parameters": {
#             "candidate_labels": ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Health", "Other"]
#         }
#     }

#     response = requests.post(HF_MODEL_URL, headers=headers, json=payload)
#     response.raise_for_status()
#     data = response.json()
#     return data.get("labels", ["Uncategorized"])[0]

# def handler(event, context):
#     """
#     Smart Expense Tracker — AI Categorization
#     Expected POST JSON body:
#     {
#       "userId": "user123",
#       "amount": 250.0,
#       "description": "Lunch at Subway",
#       "date": "2025-11-07",   # optional
#       "receiptKey": "optional-s3-key"
#     }
#     """
#     try:
#         body = json.loads(event.get('body') or "{}")

#         # Validate required fields
#         if not all(k in body for k in ['userId', 'amount', 'description']):
#             return {"statusCode": 400, "body": json.dumps({"error": "Missing required fields"})}

#         expense_id = str(uuid.uuid4())
#         date = body.get('date') or datetime.utcnow().strftime("%Y-%m-%d")

#         # 🧠 AI categorization
#         category = categorize_expense(body['description'])

#         # Prepare item
#         item = {
#             'expenseId': expense_id,
#             'userId': body['userId'],
#             'amount': str(body['amount']),
#             'category': category,
#             'date': date,
#             'description': body['description']
#         }

#         if 'receiptKey' in body:
#             item['receiptKey'] = body['receiptKey']

#         # Store in DynamoDB
#         table.put_item(Item=item)

#         return {
#             "statusCode": 201,
#             "body": json.dumps({
#                 "message": "Expense added successfully",
#                 "predictedCategory": category,
#                 "expenseId": expense_id
#             })
#         }

#     except Exception as e:
#         print("Error:", e)
#         return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
import os
import json
import uuid
import boto3
import requests
from datetime import datetime

# Initialize AWS DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

# Hugging Face model and token
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
HF_TOKEN = os.environ.get('HF_TOKEN')

def categorize_expense(description):
    """Use Hugging Face API (new router) to predict expense category"""
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN is missing from environment variables")

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": description,
        "parameters": {
            "candidate_labels": ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Health", "Other"]
        }
    }

    response = requests.post(HF_MODEL_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")

    data = response.json()
    # Extract the best predicted label
    return data.get("labels", ["Uncategorized"])[0]


def handler(event, context):
    """
    Smart Expense Tracker — AI Categorization
    Expected POST JSON body:
    {
      "userId": "user123",
      "amount": 250.0,
      "description": "Lunch at Subway",
      "date": "2025-11-07",   # optional
      "receiptKey": "optional-s3-key"
    }
    """
    try:
        body = json.loads(event.get('body') or "{}")

        # Validate required fields
        if not all(k in body for k in ['userId', 'amount', 'description']):
            return {"statusCode": 400, "body": json.dumps({"error": "Missing required fields"})}

        expense_id = str(uuid.uuid4())
        date = body.get('date') or datetime.utcnow().strftime("%Y-%m-%d")

        # 🧠 AI categorization using Hugging Face
        category = categorize_expense(body['description'])

        # Prepare item for DynamoDB
        item = {
            'expenseId': expense_id,
            'userId': body['userId'],
            'amount': str(body['amount']),
            'category': category,
            'date': date,
            'description': body['description']
        }

        if 'receiptKey' in body:
            item['receiptKey'] = body['receiptKey']

        # Store in DynamoDB
        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Expense added successfully",
                "predictedCategory": category,
                "expenseId": expense_id
            })
        }

    except Exception as e:
        print("Error:", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
