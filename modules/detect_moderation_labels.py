from flask import request, jsonify

def detect_moderation_labels(rekognition):
    try:
        file = request.files['image']
        image_byte = file.read()

        response = rekognition.detect_moderation_labels(
            Image={'Bytes': image_byte}
        )

        labels = []
        for label in response.get('ModerationLabels', []):
            labels.append({
                "Name": label.get("Name"),
                "ParentName": label.get("ParentName"),
                "Confidence": round(label.get("Confidence", 0), 2)
            })

        return jsonify({
            "status": "success",
            "moderation_labels": labels
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
