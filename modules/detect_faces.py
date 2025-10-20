from flask import request, jsonify

def detect_faces(rekognition):
    try:
        file = request.files['image']
        image_byte = file.read()

        response = rekognition.detect_faces(
            Image={'Bytes': image_byte},
            Attributes=['ALL']
        )
        faces = []
        for face in response.get('FaceDetails', []):
            faces.append({
                "AgeRange": face.get("AgeRange"),
                "Gender": face.get("Gender"),
                "Emotions": sorted(
                    face.get("Emotions", []),
                    key=lambda e: e["Confidence"],
                    reverse=True
                )[:1],  # chỉ lấy emotion có Confidence cao nhất
                "Smile": face.get("Smile"),
                "Beard": face.get("Beard"),
                "Mustache": face.get("Mustache"),
                "Eyeglasses": face.get("Eyeglasses"),
                "Sunglasses": face.get("Sunglasses"),
                "Confidence": face.get("Confidence")
            })
        return jsonify({
            "status": "success",
            "faces": faces
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
