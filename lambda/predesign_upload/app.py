import os
import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
BUCKET = os.environ['BUCKET_NAME']

def handler(event, context):
    """
    Expects body:
    {
      "userId": "user123",
      "filename": "receipt.jpg",
      "contentType": "image/jpeg"
    }
    """
    try:
        body = json.loads(event.get('body') or "{}")
        filename = body['filename']
        user = body.get('userId','unknown')
        key = f"receipts/{user}/{datetime.utcnow().strftime('%Y/%m/%d')}/{uuid.uuid4()}-{filename}"

        url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={'Bucket': BUCKET, 'Key': key, 'ContentType': body.get('contentType','application/octet-stream')},
            ExpiresIn=900
        )

        return {"statusCode": 200, "body": json.dumps({"uploadUrl": url, "key": key})}
    except Exception as e:
        print("Error:", e)
        return {"statusCode":500, "body": json.dumps({"error": str(e)})}
