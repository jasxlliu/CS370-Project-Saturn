import tkinter as tk
from tkinter import filedialog
from saturn_cli import CommandLineParser
import threading
import os

class AudioEditorApp:
    def __init__(self, master):
        self.master = master
        master.title("Audio Editor")

        # Get the screen width and height
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Set the window size to match the screen size
        master.geometry(f"{screen_width}x{screen_height}")

        # Set color (can change later).
        master.configure(bg="lightcoral")

        # Initialize the command line parser
        self.command_parser = CommandLineParser([])

        # Create GUI buttons.
        self.play_button = tk.Button(master, text="Play", command=self.play)
        self.play_overlap_button = tk.Button(master, text="Play Overlap", command=self.play_overlap)
        self.play_sequential_button = tk.Button(master, text="Play Sequential", command=self.play_sequential)
        self.browse_button = tk.Button(master, text="Browse Sound Folder", command=self.browse_sound_folder)
        self.song_label = tk.Label(master, text="No song selected", bg="lightcoral", fg="black")
        
        # Layout GUI elements
        self.play_button.pack()
        self.play_overlap_button.pack()
        self.play_sequential_button.pack()
        self.browse_button.pack()
        self.song_label.pack()

        # Store songs to play sequentially
        self.sequential_songs = []

    def browse_sound_folder(self):
        # changed depending on where this gui.py file is placed.
        initial_dir = "../sounds" 
        file_path = filedialog.askopenfilename(initialdir=initial_dir)
        if file_path:
            self.sequential_songs.append(file_path)
            self.song_label.config(text=f"Selected song: {os.path.basename(file_path)}")

    def play(self):
        # checks if we have songs selected for playback.
        if self.sequential_songs:
            # use threading if we select multiple songs.
            threading.Thread(target=self.command_parser.play, args=(self.sequential_songs[0],)).start()
        else:
            print("No song selected.")

    def play_overlap(self):
        # checks if we have songs selected for playback.
        if self.sequential_songs:
            threading.Thread(target=self.command_parser.play_overlap, args=(self.sequential_songs,)).start()
        else:
            print("No song selected.")

    def play_sequential(self):
        # checks if we have songs selected for playback.
        if self.sequential_songs:
            threading.Thread(target=self.command_parser.play_sequential, args=(self.sequential_songs,)).start()
        else:
            print("No song selected.")

def main():
    root = tk.Tk()
    app = AudioEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()