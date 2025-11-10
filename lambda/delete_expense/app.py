# import os
# import json
# import boto3

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(os.environ['TABLE_NAME'])

# def handler(event, context):
#     # expenseId comes from path parameter
#     try:
#         expense_id = event['pathParameters']['expenseId']
#         table.delete_item(Key={'expenseId': expense_id})
#         return {"statusCode": 200, "body": json.dumps({"deleted": expense_id})}
#     except Exception as e:
#         print("Error:", e)
#         return {"statusCode":500, "body": json.dumps({"error": str(e)})}
import os
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    try:
        # Extract both path parameters
        user_id = event['pathParameters']['userId']
        expense_date = event['pathParameters']['expenseDate']

        print(f"🗑️ Deleting item for UserId={user_id}, ExpenseDate={expense_date}")

        # Delete using correct key schema
        response = table.delete_item(
            Key={
                'UserId': user_id,
                'ExpenseDate': expense_date
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Expense deleted successfully",
                "deletedKeys": {
                    "UserId": user_id,
                    "ExpenseDate": expense_date
                }
            })
        }

    except Exception as e:
        print("❌ Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
