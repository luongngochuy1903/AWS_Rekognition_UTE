from flask import request, jsonify

def faceRegconise(rekognition):
    try:
        file = request.files['image']
        image_byte = file.read()

        response = rekognition.search_faces_by_image(
            CollectionId='face_collection',
            Image={'Bytes': image_byte},
            FaceMatchThreshold=80,
            MaxFaces=5
        )

        matches = []
        for match in response.get('FaceMatches', []):
            matches.append({
                "ExternalImageId": match['Face']['ExternalImageId'],
                "Similarity": match['Similarity'],
                "FaceID": match['Face']['FaceId'],
                "SearchedFaceConfidence":match['SearchedFaceConfidence']
            })

        return jsonify({
            "status": "success",
            "matches": matches
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
