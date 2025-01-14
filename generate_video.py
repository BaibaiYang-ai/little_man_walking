import cv2
from PIL import Image
from ultralytics import YOLO
import os
import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.signal import find_peaks
import subprocess
import math


import subprocess
import os
import math
import re


def generate_video(ge_video_folder, video_name, resolution):
    current_dir = os.getcwd()


    # Define the folder containing your images
    image_folder = os.path.join(current_dir, ge_video_folder)  # Update this with your folder path
    output_video = video_name  # Output video filename
    fps = 30  # Frames per second in the output video
    # video_resolution = (1920, 1080)  # Desired resolution (width, height)
    video_resolution = resolution  # Desired resolution (width, height)

    # Get list of all images in the folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png'))]

    # Sort the images by name (or you can sort by date using os.path.getmtime if needed)
    image_files.sort()  # You can change this to sort by modification time, e.g. sorted(image_files, key=lambda x: os.path.getmtime(x))

    # Check if there are any images in the folder
    if not image_files:
        print("No images found in the folder.")
        exit()

    # Read the first image to get the dimensions (width and height)
    first_image = Image.open(os.path.join(image_folder, image_files[0]))
    first_image = first_image.resize(video_resolution)  # Resize to desired resolution
    frame_width, frame_height = first_image.size

    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

    # Loop through the sorted images, convert each to a frame, and write to the video
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        
        # Open the image
        img = cv2.imread(image_path)
        
        # Resize image to match the video resolution (if needed)
        img_resized = cv2.resize(img, (frame_width, frame_height))
        
        # Write the image frame to the video
        video_writer.write(img_resized)

        # generate_seg_images(img_resized, "Moon2.webp", model_seg, image_path)

    # Release the video writer object
    video_writer.release()

    print(f"Video created successfully: {output_video}")



from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageSequenceClip, CompositeVideoClip, vfx

def combine_videos_with_gif(video_files, gif_path, output_file="output_with_gif.mp4", fps=30, codec="libx264", gif_position=("right","bottom-200")):
    """
    Combines multiple videos into one and adds a GIF overlay.

    Parameters:
        video_files (list): List of video file paths to combine.
        gif_path (str): Path to the GIF file to overlay.
        output_file (str): Name of the output video file. Default is "output_with_gif.mp4".
        fps (int): Frames per second for the output video. Default is 30.
        codec (str): Codec for the output video. Default is "libx264".
        gif_position (tuple): Position of the GIF overlay (e.g., ("center", "center")).

    Returns:
        None
    """
    try:
        # Load video clips
        clips = [VideoFileClip(video) for video in video_files]
        
        # Combine video clips
        combined_clip = concatenate_videoclips(clips, method="compose")

            # Load the GIF
        gif_clip = VideoFileClip(gif_path, has_mask=True)


        loop_count = int(combined_clip.duration // gif_clip.duration) + 1

        loops = [gif_clip.copy() for _ in range(loop_count)]
        long_loop = concatenate_videoclips(loops)
        looped_clip = long_loop.set_duration(combined_clip.duration)

                # Adjust position for the GIF
        if isinstance(gif_position, tuple) and len(gif_position) == 2:
            x_pos, y_pos = gif_position
            if isinstance(x_pos, str) and x_pos.startswith("right"):
                x_offset = int(x_pos.split("-")[-1]) if "-" in x_pos else 0
                x_pos = combined_clip.size[0] - gif_clip.size[0] - x_offset
            if isinstance(y_pos, str) and y_pos.startswith("bottom"):
                y_offset = int(y_pos.split("-")[-1]) if "-" in y_pos else 0
                y_pos = combined_clip.size[1] - gif_clip.size[1] - y_offset
            gif_position = (x_pos, y_pos)
        gif_clip = looped_clip.set_position(gif_position)


        final_clip = CompositeVideoClip([combined_clip, gif_clip])
        # Add the GIF as an overlay

        # Write the output video file
        final_clip.write_videofile(output_file, codec=codec, fps=fps)
        print(f"Video with GIF successfully saved as {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")



# Example usage
if __name__ == "__main__":
    # generate_video("/data/men_women/generate_images/output_images", "wm.mp4", (1080,1920))
    gif_path = "myanimated_resized.gif"
    video_files = ["raw_video.MOV"]
    combine_videos_with_gif(video_files, gif_path, output_file="final_video.mp4")



