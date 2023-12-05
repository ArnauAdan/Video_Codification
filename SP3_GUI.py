import imageio
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk

class ReproduceVideos:

    def __init__(self, root):

        self.root = root
        self.root.attributes('-fullscreen', True)  # Establecer la ventana en pantalla completa
        self.root.title("Reproductor de Videos")

        self.root.overrideredirect(True)

        # TITLE
        title_label = tk.Label(root, text="SP3 MY VIDEO PLAYER", font=("Times New Roman", 18), fg="red")
        title_label.grid(row=0, column=0, columnspan=3, sticky=tk.N, padx=10, pady=10)

        # CLOSE BUTTON
        close_button = tk.Button(root, text="X", command=root.destroy, font=("Times New Roman", 18), bg="red")
        close_button.grid(row=0, column=2, sticky=tk.NE, padx=10, pady=10)

        ######## FIRST SCREEN PROJECTED ########

        video_frame1 = tk.Frame(root)
        video_frame1.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.video_path1 = "BBB.mp4"
        self.cap1 = imageio.get_reader(self.video_path1)
        self.original_resolution1 = (self.cap1.get_meta_data()['size'][0], self.cap1.get_meta_data()['size'][1])
        self.is_playing1 = False

        self.resolution_var1 = tk.StringVar()# Var change_resolution
        self.resolution_var1.set("Change resolution")
        self.resolution_options1 = ["720p", "480p", "360x240", "160x120", "Original"]
        self.resolution_menu1 = ttk.Combobox(video_frame1, textvariable=self.resolution_var1,
                                             values=self.resolution_options1)
        self.resolution_menu1.grid(row=0, column=0, padx=10, pady=10)
        self.resolution_menu1.bind("<<ComboboxSelected>>",
                                   lambda event: self.change_resolution(self.cap1, self.video_label1,
                                                                        self.resolution_var1))

        self.format_var1 = tk.StringVar()# Change format
        self.format_var1.set("Choose the format")
        self.format_options1 = ["VP8", "VP9", "h265", "AV1"]
        self.format_menu1 = ttk.Combobox(video_frame1, textvariable=self.format_var1,
                                         values=self.format_options1)
        self.format_menu1.grid(row=1, column=0, padx=10, pady=10)

        self.play_button1 = tk.Button(video_frame1, text="Play", command=lambda: self.play_video(self.cap1),
                                      bg="green", fg="white", font=("Arial", 9), width=8, height=1)
        self.play_button1.grid(row=1, column=0, padx=10, pady=10)

        self.pause_button1 = tk.Button(video_frame1, text="Pause", command=lambda: self.pause_video(self.cap1),
                                       bg="green", fg="white", font=("Arial", 9), width=8, height=1)
        self.pause_button1.grid(row=2, column=0, padx=10, pady=10)

        self.video_label1 = tk.Label(video_frame1)
        self.video_label1.grid(row=1, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")

        ######## SECOND SCREEN PROJECTED ########

        video_frame2 = tk.Frame(root)
        video_frame2.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.video_path2 = "BBB.mp4"
        self.cap2 = imageio.get_reader(self.video_path2)
        self.original_resolution2 = (self.cap2.get_meta_data()['size'][0], self.cap2.get_meta_data()['size'][1])
        self.is_playing2 = False

        self.resolution_var2 = tk.StringVar()
        self.resolution_var2.set("Change resolution")
        self.resolution_options = ["720p", "480p", "360x240", "160x120", "Original"]
        self.resolution_menu2 = ttk.Combobox(video_frame2, textvariable=self.resolution_var2,
                                             values=self.resolution_options)
        self.resolution_menu2.grid(row=0, column=0, padx=10, pady=10)
        self.resolution_menu2.bind("<<ComboboxSelected>>",
                                   lambda event: self.change_resolution(self.cap2, self.video_label2,
                                                                        self.resolution_var2))

        self.play_button2 = tk.Button(video_frame2, text="Play", command=lambda: self.play_video(self.cap2),
                                      bg="green", fg="white", font=("Arial", 9), width=8, height=1)
        self.play_button2.grid(row=1, column=0, padx=10, pady=10)

        self.pause_button2 = tk.Button(video_frame2, text="Pause", command=lambda: self.pause_video(self.cap2),
                                       bg="green", fg="white", font=("Arial", 9), width=8, height=1)
        self.pause_button2.grid(row=2, column=0, padx=10, pady=10)

        self.video_label2 = tk.Label(video_frame2)
        self.video_label2.grid(row=1, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(1, weight=1)

    def play_video(self, video_reader):

        if video_reader == self.cap1 and not self.is_playing1:
            self.is_playing1 = True
            self.play_button1.config(state=tk.DISABLED)
            self.pause_button1.config(state=tk.NORMAL)
            self.play_next_frame(video_reader, self.video_label1)
        elif video_reader == self.cap2 and not self.is_playing2:
            self.is_playing2 = True
            self.play_button2.config(state=tk.DISABLED)
            self.pause_button2.config(state=tk.NORMAL)
            self.play_next_frame(video_reader, self.video_label2)

    def resize_video_frame(self, frame, max_width, max_height):
        original_width, original_height = frame.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        resized_frame = frame.resize((new_width, new_height))
        return resized_frame

    def play_next_frame(self, video_reader, video_label):

        if video_reader == self.cap1 and self.is_playing1:
            try:
                frame = video_reader.get_next_data()
                frame = Image.fromarray(frame)
                frame = self.resize_video_frame(frame, 500, 300)
                frame_image = ImageTk.PhotoImage(frame)
                video_label.config(image=frame_image)
                video_label.image = frame_image
                video_label.lift()
                self.root.after(33, lambda: self.play_next_frame(video_reader, video_label))
            except StopIteration:
                self.is_playing1 = False
                self.play_button1.config(state=tk.NORMAL)
                self.pause_button1.config(state=tk.DISABLED)
        elif video_reader == self.cap2 and self.is_playing2:
            try:
                frame = video_reader.get_next_data()
                frame = Image.fromarray(frame)
                frame = self.resize_video_frame(frame, 500, 300)
                frame_image = ImageTk.PhotoImage(frame)
                video_label.config(image=frame_image)
                video_label.image = frame_image
                video_label.lift()
                self.root.after(33, lambda: self.play_next_frame(video_reader, video_label))
            except StopIteration:
                self.is_playing2 = False
                self.play_button2.config(state=tk.NORMAL)
                self.pause_button2.config(state=tk.DISABLED)

    def pause_video(self, video_reader):

        if video_reader == self.cap1:
            self.is_playing1 = False
            self.play_button1.config(state=tk.NORMAL)
            self.pause_button1.config(state=tk.DISABLED)
        elif video_reader == self.cap2:
            self.is_playing2 = False
            self.play_button2.config(state=tk.NORMAL)
            self.pause_button2.config(state=tk.DISABLED)

    def change_resolution(self, video_reader, video_label, resolution_var):
        selected_resolution = resolution_var.get()

        if selected_resolution == "720p":
            self.change_video_resolution(video_reader, video_label, 1280, 720)
        elif selected_resolution == "480p":
            self.change_video_resolution(video_reader, video_label, 854, 480)
        elif selected_resolution == "360x240":
            self.change_video_resolution(video_reader, video_label, 360, 240)
        elif selected_resolution == "160x120":
            self.change_video_resolution(video_reader, video_label, 160, 120)
        elif selected_resolution == "Original":
            if video_reader == self.cap1:
                self.change_video_resolution(video_reader, video_label, *self.original_resolution1)
            elif video_reader == self.cap2:
                self.change_resolution(video_reader, video_label, *self.original_resolution2)

    def change_video_resolution(self, video_reader, video_label, width, height):
        output_params = ["-vf", f"scale={width}:{height}"]

        if video_reader == self.cap1:
            self.pause_video(self.cap1)
            self.cap1 = imageio.get_reader(self.video_path1, output_params=output_params)
            self.play_video(self.cap1)
        elif video_reader == self.cap2:
            self.pause_video(self.cap2)
            self.cap2 = imageio.get_reader(self.video_path2, output_params=output_params)
            self.play_video(self.cap2)


if __name__=="__main__":
    root = tk.Tk()
    app = ReproduceVideos(root)
    root.mainloop()