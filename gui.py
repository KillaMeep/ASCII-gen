# -*- coding: utf-8 -*-

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
from termcolor import colored, cprint
import platform



# SWITCHES #
opengif = True  # opens gif in native viewer when done.
cleanup = True  # file cleaner
fullchar = False  # uses more characters, but the output file is bigger
color = False  # sets color on/off
fullscale = False  # false uses full res, true makes image smaller, lower res
# END SWITCHES #


def deldir(relpath):
    for item in os.listdir(relpath):
        os.remove(f'{relpath}/{item}')
    os.rmdir(relpath)

files = os.listdir(os.getcwd())
for item in ['frames','generated']:
    if item not in files:
        os.makedirs(item)
    else:
        for file in os.listdir(item):
            os.remove(f'{item}/{file}')
for item in ['raw.gif','output.gif']:
    if item in files:
        os.remove(item)

if platform.system() == 'Windows':
    os.system('color')
error = colored('[ERROR]', 'red')
warn = colored('[WARN]', 'yellow')
ok = colored('[OK]', 'cyan')
info = colored('[INFO]', 'green')

layout = [
    [sg.Text('Select a file:'), sg.InputText(key='-FILE-', enable_events=True), sg.FileBrowse()],
    [sg.Checkbox('Open Final Result', default=opengif, key='-GIF-', tooltip='Opens the final result in the native viewer when done.')],
    [sg.Checkbox('Cleanup', default=cleanup, key='-CLEAN-', tooltip='Toggles file cleanup on close. Only turn off if you need the extracted/generated frames.')],
    [sg.Checkbox('Use More Characters', default=fullchar, key='-OPTIMIZE-', tooltip='Uses all available characters. Higher res, much bigger file.')],
    [sg.Checkbox('Use Color', default=color, key='-COLOR-', tooltip='Toggles color generation mode')],
    [sg.Checkbox(u'SMOL\u2122', default=fullscale, key='-FULLSCALE-', tooltip='Makes the images much smaller, better for sharing if full res is not needed.')],
    [sg.Button('Create GIF')],
    [sg.Text('Frame Extraction:', size=(15, 1)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='-FRAME_EXTRACT_PROGRESS-')],
    [sg.Text('ASCII Generation:', size=(15, 1)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='-IMAGE_GEN_PROGRESS-')],
    [sg.Text('GIF Generation:', size=(15, 1)), sg.ProgressBar(100, orientation='h', size=(20, 20), key='-GIF-GEN-')]
]

max_threads = os.cpu_count()
print(info, f'Running with {max_threads} threads.')

window = sg.Window('GIF Creator', layout)




while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Create GIF':
        file_path = values['-FILE-']
        opengif = values['-GIF-']
        cleanup = values['-CLEAN-']
        fullchar = values['-OPTIMIZE-']
        color = values['-COLOR-']
        fullscale = values['-FULLSCALE-']
        window['-FRAME_EXTRACT_PROGRESS-'].Update(0, 100)
        window['-IMAGE_GEN_PROGRESS-'].Update(0, 100)
        window['-GIF-GEN-'].Update(0, 100)
        window.finalize()  # Prevent GUI from closing
        break




commands = '-s generated --only-save'
if not fullscale:
    commands = commands + ' -f'
    print(warn, f'Using FULLSCALE generation command')
if fullchar:
    commands = commands + ' -c'
    print(warn, f'Using FULLCHAR generation command')
if color:
    commands = commands + ' -C'
    print(warn, f'Using COLOR generation command')



if any(item in file_path for item in ['.jpg', '.jpeg', '.png']):
    os.system(f"start /W /B ascii-image-converter.exe {file_path} {commands}")
    png_files = os.listdir(os.getcwd() + r'\generated')
    if len(png_files) == 1:
        new_file = fr'generated\{png_files[0]}'
        os.rename(new_file,r'generated\output.png')
        print(info, r'Saved in generated dir as "output.png"')
    else:
        print(error, 'Image conversion failed.')
        exit(1)
    if opengif:
        print(info, 'Launching viewer.')
        os.system(r'generated\output.png')
        print(ok, 'Launched.')
    print(ok, 'Generation complete! Closing in 5 seconds!')
    time.sleep(5)
    exit(0)

# Read the GIF or MP4 file using imageio
frames = imageio.mimread(file_path, memtest=False)
total_frames = len(frames)
print(info, f'Extracting {total_frames} frames.')

frame_extract_progress_bar = window['-FRAME_EXTRACT_PROGRESS-']
frame_extract_progress_bar.UpdateBar(0, total_frames)


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
        print(error, f"Error: {e}")
        return None

    # Calculate the frames per second (FPS)
    fps = total_frames / total_duration
    return fps


def save_frame(frame, index):
    image = Image.fromarray(frame)
    try:
        image.save(fr'frames\frame{index}.png', optimize=True, quality=100)
    except IndexError:
        print(error, f'frame {index} broke.')

# Save frames using multithreading
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    frame_count = 0
    total_frames = len(frames)

    for i, frame in enumerate(frames):
        executor.submit(save_frame, frame, i)
        frame_count += 1
        frame_extract_progress_bar.UpdateBar(frame_count)

files = os.listdir(os.getcwd() + r'\frames')
extracted_frames = len(files)
print(ok, f'Extracted {extracted_frames} frames.')


def process_frame(item):
    os.system(f"start /W /B ascii-image-converter.exe frames\{item} {commands}")
    global processed_frames
    processed_frames += 1
    # image_gen_progress_bar.UpdateBar(processed_frames)  # Removed


# Convert frames to ASCII using multithreading
processed_frames = 0

with ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = []
    for item in files:
        future = executor.submit(process_frame, item)
        futures.append(future)

    image_gen_progress_bar = window['-IMAGE_GEN_PROGRESS-']
    image_gen_progress_bar.UpdateBar(0, len(files))  # Set the maximum value of the progress bar

    while futures:
        for future in futures[:]:
            if future.done():
                futures.remove(future)
                processed_frames = len(files) - len(futures)  # Calculate the number of processed frames
                image_gen_progress_bar.UpdateBar(processed_frames, len(files))  # Update the progress bar

print(ok, 'All frames processed.')

# PNG to GIF conversion
print(info, 'Starting frame collection')

png_files = os.listdir(os.getcwd() + r'\generated')

frames_data = {}

processed_files = 0

for item in png_files:
    if '.png' in item:
        processed_files += 1
        frame_number = re.sub('[^0-9]', '', item)
        frames_data[frame_number] = item
        progress = processed_files / len(png_files) * 100

png_files = []
gif_progress_bar = window['-GIF-GEN-']
gif_progress_bar.UpdateBar(0, 4)




for x in range(0, len(frames_data)):
    png_files.append(frames_data[str(x)])
gif_progress_bar.UpdateBar(1)
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
print(ok, 'Frame collection complete.')
print(info, 'Saving GIF. This may take a while...')
gif_progress_bar.UpdateBar(2)


imageio.mimsave(gif_output_path, frames, duration=durations,
                loop=loop_count,)
image_gen_progress_bar.UpdateBar(processed_frames)
print(ok, 'GIF created.')
gif_progress_bar.UpdateBar(3)
print(info, 'Optimizing GIF.')
os.system('gifsicle.exe raw.gif --colors 256 -o output.gif')
os.remove('raw.gif')

print(ok, f"GIF optimized and saved as output.gif")

gif_progress_bar.UpdateBar(4)

time.sleep(2)
if opengif:
    print(info, 'Launching GIF viewer.')
    os.system('output.gif')
    print(ok, 'Launched.')
if cleanup:
    print(info, 'Cleaning files.')
    deldir('generated')
    deldir('frames')
    print(ok, 'Files deleted.')
print(ok, 'Generation complete! Closing in 5 seconds!')
time.sleep(5)
