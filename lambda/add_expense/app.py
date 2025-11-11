
# import os
# import json
# import uuid
# import boto3
# from datetime import datetime

# # --- Initialize AWS Resources ---
# dynamodb = boto3.resource("dynamodb")
# lambda_client = boto3.client("lambda")

# # --- Environment Variables ---
# TABLE_NAME = os.environ.get("TABLE_NAME")
# if not TABLE_NAME:
#     raise ValueError("❌ Environment variable TABLE_NAME is missing")

# table = dynamodb.Table(TABLE_NAME)


# def handler(event, context):
#     """
#     Smart Expense Tracker — Add Expense Lambda

#     Triggered via API Gateway (POST)
#     Expected JSON body:
#     {
#       "userId": "user123",
#       "amount": 250.0,
#       "description": "Lunch at Subway",
#       "date": "2025-11-07",     # optional
#       "receiptKey": "optional-s3-key"
#     }
#     """

#     try:
#         print("🧾 Incoming event:", json.dumps(event))

#         # --- Parse Body ----
#         body = event.get("body")
#         if isinstance(body, str):
#             body = json.loads(body)
#         elif not isinstance(body, dict):
#             raise ValueError("Invalid body format")

#         print("📦 Parsed body:", body)

#         # --- Validate Required Fields ---
#         required_fields = ["userId", "amount", "description"]
#         missing = [f for f in required_fields if f not in body]
#         if missing:
#             return {
#                 "statusCode": 400,
#                 "headers": {"Content-Type": "application/json"},
#                 "body": json.dumps({"error": f"Missing required fields: {', '.join(missing)}"})
#             }

#         # --- Generate IDs and Defaults ---
#         expense_id = str(uuid.uuid4())
#         expense_date = body.get("date") or datetime.utcnow().strftime("%Y-%m-%d")

#         # --- Categorization Logic (mock AI, can replace with HuggingFace later) ---
#         description_text = body["description"].lower()
#         if any(word in description_text for word in ["food", "lunch", "dinner", "restaurant", "eat", "snack"]):
#             category = "Food"
#         elif any(word in description_text for word in ["bus", "train", "flight", "travel", "uber", "taxi"]):
#             category = "Travel"
#         elif any(word in description_text for word in ["bill", "electricity", "rent", "internet", "wifi"]):
#             category = "Bills"
#         else:
#             category = "Other"

#         # --- Prepare DynamoDB Item (match schema exactly) ---
#         item = {
#             "UserId": body["userId"],        # HASH key
#             "ExpenseDate": expense_date,     # RANGE key
#             "ExpenseId": expense_id,         # Unique identifier
#             "Amount": str(body["amount"]),
#             "Category": category,
#             "Description": body["description"]
#         }

#         if "receiptKey" in body:
#             item["ReceiptKey"] = body["receiptKey"]

#         # --- Save to DynamoDB ---
#         table.put_item(Item=item)
#         print("💾 Saved to DynamoDB:", json.dumps(item))

#         # --- Return Success ---
#         return {
#             "statusCode": 201,
#             "headers": {"Content-Type": "application/json"},
#             "body": json.dumps({
#                 "message": "Expense added successfully",
#                 "predictedCategory": category,
#                 "expenseId": expense_id
#             })
#         }

#     except Exception as e:
#         print("❌ Error:", str(e))
#         return {
#             "statusCode": 500,
#             "headers": {"Content-Type": "application/json"},
#             "body": json.dumps({"error": str(e)})
#         }


# # --- Local Testing Block ---
# if __name__ == "__main__":
#     os.environ["TABLE_NAME"] = "ExpenseTrackerTable"

#     test_event = {
#         "body": json.dumps({
#             "userId": "user123",
#             "amount": 250.0,
#             "description": "Lunch at Subway",
#             "date": "2025-11-07",
#             "receiptKey": "optional-s3-key"
#         })
#     }

#     result = handler(test_event, None)
#     print("\n✅ Test Result:", json.dumps(result, indent=2))
# --- Categorization Logic using Hugging Face Lambda ---
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
CATEGORIZE_LAMBDA_NAME = os.environ.get("CATEGORIZE_LAMBDA_NAME")
if not CATEGORIZE_LAMBDA_NAME:
    raise ValueError("❌ Environment variable 'CATEGORIZE_LAMBDA_NAME' is missing.")

def get_category_from_ai(description):
    """
    Invoke the CategorizeExpense Lambda to get AI-based category prediction.
    """
    try:
        payload = {"description": description}

        response = lambda_client.invoke(
            FunctionName=CATEGORIZE_LAMBDA_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps(payload)
        )

        result = json.loads(response["Payload"].read().decode("utf-8"))

        if "body" in result:
            try:
                body = json.loads(result["body"])
                category = body.get("category") or body.get("predictedCategory") or "Uncategorized"
                return category
            except Exception:
                print("⚠️ Could not parse Categorize Lambda response body:", result)
                return "Uncategorized"
        else:
            print("⚠️ Unexpected response from Categorize Lambda:", result)
            return "Uncategorized"

    except Exception as e:
        print(f"❌ Error invoking Categorize Lambda: {e}")
        return "Uncategorized"


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

        # --- Categorize Expense using Hugging Face AI ---
        category = get_category_from_ai(body["description"])
        print("🧠 AI Predicted Category:", category)

        # --- Prepare DynamoDB Item ---
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
    os.environ["CATEGORIZE_LAMBDA_NAME"] = "CategorizeExpenseLambda"

    test_event = {
        "body": json.dumps({
            "userId": "user123",
            "amount": 250.0,
            "description": "Dinner at Subway",
            "date": "2025-11-07",
            "receiptKey": "optional-s3-key"
        })
    }

    result = handler(test_event, None)
    print("\n✅ Test Result:", json.dumps(result, indent=2))
