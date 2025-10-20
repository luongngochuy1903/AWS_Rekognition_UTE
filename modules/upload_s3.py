from flask import request, jsonify
from modules.index_face import index_faces
from modules.face_association import associate_faces, ensure_user_exists
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
        info_json= index_faces(rekognition, file_name, external_info)
        faces = info_json.get('faces', [])
        face_ids = [f['FaceId'] for f in faces]
        user_status = ensure_user_exists(rekognition, person_name)
        associate_result = associate_faces(rekognition, person_name, face_ids)

        return jsonify({
            "status": "success",
            "user_status": user_status,
            "file_name": file_name,
            "indexed_faces": faces,
            "associate_result": associate_result
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500