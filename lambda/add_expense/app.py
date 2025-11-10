# import os
# import json
# import uuid
# import boto3
# from datetime import datetime

# # Initialize AWS resources
# dynamodb = boto3.resource('dynamodb')
# lambda_client = boto3.client('lambda')

# table_name = "ExpenseTrackerTable"
# table = dynamodb.Table(table_name)

# def handler(event, context):
#     """
#     Smart Expense Tracker — Add Expense Lambda
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
#         print("🧾 Incoming event:", event)

#         # Parse JSON body (handle string or dict)
#         body = event.get("body")
#         if isinstance(body, str):
#             body = json.loads(body)
#         elif isinstance(body, dict):
#             body = body
#         else:
#             raise ValueError("Invalid body format")

#         print("📦 Parsed body:", body)

#         # Validate required fields
#         required_fields = ["userId", "amount", "description"]
#         if not all(field in body for field in required_fields):
#             return {"statusCode": 400, "body": json.dumps({"error": "Missing required fields"})}

#         expense_id = str(uuid.uuid4())
#         date = body.get("date") or datetime.utcnow().strftime("%Y-%m-%d")

#         # 🧠 Invoke categorize_expense Lambda
#      # 🧠 Mock AI categorization locally (for testing)
#         description = body["description"].lower()

#         if any(word in description for word in ["food", "lunch", "dinner", "restaurant", "eat", "snack"]):
#             category = "Food"
#         elif any(word in description for word in ["bus", "train", "flight", "travel", "uber"]):
#             category = "Travel"
#         elif any(word in description for word in ["bill", "electricity", "rent", "internet"]):
#             category = "Bills"
#         else:
#             category = "Other"

#         # Prepare DynamoDB item
#         item = {
#             "expenseId": expense_id,
#             "userId": body["userId"],
#             "amount": str(body["amount"]),
#             "category": category,
#             "date": date,
#             "description": body["description"]
#         }

#         if "receiptKey" in body:
#             item["receiptKey"] = body["receiptKey"]

#         # Save to DynamoDB
#         print("🗄️ Mock save to DynamoDB:", item)
#         print("💾 Saved to DynamoDB")

#         return {
#             "statusCode": 201,
#             "body": json.dumps({
#                 "message": "Expense added successfully",
#                 "predictedCategory": category,
#                 "expenseId": expense_id
#             })
#         }

#     except Exception as e:
#         print("❌ Error:", e)
#         return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


# # For local testing
# if __name__ == "__main__":
#     test_event = {
#         "body": json.dumps({
#             "userId": "user123",
#             "amount": 250.0,
#             "description": "Lunch at Subway",
#             "date": "2025-11-07",
#             "receiptKey": "optional-s3-key"
#         })
#     }

#     # Set environment vars for local test
#     os.environ["TABLE_NAME"] = "SmartExpenseTable"
#     os.environ["CATEGORIZE_LAMBDA_NAME"] = "categorize_expense"

#     print("\n✅ Lambda result:", handler(test_event, None))
import os
import json
import uuid
import boto3
from datetime import datetime

# --- Initialize AWS Resources ---
dynamodb = boto3.resource("dynamodb")
lambda_client = boto3.client("lambda")

# --- Environment Variables ---
TABLE_NAME = os.environ.get("TABLE_NAME")
if not TABLE_NAME:
    raise ValueError("❌ Environment variable TABLE_NAME is missing")

table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    """
    Smart Expense Tracker — Add Expense Lambda

    Triggered via API Gateway (POST)
    Expected JSON body:
    {
      "userId": "user123",
      "amount": 250.0,
      "description": "Lunch at Subway",
      "date": "2025-11-07",     # optional
      "receiptKey": "optional-s3-key"
    }
    """

    try:
        print("🧾 Incoming event:", json.dumps(event))

        # --- Parse Body ----
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        elif not isinstance(body, dict):
            raise ValueError("Invalid body format")

        print("📦 Parsed body:", body)

        # --- Validate Required Fields ---
        required_fields = ["userId", "amount", "description"]
        missing = [f for f in required_fields if f not in body]
        if missing:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"Missing required fields: {', '.join(missing)}"})
            }

        # --- Generate IDs and Defaults ---
        expense_id = str(uuid.uuid4())
        expense_date = body.get("date") or datetime.utcnow().strftime("%Y-%m-%d")

        # --- Categorization Logic (mock AI, can replace with HuggingFace later) ---
        description_text = body["description"].lower()
        if any(word in description_text for word in ["food", "lunch", "dinner", "restaurant", "eat", "snack"]):
            category = "Food"
        elif any(word in description_text for word in ["bus", "train", "flight", "travel", "uber", "taxi"]):
            category = "Travel"
        elif any(word in description_text for word in ["bill", "electricity", "rent", "internet", "wifi"]):
            category = "Bills"
        else:
            category = "Other"

        # --- Prepare DynamoDB Item (match schema exactly) ---
        item = {
            "UserId": body["userId"],        # HASH key
            "ExpenseDate": expense_date,     # RANGE key
            "ExpenseId": expense_id,         # Unique identifier
            "Amount": str(body["amount"]),
            "Category": category,
            "Description": body["description"]
        }

        if "receiptKey" in body:
            item["ReceiptKey"] = body["receiptKey"]

        # --- Save to DynamoDB ---
        table.put_item(Item=item)
        print("💾 Saved to DynamoDB:", json.dumps(item))

        # --- Return Success ---
        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Expense added successfully",
                "predictedCategory": category,
                "expenseId": expense_id
            })
        }

    except Exception as e:
        print("❌ Error:", str(e))
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }


# --- Local Testing Block ---
if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "ExpenseTrackerTable"

    test_event = {
        "body": json.dumps({
            "userId": "user123",
            "amount": 250.0,
            "description": "Lunch at Subway",
            "date": "2025-11-07",
            "receiptKey": "optional-s3-key"
        })
    }

    result = handler(test_event, None)
    print("\n✅ Test Result:", json.dumps(result, indent=2))
