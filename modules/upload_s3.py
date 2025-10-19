from flask import request, jsonify
from modules.index_face import index_faces
import boto3
import uuid
import time

def upload_to_s3(rekognition, s3):
    try:
        file = request.files['image_upload']
        person_name = request.form['name']
        person_age = request.form['age']
        external_info = f"{person_name}_{person_age}"
        file_name = f"{uuid.uuid4()}_{person_name}"
        s3.upload_fileobj(file, 'rekognition-hcmutevn', file_name)
        time.sleep(3)
        index_faces(rekognition, file_name, external_info)
        return jsonify({
                "status": "success",
                "file_name": file_name,
                "external_info": external_info
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500