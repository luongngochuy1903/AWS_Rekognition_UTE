from flask import request, jsonify
import time

def detect_faces_video(rekognition):
    try:
        s3_key = request.form['s3_file']

        response = rekognition.start_face_detection(
            Video={'S3Object': {'Bucket': 'rekognition-hcmutevn', 'Name': s3_key}},
            FaceAttributes='ALL'  
        )
        job_id = response['JobId']

        status = "IN_PROGRESS"
        max_attempts = 20
        attempt = 0
        while status == "IN_PROGRESS" and attempt < max_attempts:
            time.sleep(5)  
            result = rekognition.get_face_detection(JobId=job_id)
            status = result.get('JobStatus', 'IN_PROGRESS')
            attempt += 1

        if status != "SUCCEEDED":
            return jsonify({
                "status": "error",
                "message": f"Face detection job did not succeed, final status: {status}"
            }), 500

        faces_data = []
        for item in result.get('Faces', []):
            face_detail = item.get('Face', {})
            faces_data.append({
                "Timestamp": item.get('Timestamp'),
                "BoundingBox": face_detail.get('BoundingBox'),
                "Confidence": face_detail.get('Confidence'),
                "Smile": face_detail.get('Smile', {}),
                "Gender": face_detail.get('Gender', {}),
                "Emotions": face_detail.get('Emotions', []),
                "Pose": face_detail.get('Pose', {})
            })

        return jsonify({
            "status": "success",
            "job_id": job_id,
            "total_faces": len(faces_data),
            "faces": faces_data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500