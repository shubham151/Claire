from flask import Blueprint, Flask, render_template, request, send_file, jsonify
import requests
import re
import os
import time
import json
from app.services import createIndex, uploadVideoToIndex, download_tiktok_video

UPLOAD_DIR = '/home/spidermines/Projects/Claire/main_app/public/uploads/'
INDEX_NAME='zeitgeist_sm_color'
INDEX_ID='670b36a7e2f5d6a324a6b710'

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/')
def home():
    return 'Hello, Flask!'

@api_blueprint.route('/download_video', methods=['POST'])
def download_video():
    print("Entry")
    data = request.get_json()
    video_url = re.sub(r'\?.*', '', data.get('url'))
    try:
        filename = download_tiktok_video(video_url, UPLOAD_DIR)
        uploadVideoToIndex(filename, INDEX_ID)
        return jsonify({"message": "Document saved successfully"}), 200

    except:
        print("Failed to Download")
        return None


@api_blueprint.route('/create_index', methods=['POST'])
def create_tlIndex():
    createIndex(INDEX_NAME)
    return jsonify({"message": f"{INDEX_NAME} created successfully"}), 200





