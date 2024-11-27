import numpy as np
import os
import cv2
from datetime import datetime

def create_vector_field_video(folder_path, video_path):
    """
    Reads all .npy files from the specified folder, separates Vx and Vy arrays,
    calculates the net vector field V, and creates a video using the jet colormap.

    Parameters:
    folder_path (str): Path to the folder containing .npy files.
    video_path (str): Path to save the output video.
    """
    # Get list of all .npy files in the folder
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.npy')]
    file_list.sort()  # Ensure files are processed in order

    # Initialize lists to hold Vx and Vy arrays
    Vx_list = []
    Vy_list = []

    # Load each file and separate Vx and Vy
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        data = np.load(file_path)
        Vx_list.append(data[0])
        Vy_list.append(data[1])

    # Convert lists to numpy arrays
    Vx_array = np.array(Vx_list)
    Vy_array = np.array(Vy_list)

    # Calculate the net vector V
    V = np.sqrt(Vx_array**2 + Vy_array**2)

    # Create a video from the net vector V
    height, width = V.shape[1], V.shape[2]
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = 'output_video_{current_time}.avi'.format(current_time=current_time)
    video_path = os.path.join(video_path, video_filename)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(video_path, fourcc, 1, (width, height), isColor=True)

    for i in range(V.shape[0]):
        normalized_frame = (V[i] * 255 / np.max(V[i])).astype(np.uint8)  # Normalize and convert to uint8
        colored_frame = cv2.applyColorMap(normalized_frame, cv2.COLORMAP_JET)  # Apply jet colormap
        video.write(colored_frame)

    video.release()
    print("Video saved at:", video_path)

