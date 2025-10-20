from flask import request, jsonify
import time

def detect_text_video(rekognition):
    try:
        s3_key = request.form['s3_file']

        # Start text detection job
        response = rekognition.start_text_detection(
            Video={'S3Object': {'Bucket': 'rekognition-hcmutevn', 'Name': s3_key}}
        )
        job_id = response['JobId']

        # Poll until job finishes
        status = "IN_PROGRESS"
        max_attempts = 20
        attempt = 0
        while status == "IN_PROGRESS" and attempt < max_attempts:
            time.sleep(5)
            result = rekognition.get_text_detection(JobId=job_id)
            status = result.get('JobStatus', 'IN_PROGRESS')
            attempt += 1

        if status != "SUCCEEDED":
            return jsonify({
                "status": "error",
                "message": f"Text detection job did not succeed, final status: {status}"
            }), 500

        # Lấy kết quả text
        texts_data = []
        for item in result.get('TextDetections', []):
            td = item.get('TextDetection', {})
            texts_data.append({
                "Timestamp": item.get('Timestamp'),
                "DetectedText": td.get('DetectedText'),
                "Confidence": td.get('Confidence'),
                "Type": td.get('Type')
            })

        return jsonify({
            "status": "success",
            "job_id": job_id,
            "total_texts": len(texts_data),
            "texts": texts_data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
