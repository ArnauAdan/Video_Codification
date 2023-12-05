import imageio
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk

class ReproduceVideo:

    def __init__(self, root):

        self.root = root
        self.root.geometry("1000x500")
        self.root.title("Reproductor de Videos")

        self.video_path = "BBB.mp4"
        self.cap = imageio.get_reader(self.video_path)
        self.current_resolution = (self.cap.get_meta_data()['size'][0], self.cap.get_meta_data()['size'][1])

        self.resolution_var = tk.StringVar()
        self.resolution_var.set("Change resolution")
        self.resolution_options = ["720p", "480p", "360x240", "160x120", "Original"]
        self.resolution_menu = ttk.Combobox(root, textvariable=self.resolution_var, values=self.resolution_options)
        self.resolution_menu.pack(padx=10, pady=10)
        self.resolution_menu.bind("<<ComboboxSelected>>", self.change_resolution)

        self.play_button = tk.Button(root, text="Play", command=self.play_video, bg="green", fg="white", font=("Arial", 9), width=8, height=1)
        self.play_button.pack(side=tk.LEFT, pady=10, padx=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_video, bg="green", fg="white", font=("Arial", 9), width=8, height=1)
        self.pause_button.pack(side=tk.LEFT, pady=10)

        self.video_label = tk.Label(root)
        self.video_label.pack(padx=20, pady=20)

        self.is_playing = False

    def play_video(self):
        if not self.is_playing:
            self.is_playing = True
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.play_next_frame()

    def play_next_frame(self):
        if self.is_playing:
            try:
                frame = self.cap.get_next_data()
                frame = Image.fromarray(frame)
                frame = self.resize_video_frame(frame, self.current_resolution[0], self.current_resolution[1])
                frame_image = ImageTk.PhotoImage(frame)
                self.video_label.config(image=frame_image)
                self.video_label.image = frame_image
                self.video_label.lift()
                self.root.after(33, self.play_next_frame)
            except StopIteration:
                self.is_playing = False
                self.play_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.DISABLED)

    def pause_video(self):
        self.is_playing = False
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)

    def change_resolution(self, event):
        selected_resolution = self.resolution_var.get()

        if selected_resolution == "720p":
            self.change_video_resolution(1280, 720)
        elif selected_resolution == "480p":
            self.change_video_resolution(854, 480)
        elif selected_resolution == "360x240":
            self.change_video_resolution(360, 240)
        elif selected_resolution == "160x120":
            self.change_video_resolution(160, 120)
        elif selected_resolution == "Original":
            self.change_video_resolution(self.cap.get_meta_data()['size'][0], self.cap.get_meta_data()['size'][1])

    def change_video_resolution(self, width, height):
        self.current_resolution = (width, height)

    def resize_video_frame(self, frame, max_width, max_height):
        original_width, original_height = frame.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        resized_frame = frame.resize((new_width, new_height))
        return resized_frame


if __name__ == "__main__":
    root = tk.Tk()
    app = ReproduceVideo(root)
    root.mainloop()

