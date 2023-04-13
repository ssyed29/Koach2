from flask import request, Flask, render_template
from flask_restful import Resource, Api
import os
import cv2
import youtube_dl
import pafy
import numpy as np
import torch
from learn_characters import FrameData, Game, Game1, Game2
from PIL import Image
import imageio
import pytesseract
import cv2
import numpy as np
import re

class VideoAnalysis(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'error': 'No video file'}, 400
        video = request.files['file']
        video_path = f"temp/{video.filename}"
        video.save(video_path)
        
        character_move_gifs = load_gifs()
        round_data = analyze_video(video_path, gameplay_model, character_move_gifs)
        return {'round_data': round_data}

#Api.add_resource(VideoAnalysis, '/analyze_video')

def detect_text(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(gray)
    text_detection = cv2.dnn.readNet('models/frozen_east_text_detection.pb')


    # Return the detected text
    return text


# Perform video analysis and return the results
def analyze_video(video):
    # Determine the video source and download the video
    if isinstance(video, str):
        video_filename = download_video(video)
        video_duration = get_video_duration(video)
    else:
        video_filename = f"temp/{video.filename}"
        video.save(video_filename)
        video_duration = None

    # Load character move gifs
    character_move_gifs = load_gifs()

    # Initialize list to store round data
    round_data_list = []

    # Iterate through each frame of the video
    cap = cv2.VideoCapture(video_filename)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Use OCR to detect text in the frame
        text = detect_text(frame)

        # Process the text to extract relevant information for the round
        round_data = process_round_data(text)

        # Store the round data in the list
        round_data_list.append(round_data)

    # Release the video capture object and return the list of round data
    cap.release()
    return round_data_list


def download_video(video_url):
    # Download the video using youtube_dl
    ydl_opts = {
        "format": "best",
        "outtmpl": "videos/%(title)s.%(ext)s",
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        info = ydl.extract_info(video_url, download=False)
        return "videos/" + info["title"] + "." + info["ext"]

def get_video_duration(video_url):
    # Get the video duration using pafy
    video = pafy.new(video_url)
    return video.length

def detect_text(image):
    # Implement text detection in the image (e.g., using OCR)
    # Use the text_detection model to detect text in the image
    text_detection.setInput(cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0)))
    output = text_detection.forward()
    (h, w) = image.shape[:2]
    detections = []
    for i in range(output.shape[2]):
        confidence = output[0, 0, i, 2]
        if confidence > 0.5:
            box = output[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            detections.append((startX, startY, endX, endY))
    # Return the detected text
    return pytesseract.image_to_string(image[detections[0][1]:detections[0][3], detections[0][0]:detections[0][2]]) 


def process_round_data(text):
    # Initialize variables to store the gameplay start and end times
    gameplay_starts = []
    gameplay_ends = []

    # Compile regular expressions to find "FIGHT", "K.O.", and the round number
    fight_re = re.compile(r'FIGHT', re.IGNORECASE)
    ko_re = re.compile(r'K\.O\.', re.IGNORECASE)
    round_re = re.compile(r'Round (\d+)', re.IGNORECASE)

    # Split the text into lines
    lines = text.split('\n')

    # Iterate through each line in the text
    for line in lines:
        fight_match = fight_re.search(line)
        ko_match = ko_re.search(line)
        round_match = round_re.search(line)

        # If the "FIGHT" text is found, mark the start of the gameplay
        if fight_match:
            gameplay_starts.append(line)

        # If the "K.O." text is found, mark the end of the gameplay
        if ko_match:
            gameplay_ends.append(line)

        # If the round number is found, store the round number
        if round_match:
            current_round = int(round_match.group(1))

    # Use the gameplay_starts and gameplay_ends lists to determine gameplay sections
    gameplay_sections = list(zip(gameplay_starts, gameplay_ends))

    # Process the gameplay_sections to extract relevant information

    for start, end in gameplay_sections:
        # Extract the information for each round (e.g., determining the winner, frame data)
        # Use the start and end times to extract the relevant text from the OCR output
        text = extract_text(start, end)
        # Process the text to extract the relevant information for the round
        round_data = process_round_data(text)
        # Store the round data in a list or dictionary
        round_data_list.append(round_data)

    # Return the list or dictionary of round data
    return round_data_list

def frame_data_from_gif(gif_file):
    # Extract frame data from the given GIF file
    frames = imageio.mimread(gif_file)
    frame_data = []
    for frame in frames:
        # Extract necessary data from each frame (e.g., character position, opponent position, health bars)
        extracted_data = fetch_frame_data(frame)
        # Store the extracted data in a list or dictionary
        frame_data.append(extracted_data)
    # Return the list or dictionary of extracted frame data
    return frame_data

def extract_round_winner(frame):
    # Define color ranges for blue circles
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])

    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for blue circles
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # Apply the mask to the frame
    blue_circles = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # Find the contours of the blue circles
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours and find the one with the largest area
    max_area = 0
    winner = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            # Determine the winner based on the contour's position (left or right)
            x, _, _, _ = cv2.boundingRect(cnt)
            winner = 'left' if x < frame.shape[1] / 2 else 'right'

    return winner

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        winner = extract_round_winner(frame)
        if winner:
            print(f'The winner is the {winner} character.')

    cap.release()

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"path\to\tesseract.exe"

#app = Flask(__name__)
#api = Api(app)
