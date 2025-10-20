from flask import request, jsonify

def detect_text(rekognition):
    try:
        file = request.files['image']
        image_byte = file.read()

        response = rekognition.detect_text(
            Image={'Bytes': image_byte}
        )

        texts = [
            {
                "DetectedText": item['DetectedText'],
                "Confidence": item['Confidence'],
                "Type": item['Type']
            }
            for item in response.get('TextDetections', [])
        ]

        return jsonify({
            "status": "success",
            "texts": texts
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
