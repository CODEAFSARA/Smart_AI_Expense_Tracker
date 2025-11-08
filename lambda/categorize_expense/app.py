# import os
# import json
# import requests

# HF_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
# HF_TOKEN = os.environ.get("HF_TOKEN")

# def lambda_handler(event, context):
#     try:
#         body = json.loads(event.get("body", "{}"))
#         description = body.get("description")
        
#         if not description:
#             return {
#                 "statusCode": 400,
#                 "body": json.dumps({"error": "Missing 'description' field"})
#             }

#         headers = {
#             "Authorization": f"Bearer {HF_TOKEN}",
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "inputs": description,
#             "parameters": {
#                 "candidate_labels": ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Health", "Other"]
#             }
#         }

#         response = requests.post(HF_MODEL_URL, headers=headers, json=payload)
#         response.raise_for_status()
#         data = response.json()

#         category = data.get("labels", ["Uncategorized"])[0]

#         return {
#             "statusCode": 200,
#             "body": json.dumps({
#                 "description": description,
#                 "category": category
#             })
#         }

#     except Exception as e:
#         return {
#             "statusCode": 500,
#             "body": json.dumps({"error": str(e)})
#         }
import os
import json
import requests

HF_MODEL_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
HF_TOKEN = os.environ.get("HF_TOKEN")

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        description = body.get("description")
        
        if not description:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'description' field"})
            }

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
        response.raise_for_status()
        data = response.json()

        # 🩵 CHANGE STARTS HERE ---------------------
        # Handle both list and dict responses from Hugging Face
        if isinstance(data, list) and len(data) > 0:
            data = data[0]

        labels = data.get("labels", ["Uncategorized"])
        category = labels[0] if labels else "Uncategorized"
        # 🩵 CHANGE ENDS HERE -----------------------

        return {
            "statusCode": 200,
            "body": json.dumps({
                "description": description,
                "category": category
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
