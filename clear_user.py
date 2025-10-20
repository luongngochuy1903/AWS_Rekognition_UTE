import boto3
import os
from dotenv import load_dotenv
from flask import jsonify

load_dotenv("aws-credentials.env")

rekognition = boto3.client(
    "rekognition",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

collection_id = "face_collection"
user_id = "Ngoc_Huy"

try:
    response = rekognition.delete_user(
        CollectionId=collection_id,
        UserId=user_id
    )
    print("Xóa user:", response)
except rekognition.exceptions.ResourceNotFoundException:
    print(f"User '{user_id}' không tồn tại trong collection.")
except Exception as e:
    print("Lỗi:", e)