from flask import request, jsonify

def search_users(rekognition):
    try:
        face_id = request.form['face_id']
        response = rekognition.search_users(
            CollectionId='face_collection',
            FaceId=face_id,
            UserMatchThreshold=80,
            MaxUsers=5
        )

        matches = [{
            "UserId": m['User']['UserId'],
            "Similarity": m['Similarity']
        } for m in response.get('UserMatches', [])]

        return jsonify({
            "status": "success",
            "searched_face_id": face_id,
            "matches": matches
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500