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


def clear_collection(rekognition):
    try:
        collection_id = 'face_collection'
        deleted_faces = []
        next_token = None

        while True:
            if next_token:
                response = rekognition.list_faces(CollectionId=collection_id, NextToken=next_token)
            else:
                response = rekognition.list_faces(CollectionId=collection_id)

            faces = response.get('Faces', [])
            face_ids = [f['FaceId'] for f in faces]

            if face_ids:
                delete_resp = rekognition.delete_faces(
                    CollectionId=collection_id,
                    FaceIds=face_ids
                )
                deleted_faces.extend(delete_resp.get('DeletedFaces', []))

            next_token = response.get('NextToken')
            if not next_token:
                break

        return {
            "status": "success",
            "message": f"Đã xoá {len(deleted_faces)} khuôn mặt khỏi collection.",
            "deleted_faces": deleted_faces
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

print(clear_collection(rekognition))