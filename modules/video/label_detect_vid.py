from flask import request, jsonify
import uuid
import boto3
import os, time

def detect_labels_video(rekognition):
    try:
        s3_key = request.form['s3_file']

        response = rekognition.start_label_detection(
            Video={'S3Object': {'Bucket': 'rekognition-hcmutevn', 'Name': s3_key}},
            MinConfidence=70,
        )
        job_id = response['JobId']

        status = "IN_PROGRESS"
        max_attempts = 20  
        attempt = 0
        while status == "IN_PROGRESS" and attempt < max_attempts:
            time.sleep(5) 
            result = rekognition.get_label_detection(JobId=job_id, SortBy='TIMESTAMP')
            status = result.get('JobStatus', 'IN_PROGRESS')
            attempt += 1

        if status != "SUCCEEDED":
            return jsonify({
                "status": "error",
                "message": f"Label detection job did not succeed, final status: {status}"
            }), 500

        labels_data = []
        for item in result.get('Labels', []):
            labels_data.append({
                "Timestamp": item['Timestamp'],
                "Label": item['Label']['Name'],
                "Confidence": item['Label']['Confidence']
            })

        return jsonify({
            "status": "success",
            "job_id": job_id,
            "total_labels": len(labels_data),
            "labels": labels_data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500