
# import os
# import json
# import requests

# HF_TOKEN = os.environ.get("HF_TOKEN")
# HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"


# def categorize_expense(description):
#     """Use Hugging Face API (new router) to predict expense category"""
#     if not HF_TOKEN:
#         raise ValueError("HF_TOKEN is missing from environment variables")

#     headers = {
#         "Authorization": f"Bearer {HF_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "inputs": description,
#         "parameters": {
#             "candidate_labels": ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Health", "Other"]
#         }
#     }

#     response = requests.post(HF_MODEL_URL, headers=headers, json=payload)
#     if response.status_code != 200:
#         raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")

#     data = response.json()

#     # ✅ Handle both dict or list response types
#     if isinstance(data, list) and len(data) > 0 and "label" in data[0]:
#         return data[0]["label"]  # e.g., "Food"
#     elif isinstance(data, dict) and "labels" in data:
#         return data["labels"][0]
#     else:
#         print("⚠️ Unexpected response format:", data)
#         return "Uncategorized"


# def handler(event, context):
#     """Lambda entry point"""
#     try:
#         body = json.loads(event.get("body", "{}")) if isinstance(event.get("body"), str) else event
#         description = body.get("description", "")

#         if not description:
#             return {
#                 "statusCode": 400,
#                 "body": json.dumps({"error": "Missing expense description"})
#             }

#         category = categorize_expense(description)

#         return {
#             "statusCode": 200,
#             "body": json.dumps({"category": category})
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
    """Use Hugging Face API (router) to predict expense category."""
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
    print("🔍 HF response:", data)  # helpful for CloudWatch

    # ✅ Robust parsing for all known response formats
    if isinstance(data, dict):
        # New router format
        if "labels" in data and "scores" in data:
            labels = data["labels"]
            scores = data["scores"]
            if labels and scores:
                top_label = labels[scores.index(max(scores))]
                return top_label
        # Old format inside "result"
        elif "result" in data and "labels" in data["result"]:
            return data["result"]["labels"][0]

    elif isinstance(data, list) and len(data) > 0:
        # Some models return list-style output
        entry = data[0]
        if "label" in entry:
            return entry["label"]

    print("⚠️ Unexpected response format:", data)
    return "Uncategorized"
