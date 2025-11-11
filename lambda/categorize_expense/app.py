
# import os
# import json
# import requests

# HF_TOKEN = os.environ.get("HF_TOKEN")
# HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"

# def categorize_expense(description):
#     """Use Hugging Face API (router) to predict expense category."""
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
#     print("🔍 HF response:", data)  # helpful for CloudWatch

#     # ✅ Robust parsing for all known response formats
#     if isinstance(data, dict):
#         # New router format
#         if "labels" in data and "scores" in data:
#             labels = data["labels"]
#             scores = data["scores"]
#             if labels and scores:
#                 top_label = labels[scores.index(max(scores))]
#                 return top_label
#         # Old format inside "result"
#         elif "result" in data and "labels" in data["result"]:
#             return data["result"]["labels"][0]

#     elif isinstance(data, list) and len(data) > 0:
#         # Some models return list-style output
#         entry = data[0]
#         if "label" in entry:
#             return entry["label"]

#     print("⚠️ Unexpected response format:", data)
#     return "Uncategorized"
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
    print("🔍 HF response:", data)

    if isinstance(data, dict):
        if "labels" in data and "scores" in data:
            labels = data["labels"]
            scores = data["scores"]
            if labels and scores:
                top_label = labels[scores.index(max(scores))]
                return top_label
        elif "result" in data and "labels" in data["result"]:
            return data["result"]["labels"][0]
    elif isinstance(data, list) and len(data) > 0:
        entry = data[0]
        if "label" in entry:
            return entry["label"]

    print("⚠️ Unexpected response format:", data)
    return "Uncategorized"


def handler(event, context):
    """AWS Lambda entry point."""
    try:
        print("🧾 Incoming event:", event)
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        elif not isinstance(body, dict):
            body = event  # direct invocation

        description = body.get("description")
        if not description:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing description"})
            }

        category = categorize_expense(description)

        return {
            "statusCode": 200,
            "body": json.dumps({"category": category})
        }

    except Exception as e:
        print("❌ Error in Categorize Lambda:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

