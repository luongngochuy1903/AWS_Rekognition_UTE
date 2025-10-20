from flask import request, jsonify
import time

def detect_celebrity_video(rekognition):
    try:
        s3_key = request.form['s3_file']

        # Start celebrity recognition job
        response = rekognition.start_celebrity_recognition(
            Video={'S3Object': {'Bucket': 'rekognition-hcmutevn', 'Name': s3_key}}
        )
        job_id = response['JobId']

        # Poll until job finishes
        status = "IN_PROGRESS"
        max_attempts = 20
        attempt = 0
        while status == "IN_PROGRESS" and attempt < max_attempts:
            time.sleep(5)
            result = rekognition.get_celebrity_recognition(JobId=job_id)
            status = result.get('JobStatus', 'IN_PROGRESS')
            attempt += 1

        if status != "SUCCEEDED":
            return jsonify({
                "status": "error",
                "message": f"Celebrity recognition job did not succeed, final status: {status}"
            }), 500

        # Lấy kết quả celeb
        celebs_data = []
        for item in result.get('Celebrities', []):
            celeb = item.get('Celebrity', {})
            celebs_data.append({
                "Timestamp": item.get('Timestamp'),
                "Name": celeb.get('Name'),
                "Id": celeb.get('Id'),
                "Urls": celeb.get('Urls', []),
                "Confidence": celeb.get('Confidence'),
                "BoundingBox": celeb.get('Face', {}).get('BoundingBox', {})
            })

        return jsonify({
            "status": "success",
            "job_id": job_id,
            "total_celebrities": len(celebs_data),
            "celebrities": celebs_data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
