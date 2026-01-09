# -*- coding: utf-8 -*-
"""
ASCII Art Generator - Convert images and videos to ASCII art
Uses tkinter for GUI (free and built into Python)
"""

import time
import os
import threading
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import Tk, Label, Entry, Button, Checkbutton, BooleanVar, StringVar, Frame, filedialog, messagebox
from tkinter.ttk import Progressbar, Style
from PIL import Image
try:
    # moviepy 1.x
    from moviepy.editor import VideoFileClip
except ImportError:
    # moviepy 2.x
    from moviepy import VideoFileClip
import imageio
from termcolor import colored
import platform


class ASCIIGenerator:
    """Main application class for ASCII art generation from images/videos."""
    
    # Default settings
    DEFAULT_SETTINGS = {
        'open_result': True,      # Opens result in native viewer when done
        'cleanup': True,          # File cleaner
        'full_char': False,       # Uses more characters (bigger output)
        'color': False,           # Color mode on/off
        'full_scale': False,      # False = full res, True = smaller/lower res
        'export_mp4': False,      # Export as MP4 in addition to GIF
    }
    
    SUPPORTED_IMAGE_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    SUPPORTED_VIDEO_FORMATS = ('.gif', '.mp4', '.avi', '.mov', '.webm')

    def __init__(self):
        self.system = platform.system()
        self.max_threads = os.cpu_count() or 4
        self.processing = False
        self.setup_directories()
        self.setup_console()
        self.setup_gui()
        
    def setup_directories(self):
        """Create necessary directories and clean up old files."""
        for directory in ['frames', 'generated']:
            os.makedirs(directory, exist_ok=True)
            # Clean existing files
            for file in os.listdir(directory):
                try:
                    os.remove(os.path.join(directory, file))
                except OSError:
                    pass
        
        # Remove old output files
        for old_file in ['raw.gif', 'output.gif']:
            if os.path.exists(old_file):
                try:
                    os.remove(old_file)
                except OSError:
                    pass

    def setup_console(self):
        """Setup console colors for Windows."""
        if self.system == 'Windows':
            os.system('color')
        
        self.error = colored('[ERROR]', 'red')
        self.warn = colored('[WARN]', 'yellow')
        self.ok = colored('[OK]', 'cyan')
        self.info = colored('[INFO]', 'green')
        
        print(f'{self.info} Running on {self.system}')
        print(f'{self.info} Running with {self.max_threads} threads.')

    def setup_gui(self):
        """Initialize the GUI components."""
        self.root = Tk()
        self.root.title('ASCII Art Generator')
        self.root.resizable(False, False)
        self.root.configure(bg='#2b2b2b')
        
        # Configure style for ttk widgets
        style = Style()
        style.theme_use('clam')
        style.configure('TProgressbar', 
                       background='#4CAF50',
                       troughcolor='#404040',
                       borderwidth=0,
                       lightcolor='#4CAF50',
                       darkcolor='#4CAF50')
        
        # Variables
        self.file_path = StringVar()
        self.open_result = BooleanVar(value=self.DEFAULT_SETTINGS['open_result'])
        self.cleanup_var = BooleanVar(value=self.DEFAULT_SETTINGS['cleanup'])
        self.full_char = BooleanVar(value=self.DEFAULT_SETTINGS['full_char'])
        self.color_var = BooleanVar(value=self.DEFAULT_SETTINGS['color'])
        self.full_scale = BooleanVar(value=self.DEFAULT_SETTINGS['full_scale'])
        self.export_mp4 = BooleanVar(value=self.DEFAULT_SETTINGS['export_mp4'])
        
        # Main frame with padding
        main_frame = Frame(self.root, bg='#2b2b2b', padx=20, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        # File selection row
        file_frame = Frame(main_frame, bg='#2b2b2b')
        file_frame.pack(fill='x', pady=(0, 15))
        
        Label(file_frame, text='Select a file:', bg='#2b2b2b', fg='white', 
              font=('Segoe UI', 10)).pack(side='left')
        
        self.file_entry = Entry(file_frame, textvariable=self.file_path, width=40,
                               font=('Segoe UI', 9), bg='#404040', fg='white',
                               insertbackground='white', relief='flat')
        self.file_entry.pack(side='left', padx=(10, 5), ipady=5)
        
        browse_btn = Button(file_frame, text='Browse', command=self.browse_file,
                           bg='#4CAF50', fg='white', relief='flat', 
                           font=('Segoe UI', 9, 'bold'), cursor='hand2',
                           activebackground='#45a049', activeforeground='white')
        browse_btn.pack(side='left', ipadx=10, ipady=3)
        
        # Checkboxes frame
        checkbox_frame = Frame(main_frame, bg='#2b2b2b')
        checkbox_frame.pack(fill='x', pady=(0, 15))
        
        checkboxes = [
            (self.open_result, 'Open Final Result', 
             'Opens the final result in the native viewer when done'),
            (self.cleanup_var, 'Cleanup Files', 
             'Toggles file cleanup on close. Turn off to keep extracted/generated frames'),
            (self.full_char, 'Use More Characters', 
             'Uses all available characters. Higher res, much bigger file'),
            (self.color_var, 'Use Color', 
             'Toggles color generation mode'),
            (self.full_scale, 'SMOL™', 
             'Makes images smaller, better for sharing if full res not needed'),
            (self.export_mp4, 'Export as MP4', 
             'Also export video as MP4 format (in addition to GIF)'),
        ]
        
        for var, text, tooltip in checkboxes:
            cb = Checkbutton(checkbox_frame, text=text, variable=var,
                           bg='#2b2b2b', fg='white', selectcolor='#404040',
                           activebackground='#2b2b2b', activeforeground='white',
                           font=('Segoe UI', 9), cursor='hand2')
            cb.pack(anchor='w', pady=2)
            self.create_tooltip(cb, tooltip)
        
        # Create button
        self.create_btn = Button(main_frame, text='Create ASCII Art', 
                                command=self.start_processing,
                                bg='#2196F3', fg='white', relief='flat',
                                font=('Segoe UI', 11, 'bold'), cursor='hand2',
                                activebackground='#1976D2', activeforeground='white')
        self.create_btn.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Progress bars frame
        progress_frame = Frame(main_frame, bg='#2b2b2b')
        progress_frame.pack(fill='x')
        
        # Create progress bars
        def create_progress_row(label_text):
            row = Frame(progress_frame, bg='#2b2b2b')
            row.pack(fill='x', pady=5)
            Label(row, text=label_text, bg='#2b2b2b', fg='white',
                  font=('Segoe UI', 9), width=16, anchor='w').pack(side='left')
            progress = Progressbar(row, length=250, mode='determinate')
            progress.pack(side='left', padx=(5, 0))
            return progress
        
        self.frame_progress = create_progress_row('Frame Extraction:')
        self.ascii_progress = create_progress_row('ASCII Generation:')
        self.gif_progress = create_progress_row('GIF Generation:')
        
        # Status label
        self.status_label = Label(main_frame, text='Ready', bg='#2b2b2b', 
                                  fg='#888888', font=('Segoe UI', 9))
        self.status_label.pack(pady=(15, 0))

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget."""
        def show_tooltip(event):
            tooltip = Tk()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            
            label = Label(tooltip, text=text, bg='#ffffe0', fg='black',
                         relief='solid', borderwidth=1, font=('Segoe UI', 8),
                         padx=5, pady=2)
            label.pack()
            
            widget._tooltip = tooltip
            
        def hide_tooltip(event):
            if hasattr(widget, '_tooltip'):
                widget._tooltip.destroy()
                del widget._tooltip
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def browse_file(self):
        """Open file dialog to select input file."""
        filetypes = [
            ('All Supported', '*.gif *.mp4 *.jpg *.jpeg *.png *.bmp *.webp *.avi *.mov *.webm'),
            ('Images', '*.jpg *.jpeg *.png *.bmp *.webp'),
            ('Videos/GIFs', '*.gif *.mp4 *.avi *.mov *.webm'),
            ('All Files', '*.*'),
        ]
        filename = filedialog.askopenfilename(
            title='Select an image or video',
            filetypes=filetypes
        )
        if filename:
            self.file_path.set(filename)

    def update_status(self, text, color='#888888'):
        """Update status label safely from any thread."""
        self.root.after(0, lambda: self.status_label.configure(text=text, fg=color))

    def update_progress(self, progress_bar, value, maximum=100):
        """Update progress bar safely from any thread."""
        self.root.after(0, lambda: progress_bar.configure(value=value, maximum=maximum))

    def reset_progress_bars(self):
        """Reset all progress bars to 0."""
        for bar in [self.frame_progress, self.ascii_progress, self.gif_progress]:
            bar.configure(value=0, maximum=100)

    def get_commands(self):
        """Build command line arguments for ascii-image-converter."""
        commands = ['-s', 'generated', '--only-save']
        
        if not self.full_scale.get():
            commands.append('-f')
            print(f'{self.warn} Using FULLSCALE generation command')
        
        if self.full_char.get():
            commands.append('-c')
            print(f'{self.warn} Using FULLCHAR generation command')
        
        if self.color_var.get():
            commands.append('-C')
            print(f'{self.warn} Using COLOR generation command')
        
        return ' '.join(commands)

    def delete_directory(self, rel_path):
        """Delete a directory and its contents."""
        try:
            for item in os.listdir(rel_path):
                os.remove(os.path.join(rel_path, item))
            os.rmdir(rel_path)
        except OSError as e:
            print(f'{self.error} Failed to delete {rel_path}: {e}')

    def start_processing(self):
        """Start the processing in a background thread."""
        file_path = self.file_path.get().strip()
        
        if not file_path:
            messagebox.showerror('Error', 'Please select a file first!')
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror('Error', 'Selected file does not exist!')
            return
        
        if self.processing:
            messagebox.showwarning('Warning', 'Processing already in progress!')
            return
        
        self.processing = True
        self.create_btn.configure(state='disabled', bg='#666666')
        self.reset_progress_bars()
        
        # Start processing in background thread
        thread = threading.Thread(target=self.process_file, args=(file_path,), daemon=True)
        thread.start()

    def process_file(self, file_path):
        """Main processing function - runs in background thread."""
        try:
            file_lower = file_path.lower()
            
            # Check if it's an image or video
            if any(file_lower.endswith(ext) for ext in self.SUPPORTED_IMAGE_FORMATS):
                self.process_image(file_path)
            elif any(file_lower.endswith(ext) for ext in self.SUPPORTED_VIDEO_FORMATS):
                self.process_video(file_path)
            else:
                self.update_status('Unsupported file format!', '#ff6b6b')
                messagebox.showerror('Error', 'Unsupported file format!')
                return
                
        except Exception as e:
            print(f'{self.error} {str(e)}')
            self.update_status(f'Error: {str(e)}', '#ff6b6b')
            messagebox.showerror('Error', f'An error occurred: {str(e)}')
        finally:
            self.processing = False
            self.root.after(0, lambda: self.create_btn.configure(
                state='normal', bg='#2196F3'))

    def process_image(self, file_path):
        """Process a single image file."""
        self.update_status('Processing image...', '#4CAF50')
        commands = self.get_commands()
        
        # Run ascii-image-converter
        if self.system == 'Windows':
            os.system(f'start /W /B ascii-image-converter.exe "{file_path}" {commands}')
        else:
            os.system(f'ascii-image-converter "{file_path}" {commands}')
        
        self.update_progress(self.frame_progress, 100)
        self.update_progress(self.ascii_progress, 100)
        self.update_progress(self.gif_progress, 100)
        
        # Check output
        png_files = os.listdir('generated')
        if len(png_files) >= 1:
            new_file = os.path.join('generated', png_files[0])
            output_file = os.path.join('generated', 'output.png')
            if new_file != output_file:
                os.rename(new_file, output_file)
            print(f'{self.info} Saved in generated dir as "output.png"')
            
            if self.open_result.get():
                print(f'{self.info} Launching viewer.')
                if self.system == 'Windows':
                    os.startfile(output_file)
                else:
                    os.system(f'xdg-open "{output_file}"')
            
            self.update_status('Image conversion complete!', '#4CAF50')
        else:
            self.update_status('Image conversion failed!', '#ff6b6b')
            print(f'{self.error} Image conversion failed.')

    def process_video(self, file_path):
        """Process a video/GIF file."""
        self.update_status('Extracting frames...', '#4CAF50')
        
        # Read frames
        try:
            frames = imageio.mimread(file_path, memtest=False)
        except Exception as e:
            raise Exception(f'Failed to read video file: {e}')
        
        total_frames = len(frames)
        print(f'{self.info} Extracting {total_frames} frames.')
        
        # Extract frames with threading
        self.extract_frames(frames, total_frames)
        
        # Process frames to ASCII
        self.update_status('Generating ASCII art...', '#4CAF50')
        frame_files = os.listdir('frames')
        self.convert_frames_to_ascii(frame_files)
        
        # Create GIF
        self.update_status('Creating GIF...', '#4CAF50')
        self.create_gif(file_path)
        
        # Cleanup
        if self.cleanup_var.get():
            print(f'{self.info} Cleaning files.')
            self.delete_directory('generated')
            self.delete_directory('frames')
            print(f'{self.ok} Files deleted.')
        
        self.update_status('Generation complete!', '#4CAF50')
        print(f'{self.ok} Generation complete!')

    def extract_frames(self, frames, total_frames):
        """Extract frames from video with multithreading."""
        def save_frame(frame, index):
            try:
                image = Image.fromarray(frame)
                image.save(f'frames/frame{index}.png', optimize=True, quality=100)
            except Exception as e:
                print(f'{self.error} Frame {index} failed: {e}')
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for i, frame in enumerate(frames):
                future = executor.submit(save_frame, frame, i)
                futures.append(future)
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                self.update_progress(self.frame_progress, completed, total_frames)
        
        print(f'{self.ok} Extracted {len(os.listdir("frames"))} frames.')

    def convert_frames_to_ascii(self, frame_files):
        """Convert extracted frames to ASCII art."""
        commands = self.get_commands()
        total_files = len(frame_files)
        processed = [0]  # Use list for mutable counter in nested function
        lock = threading.Lock()
        
        def process_frame(item):
            if self.system == 'Windows':
                os.system(f'start /W /B ascii-image-converter.exe "frames/{item}" {commands}')
            else:
                os.system(f'ascii-image-converter "frames/{item}" {commands}')
            
            with lock:
                processed[0] += 1
                self.update_progress(self.ascii_progress, processed[0], total_files)
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(process_frame, item) for item in frame_files]
            
            # Wait for all to complete
            for future in as_completed(futures):
                pass
        
        print(f'{self.ok} All frames processed.')

    def get_video_fps(self, file_path):
        """Get the FPS of a video file."""
        try:
            if file_path.lower().endswith('.gif'):
                total_frames = 0
                total_duration = 0
                
                with Image.open(file_path) as img:
                    while True:
                        try:
                            img.seek(img.tell() + 1)
                            total_frames += 1
                            total_duration += img.info.get('duration', 100) / 1000.0
                        except EOFError:
                            break
                
                return total_frames / total_duration if total_duration > 0 else 10
            else:
                video_clip = VideoFileClip(file_path)
                fps = video_clip.fps
                video_clip.close()
                return fps
        except Exception as e:
            print(f'{self.warn} Could not determine FPS: {e}. Using default 10 FPS.')
            return 10

    def create_gif(self, original_file_path):
        """Create the output GIF from processed frames."""
        print(f'{self.info} Starting frame collection')
        self.update_progress(self.gif_progress, 0, 4)
        
        png_files = os.listdir('generated')
        frames_data = {}
        
        for item in png_files:
            if item.endswith('.png'):
                frame_number = re.sub('[^0-9]', '', item)
                if frame_number:
                    frames_data[int(frame_number)] = item
        
        # Sort frames by number
        sorted_files = [frames_data[i] for i in sorted(frames_data.keys())]
        self.update_progress(self.gif_progress, 1, 4)
        
        # Load frames
        frames = [imageio.imread(f'generated/{file}') for file in sorted_files]
        
        # Calculate timing
        fps = self.get_video_fps(original_file_path)
        frame_duration = 1.0 / fps if fps > 0 else 0.1
        gif_frame_duration = int(frame_duration * 1000)
        
        print(f'{self.ok} Frame collection complete. FPS: {fps:.2f}')
        print(f'{self.info} Saving GIF. This may take a while...')
        self.update_progress(self.gif_progress, 2, 4)
        
        # Create durations list
        durations = [gif_frame_duration] * len(frames)
        
        # Save raw GIF
        imageio.mimsave('raw.gif', frames, duration=durations, loop=0)
        print(f'{self.ok} GIF created.')
        self.update_progress(self.gif_progress, 3, 4)
        
        # Optimize with gifsicle
        print(f'{self.info} Optimizing GIF.')
        if self.system == 'Windows':
            os.system('gifsicle.exe raw.gif --colors 256 -o output.gif')
        else:
            os.system('gifsicle raw.gif --colors 256 -o output.gif')
        
        # Cleanup raw file
        if os.path.exists('raw.gif'):
            os.remove('raw.gif')
        
        print(f'{self.ok} GIF optimized and saved as output.gif')
        self.update_progress(self.gif_progress, 4, 4)
        
        # Create MP4 if requested
        if self.export_mp4.get():
            print(f'{self.info} Creating MP4 version...')
            try:
                # Use imageio to create MP4
                imageio.mimsave('output.mp4', frames, fps=fps, codec='libx264', quality=8)
                print(f'{self.ok} MP4 created and saved as output.mp4')
            except Exception as e:
                print(f'{self.warn} MP4 creation failed: {e}')
                print(f'{self.info} Trying alternative method...')
                try:
                    # Alternative: use ffmpeg directly via imageio-ffmpeg
                    imageio.mimsave('output.mp4', frames, fps=fps, 
                                  format='FFMPEG', codec='libx264', 
                                  ffmpeg_params=['-pix_fmt', 'yuv420p'])
                    print(f'{self.ok} MP4 created successfully')
                except Exception as e2:
                    print(f'{self.error} MP4 creation failed: {e2}')
        
        # Open result if requested
        if self.open_result.get():
            print(f'{self.info} Launching GIF viewer.')
            if self.system == 'Windows':
                os.startfile('output.gif')
            else:
                os.system('xdg-open "output.gif"')
            print(f'{self.ok} Launched.')
            
            # Also open MP4 if it was created
            if self.export_mp4.get() and os.path.exists('output.mp4'):
                print(f'{self.info} Launching MP4 viewer.')
                if self.system == 'Windows':
                    os.startfile('output.mp4')
                else:
                    os.system('xdg-open "output.mp4"')
                print(f'{self.ok} Launched.')

    def run(self):
        """Start the application."""
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')
        
        self.root.mainloop()


def main():
    """Main entry point."""
    app = ASCIIGenerator()
    app.run()


if __name__ == '__main__':
    main()
