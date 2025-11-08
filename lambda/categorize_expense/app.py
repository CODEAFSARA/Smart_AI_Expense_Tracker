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

HF_TOKEN = os.environ.get("HF_TOKEN")
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

def categorize_expense(description):
    """Categorize text using Hugging Face model with dynamic response handling."""
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN not found. Please set it in env or in code.")

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
#
    payload = {
        "inputs": description,
        "parameters": {
            "candidate_labels": ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Health", "Other"]
        }
    }
#
    response = requests.post(HF_MODEL_URL, headers=headers, json=payload)
    print("🔍 Status code:", response.status_code)
    print("🔍 Raw response text:", response.text[:400])

    if response.status_code != 200:
        raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")

    data = response.json()

    # 🧠 Handle multiple possible formats
    if isinstance(data, list):
        # Your current case — list of label-score pairs
        if len(data) > 0 and isinstance(data[0], dict) and "label" in data[0]:
            return data[0]["label"]
        else:
            return "Uncategorized"

    elif isinstance(data, dict):
        # Standard response structure
        labels = data.get("labels", [])
        if labels:
            return labels[0]

    return "Uncategorized"


# 🧪 Local test
if __name__ == "__main__":
    test_description = "Lunch at Subway"
    category = categorize_expense(test_description)
    print(f"\n✅ '{test_description}' categorized as: {category}")
