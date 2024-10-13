from twelvelabs import TwelveLabs
from flask import current_app
from twelvelabs.models.task import Task
import yt_dlp
import os


# client = TwelveLabs(api_key=current_app.config['12LAB_KEY'])

engines = [
        {
            "name": "pegasus1.1",
            "options": ["visual", "conversation"]
        }
    ]

def get_twelve_labs_client():
    return TwelveLabs(api_key=current_app.config['12LAB_KEY'])

def createIndex(indexName):
    client=get_twelve_labs_client()
    index = client.index.create(
        # name="zeitgeist_sm_color",
        name=indexName,
        engines=engines,
        # addons=["thumbnail"]
        )
    print(f"A new index has been created: id={index.id} name={index.name} engines={index.engines}")

def uploadVideoToIndex(videoPath, indexName):
    client=get_twelve_labs_client()
    task = client.task.create(
    index_id=indexName,
    file=videoPath
    )
    print(f"Task id={task.id}")
    
def download_tiktok_video(video_url, save_path):
    # Ensure the save directory exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(save_path, '%(id)s.%(ext)s'),
        'format': 'best',
    }

    try:
        # Create a yt-dlp object and download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"Video successfully downloaded: {filename}")
            return filename
    
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None