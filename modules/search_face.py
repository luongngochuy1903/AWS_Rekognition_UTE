from flask import request, jsonify

def search_faces(rekognition):
    try:
        face_id = request.form['face_id']
        response = rekognition.search_faces(
            CollectionId='face_collection',
            FaceId=face_id,
            FaceMatchThreshold=80,
            MaxFaces=5
        )

        matches = [
            {
                "FaceID": res['Face']['FaceId'],
                'ExternalImageId': res['Face'].get('ExternalImageId'),
                "Similarity": res['Similarity']
            }
            for res in response.get('FaceMatches', [])
        ]

        return jsonify({
                "status": "success",
                "searched_face_id": face_id,
                "matches": matches
            })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500