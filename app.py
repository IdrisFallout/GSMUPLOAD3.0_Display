import json
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import threading
import time

root = tk.Tk()
root.title("Media Display")
root.attributes("-fullscreen", True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

label = tk.Label(root)
label.config(bg='black')
label.pack(fill=tk.BOTH, expand=True)

json_path = '../GSMUPLOAD3.0/static/file_path.json'
current_media = None  # To hold the current media reference


def display_media(file_path):
    global current_media
    if current_media is not None:
        label.after_cancel(current_media)  # Cancel previous media display
        label.configure(image=None)  # Clear the label

    if file_path.endswith(('.mp4', '.mov', '.avi')):
        cap = cv2.VideoCapture(file_path)
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = maintain_aspect_ratio(frame)
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            label.configure(image=photo)
            label.image = photo
            current_media = root.after(30, update_video, cap)
    else:
        image = Image.open(file_path)
        image = maintain_aspect_ratio_image(image)
        photo = ImageTk.PhotoImage(image=image)
        label.configure(image=photo)
        label.image = photo

    return current_media


def maintain_aspect_ratio(frame):
    height, width, _ = frame.shape
    aspect_ratio = width / height
    if aspect_ratio > (screen_width / screen_height):
        new_width = screen_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = screen_height
        new_width = int(new_height * aspect_ratio)
    return cv2.resize(frame, (new_width, new_height))


def maintain_aspect_ratio_image(image):
    width, height = image.size
    aspect_ratio = width / height
    if aspect_ratio > (screen_width / screen_height):
        new_width = screen_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = screen_height
        new_width = int(new_height * aspect_ratio)
    return image.resize((new_width, new_height))


def update_video(cap):
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = maintain_aspect_ratio(frame)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        label.configure(image=photo)
        label.image = photo
        root.after(30, update_video, cap)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Move back to the beginning of the video
        update_video(cap)


def get_file_path_from_json():
    with open(json_path, 'r') as file:
        content = file.read()
        json_data = json.loads(content)
        file_path = json_data.get('file_path', '').replace('\\', '/').replace('static/', '../GSMUPLOAD3.0/static/')
    return file_path


def play_initial_media():
    initial_file_path = get_file_path_from_json()
    display_media(initial_file_path)


def check_file_changes():
    global current_media
    prev_modified_time = os.path.getmtime(json_path)
    while True:
        current_modified_time = os.path.getmtime(json_path)
        if current_modified_time != prev_modified_time:
            new_file_path = get_file_path_from_json()
            display_media(new_file_path)
            prev_modified_time = current_modified_time
        time.sleep(1)  # Check every 1 second


# Initial play when the program starts
play_initial_media()

# Start file monitoring in a separate thread
file_monitor_thread = threading.Thread(target=check_file_changes)
file_monitor_thread.daemon = True
file_monitor_thread.start()

# Run the main Tkinter loop
root.mainloop()

############################################
# import json
# import tkinter as tk
# from PIL import Image, ImageTk
# from tkVideoPlayer import TkinterVideo
# import time
# import os
# import threading
#
# root = tk.Tk()
# root.title("Media Display")
# root.attributes("-fullscreen", True)
#
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
#
# player = TkinterVideo(master=root, scaled=True)
# player.config(bg='black')
# player.pack(fill=tk.BOTH, expand=True)
#
# json_path = '../GSMUPLOAD3.0/static/file_path.json'
# current_media = None  # To hold the current media reference
#
#
# def display_media(file_path):
#     global current_media
#     if current_media is not None:
#         player.stop()
#
#     if file_path.endswith(('.mp4', '.mov', '.avi')):
#         player.set_media_file(file_path)
#         player.play()
#     else:
#         image = Image.open(file_path)
#         image = maintain_aspect_ratio_image(image)
#         photo = ImageTk.PhotoImage(image=image)
#         player.config(image=photo)
#         player.image = photo
#
#
# def maintain_aspect_ratio_image(image):
#     width, height = image.size
#     aspect_ratio = width / height
#     if aspect_ratio > (screen_width / screen_height):
#         new_width = screen_width
#         new_height = int(new_width / aspect_ratio)
#     else:
#         new_height = screen_height
#         new_width = int(new_height * aspect_ratio)
#     return image.resize((new_width, new_height))
#
#
# def check_file_changes():
#     prev_modified_time = os.path.getmtime(json_path)
#     while True:
#         current_modified_time = os.path.getmtime(json_path)
#         if current_modified_time != prev_modified_time:
#             with open(json_path, 'r') as file:
#                 content = file.read()
#                 json_data = json.loads(content)
#                 file_path = json_data.get('file_path', '')
#                 file_path = file_path.replace('\\', '/')
#                 file_path = file_path.replace('static/', '../GSMUPLOAD3.0/static/')
#                 print(file_path)
#
#                 # Update media displayed based on the new file_path
#                 display_media(file_path)
#
#             prev_modified_time = current_modified_time
#         time.sleep(1)  # Check every 1 second
#
#
# file_path = "forza5.mp4"
# display_media(file_path)
#
# file_monitor_thread = threading.Thread(target=check_file_changes)
# file_monitor_thread.daemon = True
# file_monitor_thread.start()
#
# root.mainloop()

########################################

# from tkinter import *
# from tkvideo import tkvideo
# import json
# import os
# import time
# import threading
#
# json_path = '../GSMUPLOAD3.0/static/file_path.json'
#
#
# def get_path():
#     with open('../GSMUPLOAD3.0/static/file_path.json', 'r') as f:
#         data = json.load(f)
#     file_path = data.get('file_path').replace('\\', '/')  # Replace backslashes with forward slashes
#     file_path = file_path.replace('static/', '../GSMUPLOAD3.0/static/')
#     return file_path
#
#
# def check_file_changes():
#     prev_modified_time = os.path.getmtime(json_path)
#     while True:
#         current_modified_time = os.path.getmtime(json_path)
#         if current_modified_time != prev_modified_time:
#             with open(json_path, 'r') as file:
#                 content = file.read()
#                 json_data = json.loads(content)
#                 file_path = json_data.get('file_path', '')
#                 file_path = file_path.replace('\\', '/')
#                 file_path = file_path.replace('static/', '../GSMUPLOAD3.0/static/')
#                 print(file_path)
#
#                 # Update media displayed based on the new file_path
#                 display_media(file_path)
#
#             prev_modified_time = current_modified_time
#         time.sleep(1)  # Check every 1 second
#
#
# def display_media(file_path):
#     # global player
#     # player.stop()
#     player.load(file_path, my_label, loop=-1)
#     player.play()
#
#
# root = Tk()
# my_label = Label(root)
# my_label.pack()
# # my_label.config(bg='black')
# player = tkvideo(get_path(), my_label, loop=-1, size=(1280, 720))
# player.play()
#
# file_monitor_thread = threading.Thread(target=check_file_changes)
# file_monitor_thread.daemon = True
# file_monitor_thread.start()
#
# root.mainloop()

########################################

# import json
# import os
# import time
# import vlc
#
# json_path = '../GSMUPLOAD3.0/static/file_path.json'
#
#
# def get_path():
#     with open(json_path, 'r') as f:
#         data = json.load(f)
#     file_path = data.get('file_path').replace('\\', '/')  # Replace backslashes with forward slashes
#     file_path = file_path.replace('static/', '../GSMUPLOAD3.0/static/')
#     return file_path
#
#
# def play_media(file_path):
#     # Specify the path to the libvlc library
#     vlc_path = "C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"  # Replace with the actual path to your VLC installation
#     vlc_instance = vlc.Instance(f'--no-xlib --plugin-path={vlc_path}')
#
#     player = vlc_instance.media_player_new()
#     media = vlc_instance.media_new(file_path)
#     player.set_media(media)
#     player.play()
#     return player
#
#
# def monitor_file_changes():
#     prev_modified_time = os.path.getmtime(json_path)
#     player = None
#
#     while True:
#         current_modified_time = os.path.getmtime(json_path)
#
#         if current_modified_time != prev_modified_time:
#             with open(json_path, 'r') as file:
#                 content = file.read()
#                 json_data = json.loads(content)
#                 file_path = json_data.get('file_path', '')
#                 file_path = file_path.replace('\\', '/')
#                 file_path = file_path.replace('static/', '../GSMUPLOAD3.0/static/')
#                 print(file_path)
#
#                 if player is not None:
#                     player.stop()  # Stop the current playback
#
#                 player = play_media(file_path)  # Play the new media
#
#             prev_modified_time = current_modified_time
#
#         time.sleep(1)  # Check every 1 second for changes
#
#
# if __name__ == "__main__":
#     monitor_file_changes()

########################################

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel
# from PyQt5.QtGui import QPixmap
#
#
# class FullScreenMediaApp(QWidget):
#     def __init__(self, media_path):
#         super().__init__()
#
#         self.media_path = media_path
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Full Screen Media Display')
#
#         # Set up QLabel to display the image
#         self.label = QLabel(self)
#         self.label.setGeometry(0, 0, self.width(), self.height())
#         self.display_media()
#
#         self.showFullScreen()
#
#     def display_media(self):
#         pixmap = QPixmap(self.media_path)
#         self.label.setPixmap(pixmap.scaled(self.label.size(), aspectRatioMode=True))
#
#
# def run_app(media_path):
#     app = QApplication(sys.argv)
#     full_screen_app = FullScreenMediaApp(media_path)
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     # Replace 'YOUR_MEDIA_PATH' with the actual file path of the media you want to display
#     media_path = 'bugatti5.png'
#     run_app(media_path)


########################################
# import json
# import os
# import threading
# import time
#
# json_path = '../GSMUPLOAD3.0/static/file_path.json'
#
#
# def check_file_changes():
#     prev_modified_time = os.path.getmtime(json_path)
#     while True:
#         current_modified_time = os.path.getmtime(json_path)
#         if current_modified_time != prev_modified_time:
#             with open(json_path, 'r') as file:
#                 content = file.read()
#                 json_data = json.loads(content)
#                 file_path = json_data.get('file_path', '')
#                 file_path = file_path.replace('\\', '/')
#                 file_path = file_path.replace('static/', '../GSMUPLOAD3.0/static/')
#
#                 # Update media displayed based on the new file_path
#                 display_media(file_path)
#
#             prev_modified_time = current_modified_time
#         time.sleep(1)  # Check every 1 second
#
#
# def display_media(file_path):
#     print(file_path)
#
#
# if __name__ == "__main__":
#     check_file_changes()
#     # file_monitor_thread = threading.Thread(target=check_file_changes)
#     # file_monitor_thread.daemon = True
#     # file_monitor_thread.start()


########################################

# from tkinter import Tk, Label
# from tkvideo import tkvideo
# import json
# import os
# import time
# import threading
#
# json_path = '../GSMUPLOAD3.0/static/file_path.json'
#
#
# def get_path():
#     with open(json_path, 'r') as f:
#         data = json.load(f)
#     file_path = data.get('file_path', '').replace('\\', '/')  # Replace backslashes with forward slashes
#     file_path = file_path.replace('static/', '../GSMUPLOAD3.0/static/')
#     return file_path
#
#
# def check_file_changes():
#     prev_modified_time = os.path.getmtime(json_path)
#     while True:
#         current_modified_time = os.path.getmtime(json_path)
#         if current_modified_time != prev_modified_time:
#             with open(json_path, 'r') as file:
#                 content = file.read()
#                 json_data = json.loads(content)
#                 file_path = json_data.get('file_path', '')
#                 file_path = file_path.replace('\\', '/')
#                 file_path = file_path.replace('static/', '../GSMUPLOAD3.0/static/')
#                 print(file_path)
#
#                 # Update media displayed based on the new file_path
#                 display_media(file_path)
#
#             prev_modified_time = current_modified_time
#         time.sleep(1)  # Check every 1 second
#
#
# def display_media(file_path):
#     player.load(file_path, my_label, loop=1)
#     player.play()
#
#
# root = Tk()
# root.attributes('-fullscreen', True)  # Make the window fullscreen
# root.overrideredirect(True)  # Remove the title bar
#
# my_label = Label(root)
# my_label.pack(expand=True, fill='both')
#
# player = tkvideo(get_path(), my_label, loop=1, size=(root.winfo_screenwidth(), root.winfo_screenheight()))
# player.play()
#
# file_monitor_thread = threading.Thread(target=check_file_changes)
# file_monitor_thread.daemon = True
# file_monitor_thread.start()
#
# root.mainloop()
