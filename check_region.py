import boto3
import os
from dotenv import load_dotenv

load_dotenv("aws-credentials.env")

AWS_REGION = os.getenv("AWS_REGION")
print(AWS_REGION)

s3 = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

bucket_name = "rekognition-hcmutevn"

response = s3.get_bucket_location(Bucket=bucket_name)
print("Bucket region:", response['LocationConstraint'])

rekognition = boto3.client(
    'rekognition',
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

collections = rekognition.list_collections()
print("Collections:", collections['CollectionIds'])

collection_id = "face_collection"
info = rekognition.describe_collection(CollectionId=collection_id)
print("Collection info:", info)

faces = []
response = rekognition.list_faces(CollectionId=collection_id, MaxResults=1000)

faces.extend(response['Faces'])
print(f"Collection '{collection_id}' có {len(faces)} face vectors")