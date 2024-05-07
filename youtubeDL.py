import os
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube

# Function to handle download button click event
def download_video():
    # Get the YouTube link from the text field
    youtube_link = link_entry.get()
    
    # Get the folder path from the text field
    folder_path = folder_entry.get()
    
    # Get the selected choices (MP3 and MP4)
    mp3_choice = mp3_var.get()
    mp4_choice = mp4_var.get()
    
    # Create a YouTube object
    youtube = YouTube(youtube_link)
    
    # Get the highest available quality stream
    stream = youtube.streams.get_highest_resolution() if mp4_choice else youtube.streams.get_audio_only()
    
    # Create audio and video folders in the selected folder path
    audio_folder = os.path.join(folder_path, "audio")
    video_folder = os.path.join(folder_path, "video")
    
    
    
    # Download the video or audio
    if mp4_choice:
        os.makedirs(audio_folder, exist_ok=True)
        stream.download(output_path=video_folder)
    
    if mp3_choice:
        os.makedirs(video_folder, exist_ok=True)
        stream.download(output_path=audio_folder)
        # Change the file extension to .mp3
        base_filename = os.path.splitext(stream.default_filename)[0]
        new_filename = base_filename + ".mp3"
        os.rename(os.path.join(audio_folder, stream.default_filename), os.path.join(audio_folder, new_filename))
        
    # Update the status label
    update_status("Download completed")
    
# Function to handle the context menu
def show_context_menu(event):
    context_menu.tk_popup(event.x_root, event.y_root)

# Function to handle paste button click event
def paste_from_clipboard():
    clipboard_text = window.clipboard_get()
    link_entry.delete(0, tk.END)
    link_entry.insert(tk.END, clipboard_text)

# Function to handle browse button click event
def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(tk.END, folder_path)
        
# Create a new window
window = tk.Tk()

# Set the window title
window.title("Youtube Downloader")

# Set the window size
window.geometry("300x150")

# Create a label for the YouTube link
link_label = tk.Label(window, text="YouTube Link:")
link_label.grid(row=0, column=0, sticky="w")

# Create a text field for the YouTube link
link_entry = tk.Entry(window)
link_entry.grid(row=0, column=1, padx=5, pady=5)

# Create a label for the folder path
folder_label = tk.Label(window, text="Folder Path:")
folder_label.grid(row=1, column=0, sticky="w")

# Create a text field for the folder path
folder_entry = tk.Entry(window)
folder_entry.grid(row=1, column=1, padx=5, pady=5)

# Create a browse button
browse_button = tk.Button(window, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2, padx=5, pady=5)

# Create two checkboxes for MP3 and MP4 choices
mp3_var = tk.IntVar()
mp3_checkbox = tk.Checkbutton(window, text="MP3", variable=mp3_var)
mp3_checkbox.grid(row=2, column=0)

mp4_var = tk.IntVar()
mp4_checkbox = tk.Checkbutton(window, text="MP4", variable=mp4_var)
mp4_checkbox.grid(row=2, column=1)

# Create a context menu
context_menu = tk.Menu(link_label , tearoff=0)
context_menu.add_command(label="Cut", command=lambda: link_entry.event_generate("<<Cut>>"))
context_menu.add_command(label="Copy", command=lambda: link_entry.event_generate("<<Copy>>"))
context_menu.add_separator()
context_menu.add_command(label="Paste", command=paste_from_clipboard)

# Bind the context menu to the window
window.bind("<Button-3>", show_context_menu)

# Create a download button
download_button = tk.Button(window, text="Download", command=download_video)
download_button.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Create a label for the status
status_label = tk.Label(window, text="")
status_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Function to update the status label
def update_status(message):
    status_label.config(text=message)

# Run the window's event loop
window.mainloop()
