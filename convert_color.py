import time
import os
import threading
import re
from concurrent.futures import ThreadPoolExecutor
import PySimpleGUI as sg
from PIL import Image
from moviepy.editor import VideoFileClip
from tqdm import tqdm
import imageio
import subprocess


#SWITCHES#
optimize = True  # uses more characters, but the output file is bigger
#END SWITCHES#

os.system('if not exist frames mkdir frames && if not exist generated mkdir generated')
os.system('if exist frames cd frames && del /s /q * >nul')
os.system('if exist generated cd generated && del /s /q * >nul')
os.system('if exist output.gif del /s /q output.gif >nul')

layout = [
    [sg.Text('Select a file:'), sg.InputText(key='-FILE-', enable_events=True), sg.FileBrowse()],
    [sg.Checkbox('Optimize', default=optimize, key='-OPTIMIZE-')],
    [sg.Button('Create GIF')]
]

window = sg.Window('GIF Creator', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Create GIF':
        file_path = values['-FILE-']
        optimize = values['-OPTIMIZE-']
        window.close()
        break

# Read the GIF or MP4 file using imageio
frames = imageio.mimread(file_path, memtest=False)
print(f'Extracting {len(frames)} frames.')


def calculate_frame_duration(fps, num_frames):
    frame_duration = 1.0 / fps
    total_duration = frame_duration * num_frames
    return frame_duration


def get_video_fps(file_path):
    total_frames = 0
    total_duration = 0

    # Open the video file using Pillow for GIFs or moviepy for MP4 files
    try:
        if file_path.lower().endswith(".gif"):
            with Image.open(file_path) as img:
                while True:
                    try:
                        # Seek to the next frame
                        img.seek(img.tell() + 1)
                        total_frames += 1
                        total_duration += img.info['duration'] / 1000.0
                    except EOFError:
                        break
        else:
            video_clip = VideoFileClip(file_path)
            total_frames = int(video_clip.fps * video_clip.duration)
            total_duration = video_clip.duration
    except Exception as e:
        print(f"Error: {e}")
        return None

    # Calculate the frames per second (FPS)
    fps = total_frames / total_duration
    return fps

def save_frame(frame, index):
    image = Image.fromarray(frame)
    try:
        image.save(fr'frames\frame{index}.png', optimize=True, quality=100)
    except IndexError:
        print(f'frame {index} broke.')

# Save frames using multithreading
with ThreadPoolExecutor(max_workers=12) as executor:
    for i, frame in enumerate(frames):
        executor.submit(save_frame, frame, i)

files = os.listdir(os.getcwd()+r'\frames')
print(f'Extracted {len(files)} frames.')

def process_frame(item):
    if optimize:
        os.system(f"ascii-image-converter.exe frames\{item} -C -f -s generated --only-save")
    else:
        os.system(f"ascii-image-converter.exe frames\{item} -C -c -f -s generated --only-save")
    with lock:
        global processed_frames
        processed_frames += 1

# Convert frames to ASCII using multithreading
total_frames = len(files)
processed_frames = 0
lock = threading.Lock()

with ThreadPoolExecutor() as executor:
    futures = []
    for item in files:
        future = executor.submit(process_frame, item)
        futures.append(future)

    # Track progress based on completion of individual frames
    progress_bar = tqdm(total=len(frames), desc='Creating GIF')

    while futures:
        for future in futures[:]:
            if future.done():
                futures.remove(future)
                progress_bar.update(1)

    progress_bar.close()

print('\nAll frames processed.')

# PNG to GIF conversion

png_files = os.listdir(os.getcwd()+r'\generated')

frames_data = {}

processed_files = 0

for item in png_files:
    if '.png' in item:
        processed_files += 1
        frame_number = re.sub('[^0-9]', '', item)
        frames_data[frame_number] = item
        progress = processed_files / len(png_files) * 100
        print(f'Reading ASCII files: {progress:.2f}% [{processed_files}/{len(png_files)}]',
             end='\r', flush=True)
    

png_files = []

for x in range(0,len(frames_data)):
    png_files.append(frames_data[str(x)])

frames = [imageio.imread(os.path.join('generated', file)) for file in png_files]

fps = int(get_video_fps(file_path))
frame_duration = calculate_frame_duration(fps, len(frames))
gif_output_path = 'raw.gif'

# Set the loop parameter to 0 for infinite looping
gif_frame_duration = int(frame_duration * 1000)
loop_count = 0

# Create a list of durations with the same length as the frames list
durations = [gif_frame_duration] * len(frames)

# Add infinite loop parameter to the durations list
durations.append(0)

progress_bar = tqdm(total=len(frames), desc='Creating GIF')

def update_progress():
    progress_bar.update(1)

imageio.mimsave(gif_output_path, frames, duration=durations, 
                loop=loop_count, progress_callback=update_progress)
progress_bar.close()

os.system('gifsicle.exe raw.gif --colors 256 -o output.gif')
os.remove('raw.gif')


print(f"GIF saved as output.gif")
time.sleep(2)
os.system('output.gif')
