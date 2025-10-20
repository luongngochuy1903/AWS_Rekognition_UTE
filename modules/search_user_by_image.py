from flask import request, jsonify

def search_users_by_image(rekognition):
    try:
        file = request.files['image']
        image_bytes = file.read()

        response = rekognition.search_users_by_image(
            CollectionId='face_collection',
            Image={'Bytes': image_bytes},
            UserMatchThreshold=80,
            MaxUsers=5
        )

        matches = [{
            "UserId": m['User']['UserId'],
            "Similarity": m['Similarity']
        } for m in response.get('UserMatches', [])]


        return jsonify({
            "status": "success",
            "matches": matches
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500