from flask import Flask, request, jsonify, render_template
import boto3

def detect_labels(rekognition):
    try:
        if 'image' not in request.files:
            return jsonify({"error": "Không tìm thấy ảnh"}), 400

        file = request.files['image']
        image_bytes = file.read()
        print(f"Nhận file: {file.filename}, kích thước {len(image_bytes)}")

        response = rekognition.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=70
        )

        labels = [
            {"name": label["Name"], "confidence": label["Confidence"], "categories":label["Categories"]}
            for label in response["Labels"]
        ]

        return jsonify({"labels": labels})

    except Exception as e:
        print("Lỗi:", e)
        return jsonify({"error": str(e)}), 500