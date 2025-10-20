from flask import jsonify
#Insert to collection
def index_faces(rekognition, filename, input_metadata):
    response = rekognition.index_faces(
        CollectionId='face_collection',
        Image={'S3Object': {'Bucket': 'rekognition-hcmutevn', 'Name': filename}},
        ExternalImageId=input_metadata,
        DetectionAttributes=['ALL']
        )
    
    faces = []
    for record in response.get('FaceRecords', []):
        face = record['Face']
        details = record['FaceDetail']
        
        faces.append({
                "FaceId": face['FaceId'],
                "ImageId": face['ImageId'],
                "ExternalImageId": face.get('ExternalImageId'),
                "Confidence": face['Confidence'],
                "AgeRange": details.get('AgeRange', {}),
                "Gender": details.get('Gender', {}),
                "Emotions": details.get('Emotions', []),
                "Smile": details.get('Smile', {}),
                "Eyeglasses": details.get('Eyeglasses', {}),
                "Beard": details.get('Beard', {}),
                "Mustache": details.get('Mustache', {}),
                "EyesOpen": details.get('EyesOpen', {}),
                "MouthOpen": details.get('MouthOpen', {}),
                "Pose": details.get('Pose', {}),
                "Quality": details.get('Quality', {})
            })
    
    if not faces:
            return {
            "status": "no_face_detected",
            "message": f"No faces detected in {filename}"
        }

    return {
        "status": "success",
        "message": f"Indexed {len(faces)} face(s) from image '{filename}'",
        "faces": faces
    }