from flask import Flask, request, jsonify, render_template
import boto3
import os
from dotenv import load_dotenv
from modules.detect_label import detect_labels
from modules.upload_s3 import upload_to_s3, upload_s3_video
from modules.face_regconise import faceRegconise
from modules.search_face import search_faces
from modules.search_user import search_users
from modules.search_user_by_image import search_users_by_image
from modules.compare_image import compare_faces

from modules.video.label_detect_vid import *
from modules.video.face_detect_vid import *

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

#VIDEO
@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/video/upload', methods=['POST'])
def upload_video():
    return upload_s3_video(s3)

@app.route('/video/label-detect', methods=['POST'])
def video_label_detect():
    return detect_labels_video(rekognition)

@app.route('/video/face-detect', methods=['POST'])
def video_face_detect():
    return detect_faces_video(rekognition)

#Nhóm 1
@app.route('/recognise', methods=['POST'])
def recognise():
    return faceRegconise(rekognition)

@app.route('/compare', methods=['POST'])
def compare():
    return compare_faces(rekognition)

@app.route('/upload', methods=['POST'])
def upload():
    return upload_to_s3(rekognition, s3)

@app.route('/search_face', methods=['POST'])
def search_face():
    return search_faces(rekognition)

@app.route('/search_users', methods=['POST'])
def search_user():
    return search_users(rekognition)

@app.route('/search_users_by_image', methods=['POST'])
def search_users_by_images():
    return search_users_by_image(rekognition)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8087, debug=True)
