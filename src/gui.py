import tkinter as tk


class AudioEditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sound Archive App")
        self.root.geometry("800x600")
        self.root.configure(bg="lightblue")

        # Create frames for all our pages we drew on the whiteboard.
        self.home_frame = tk.Frame(self.root)
        self.playlist_frame = tk.Frame(self.root)
        self.edit_frame = tk.Frame(self.root)

        self.f_names = [self.home_frame, self.playlist_frame, self.edit_frame]

        # Initialize the start screen
        self.home_screen()
        self.root.mainloop()

    def home_screen(self):
        self.clear_frames()

        # Pack the home frame into the root window
        self.home_frame.pack()

        # Add a button to open the next page.
        button = tk.Button(self.home_frame, text="Open", command=self.playlist_screen)
        button.pack()

    def playlist_screen(self):
        self.clear_frames()

        # Pack the playlist frame into the root window
        self.playlist_frame.pack()

        # Add a button to open the new page
        # TODO: create a button for every playlist we have. For now, I left kinda a default hard coded value.
        button = tk.Button(
            self.playlist_frame,
            text="My Library",
            command=self.songs_in_playlist_screen,
        )
        button.pack()

        # Define our back button back to the home
        back_button = tk.Button(
            self.playlist_frame, text="Go Back", command=self.home_screen
        )
        back_button.pack()

    def songs_in_playlist_screen(self):
        self.clear_frames()
        # TODO: Placeholder action for now
        print("Displaying songs in the playlist...")

    def clear_frames(self):
        # Destroy widgets in all frames
        for frame in self.f_names:
            for widget in frame.winfo_children():
                widget.destroy()


if __name__ == "__main__":
    app = AudioEditorApp()
