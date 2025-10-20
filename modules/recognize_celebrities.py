from flask import request, jsonify

def recognize_celebrities(rekognition):
    try:
        file = request.files['image']
        image_byte = file.read()

        response = rekognition.recognize_celebrities(
            Image={'Bytes': image_byte}
        )

        celebs = [
            {
                "Name": celeb['Name'],
                "MatchConfidence": celeb['MatchConfidence']
            }
            for celeb in response.get('CelebrityFaces', [])
        ]

        return jsonify({
            "status": "success",
            "celebrities": celebs
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
