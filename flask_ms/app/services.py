from twelvelabs import TwelveLabs
from flask import current_app
from twelvelabs.models.task import Task
import yt_dlp
import os
import cv2
from collections import Counter
from flask import request, jsonify


# client = TwelveLabs(api_key=current_app.config['12LAB_KEY'])

engines = [
        {
          "name": "marengo2.6",
          "options": ["visual", "conversation", "text_in_video", "logo"]
        },
        {
            "name": "pegasus1.1",
            "options": ["visual", "conversation"]
        }
    ]


def get_twelve_labs_client():
    return TwelveLabs(api_key=current_app.config['12LAB_KEY'])

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
    print(videoPath+ " "+ indexName)
    client=get_twelve_labs_client()
    try:
        task = client.task.create(
        index_id=indexName,
        file=videoPath
        )

        print(f"Task id={task.id}")

        return task.video_id
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return None
    
    

def rename_video(old, new):
    # Get the current filename and the new name (without extension)
    

    # Get the file extension
    file_extension = os.path.splitext(old)[1]  # Get the extension (.mp4, .avi, etc.)
    
    # Create new file path with the new name and the same extension
    new_file_path = f"{new}{file_extension}"

    try:
        # Rename the file
        os.rename(old, new_file_path)
        return True
    except Exception as e:
        return False

def search_query(indexId, searchQuery, top_cnt, uploadDir):
    client=get_twelve_labs_client()
    try:
        search_results = client.search.query(
            index_id=indexId,
            query_text=searchQuery, 
            options=['visual']
        )

        print(search_results)
        
        video_segments = process_search_results(search_results)

        while True:
            try:
                search_results = next(search_results)
                video_segments.extend(process_search_results(search_results))
            except StopIteration:
                break
        


        print(f"Found {len(video_segments)} segments labeled {searchQuery}.")
        print(video_segments)


        all_colors = Counter()

        for segment in video_segments:
            video_id = segment["video_id"]
            start = segment["start"]
            end = segment["end"]
            
            video_path = os.path.join(uploadDir, f"{video_id}.mp4") 
            
            if not os.path.exists(video_path):
                print(f"Video file not found: {video_path}")
                continue
            
            colors = extract_colors(video_path, start, end)
            all_colors.update(colors)


        most_common_colors = all_colors.most_common(top_cnt)
        colors_response = []
        for color, count in most_common_colors:
            colors_response.append({
                'color': rgb_to_hex(color),
                'count': count
            })

        return colors_response


    except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return None


def rgb_to_hex(rgb_tuple):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)
 
def process_search_results(search_results):
    segments = []
    for clip in search_results.data:
        segments.append({
            "video_id": clip.video_id,
            "start": clip.start,
            "end": clip.end,
            "metadata": clip.metadata
        })
    return segments

    
def extract_colors(video_path, start_time, end_time, frame_skip=300):

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return Counter()
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    colors = []
    frame_count = start_frame
    while frame_count <= end_frame:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Reshape the frame to a list of pixels
        pixels = frame_rgb.reshape(-1, 3)
        
        
        if frame_count % frame_skip == 0:
            # Convert pixels to tuples and add to the list
            colors.extend([tuple(pixel) for pixel in pixels])
        
        frame_count += frame_skip
    
    cap.release()
    
    # Count the most common colors
    color_counts = Counter(colors)
    return color_counts


