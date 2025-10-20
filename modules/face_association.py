from flask import request, jsonify

def ensure_user_exists(rekognition, user_id):
    try:
        rekognition.create_user(
            CollectionId='face_collection',
            UserId=user_id
        )
        return {"status": "success", "message": f"User '{user_id}' created."}
    except Exception as e:
        if "already exists" in str(e).lower() or "invalid parameter" in str(e).lower():
            return {"status": "exists", "message": f"User '{user_id}' already exists."}
        else:
            raise
    
def associate_faces(rekognition, user_id, face_ids):
    try:
        response = rekognition.associate_faces(
            CollectionId='face_collection',
            UserId=user_id,
            FaceIds=face_ids
        )
        return {
            "status": "success",
            "user_id": user_id,
            "associated_faces": face_ids,
            "full_response": response
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}