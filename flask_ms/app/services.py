from twelvelabs import TwelveLabs
from flask import current_app
from twelvelabs.models.task import Task
import yt_dlp
import os
from collections import Counter
from flask import request, jsonify
import cv2
import torch
import numpy as np
from collections import Counter
from ultralytics import YOLO

from collections import Counter
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo


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

        # while True:
        #     try:
        #         search_results = next(search_results)
        #         video_segments.extend(process_search_results(search_results))
        #     except StopIteration:
        #         break
        


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

    
def extract_colors(video_path, start_time, end_time, frame_skip=50):
    # Load class names (COCO dataset labels used by YOLOv8)
    classNames = {
        0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle',
        4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat',
        9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign',
        12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat',
        16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant',
        21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack',
        25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase',
        29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball',
        33: 'kite', 34: 'baseball bat', 35: 'baseball glove',
        36: 'skateboard', 37: 'surfboard', 38: 'tennis racket',
        39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork',
        43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana',
        47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli',
        51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut',
        55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant',
        59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv',
        63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard',
        67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster',
        71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock',
        75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier',
        79: 'toothbrush'
    }

    # Desired classes to extract colors from ('car' and 'bus')
    desired_classes = [0]  # YOLO class IDs for 'car' and 'bus'

    # Load the pre-trained YOLOv8 segmentation model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = YOLO('yolov8s-seg.pt')  # Use 'yolov8n-seg.pt' for a smaller, faster model
    model.to(device)

    # Open the video file
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

        if (frame_count - start_frame) % frame_skip == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform detection, specifying desired classes
            with torch.no_grad():
                results = model(frame_rgb, classes=desired_classes)

            # Process detections
            for result in results:
                boxes = result.boxes  # Boxes object
                masks = result.masks  # Masks object

                if masks is None:
                    continue  # Skip if no masks are available

                scores = boxes.conf.cpu().numpy()
                masks_data = masks.data.cpu().numpy()  # Shape: (N, H, W)

                for i in range(len(scores)):
                    if scores[i] > 0.5:
                        # Bounding box and mask
                        x1, y1, x2, y2 = boxes.xyxy[i].cpu().numpy().astype(int)
                        mask = masks_data[i]  # Mask for the detected object
                        mask = (mask > 0.5).astype(np.uint8)  # Binarize the mask

                        # Apply the mask to the region of interest (ROI)
                        roi = frame_rgb[y1:y2, x1:x2]
                        mask_resized = cv2.resize(mask, (roi.shape[1], roi.shape[0]))
                        masked_roi = roi[mask_resized == 1]

                        # Extract the dominant color from the masked ROI
                        if masked_roi.size > 0:
                            # Quantize the colors to reduce the number of unique colors
                            quantized_colors = (masked_roi // 32) * 32  # Reduce to 8 levels per channel
                            # Flatten the array for histogram computation
                            flat_colors = quantized_colors.reshape(-1, 3)
                            # Convert colors to tuples for counting
                            colors_list = [tuple(color) for color in flat_colors]
                            # Count the colors
                            color_counts = Counter(colors_list)
                            # Get the most common color
                            dominant_color = color_counts.most_common(1)[0][0]
                            # Add the dominant color to the list
                            colors.append(dominant_color)

        frame_count += frame_skip

    cap.release()

    # Count the most common dominant colors
    color_counts = Counter(colors)
    return color_counts