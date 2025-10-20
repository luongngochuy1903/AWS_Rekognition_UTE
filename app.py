from flask import Flask, request, jsonify, render_template
import boto3
import os
from dotenv import load_dotenv
from modules.detect_label import detect_labels
from modules.upload_s3 import upload_to_s3
from modules.face_regconise import faceRegconise

from modules.detect_faces import detect_faces
from modules.detect_text import detect_text
from modules.detect_moderation_labels import detect_moderation_labels
from modules.recognize_celebrities import recognize_celebrities


load_dotenv("aws-credentials.env")

AWS_REGION = os.getenv("AWS_REGION")

app = Flask(__name__)

rekognition = boto3.client(
    'rekognition',
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

s3 = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

@app.route('/')
def index():
    return render_template('index.html')

#Nhóm 2
@app.route('/detect', methods=['POST'])
def detect():
    return detect_labels(rekognition)

@app.route('/upload', methods=['POST'])
def upload():
    return upload_to_s3(rekognition, s3)

#t
@app.route('/detect-text', methods=['POST'])
def detectText():
    return detect_text(rekognition)

@app.route('/detect-moderation-labels', methods=['POST'])
def detectModerationLabels():
    return detect_moderation_labels(rekognition)



#Nhóm 1
@app.route('/recognise', methods=['POST'])
def recognise():
    return faceRegconise(rekognition)
#tâm
@app.route('/detect-faces', methods=['POST'])
def detectFaces():
    return detect_faces(rekognition)

@app.route('/recognize-celebrities', methods=['POST'])
def recognizeCelebrities():
    return recognize_celebrities(rekognition)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8087, debug=True)
