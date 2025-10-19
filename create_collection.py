import boto3
import os
from dotenv import load_dotenv

load_dotenv("aws-credentials.env")

rekognition = boto3.client(
    "rekognition",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

collection_id = "face_collection"

# try:
#     response_delete = rekognition.delete_collection(CollectionId=collection_id)
#     print(f"Đã xóa collection: {collection_id}, Response: {response_delete}")
# except rekognition.exceptions.ResourceNotFoundException:
#     print(f"Collection {collection_id} chưa tồn tại, không cần xóa.")

# Tạo collection
response = rekognition.create_collection(CollectionId=collection_id)
print(response)
