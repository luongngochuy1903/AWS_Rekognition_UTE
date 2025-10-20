from flask import request, jsonify

def detect_protective_equipment(rekognition):
    try:
        file = request.files['image']
        image_byte = file.read()

        response = rekognition.detect_protective_equipment(
            Image={'Bytes': image_byte},
            SummarizationAttributes={
                'MinConfidence': 70,  # mức độ tin cậy tối thiểu
                'RequiredEquipmentTypes': ['FACE_COVER', 'HAND_COVER', 'HEAD_COVER']
            }
        )

        persons = []
        for person in response.get('Persons', []):
            equipment_info = []
            for equipment in person.get('BodyParts', []):
                equipment_info.append({
                    "Name": equipment.get("Name"),
                    "Confidence": equipment.get("Confidence"),
                    "EquipmentDetections": [
                        {
                            "Type": eq.get("Type"),
                            "CoversBodyPart": eq.get("CoversBodyPart"),
                            "Confidence": eq.get("Confidence"),
                            "Id": eq.get("Id")
                        } for eq in equipment.get("EquipmentDetections", [])
                    ]
                })

            persons.append({
                "BoundingBox": person.get("BoundingBox"),
                "Confidence": person.get("Confidence"),
                "BodyParts": equipment_info
            })

        return jsonify({
            "status": "success",
            "persons": persons
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
