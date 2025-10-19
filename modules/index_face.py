#Insert to collection
def index_faces(rekognition, filename, input_metadata):
    rekognition.index_faces(
    CollectionId='face_collection',
    Image={'S3Object': {'Bucket': 'rekognition-hcmutevn', 'Name': filename}},
    ExternalImageId=input_metadata,
    DetectionAttributes=['ALL']
)