from flask import request, jsonify

def compare_faces(rekognition):
    try:
        source_file = request.files.get('image')
        target_file = request.files.get('image_target')

        if not source_file or not target_file:
            return jsonify({
                "status": "error",
                "message": "Thiếu ảnh nguồn hoặc ảnh đích!"
            }), 400

        response = rekognition.compare_faces(
            SourceImage={'Bytes': source_file.read()},
            TargetImage={'Bytes': target_file.read()},
            SimilarityThreshold=80
        )

        matches = [
            {
                "Similarity": match["Similarity"],
                "Emotion": match.get("Face", {}).get("Emotions", []),
                "Confidence": match["Face"]["Confidence"]
            }
            for match in response.get("FaceMatches", [])
        ]

        unmatches = [
            {
                "Emotion": match.get("Emotions", []),
                "Confidence": match["Confidence"]
            }
            for match in response.get("UnmatchedFaces", [])
        ]

        return jsonify({
            "status": "success",
            "matches": matches,
            "unmatched_faces": unmatches
        })

    except Exception as e:
        if "invalid parameter" in str(e).lower():
            return jsonify({"status": "fail", 
                            "message": "Wrong input !"
                            })
        else:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500