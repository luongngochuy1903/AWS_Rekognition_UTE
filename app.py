from flask import Flask, request, jsonify, render_template
import boto3
import os
from dotenv import load_dotenv
from modules.detect_label import detect_labels
from modules.upload_s3 import upload_to_s3
from modules.face_regconise import faceRegconise

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

#Nhóm 1
@app.route('/recognise', methods=['POST'])
def recognise():
    return faceRegconise(rekognition)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8087, debug=True)
