import subprocess
import os

class ChangeResolution:

    def __init__(self, input_path):
        self.path = input_path
        self.output_directory = "output_folder_SP3_Arnau_Adan" # Generate a folder to save the videos
        os.makedirs(self.output_directory, exist_ok=True) # Prove that does not exist yet

    def change_resolution_and_codec(self, string_resolution, string_codec):
        """
        Chance the resolution and the codec of the BBB audio.

        INPUT:
            string_resolution (str): possible options ('720p', '480p', '360x240', '160x120').
            string_codec (str): possible options ('vp8', 'vp9', 'h265', 'AV1', 'mp4').

        OUTPUT:
            Save the video in the folder output_folder_SP3_Arnau_Adan.
        """
        # Here we generate two different dictionaries with the possible options
        dic_resolution = {'720p': [1280, 720], '480p': [854, 480], '360x240': [360, 240], '160x120': [160, 120]}
        dic_codec = {'vp8': '.webm', 'vp9': '.webm', 'h265': '.mp4', 'AV1': 'mkv', 'mp4': '.mp4'}

        # Break the function if the input is incorrect
        if string_resolution not in dic_resolution:
            raise ValueError("Wrong resolution option")

        if string_codec not in dic_codec:
            raise ValueError("Wrong codec option")

        output_filename = os.path.join(self.output_directory, f"BBB_{string_resolution}_resolution{dic_codec[string_codec]}")

        command = [
            "ffmpeg",
            "-i", self.path,
            "-c:v", string_codec,
            "-c:a", "aac", # Needed audio codec
            "-b:a", "394k",
            "-ar", "48000",
            "-ac", "6",
            "-vf", f"scale={dic_resolution[string_resolution][0]}:{dic_resolution[string_resolution][1]}",
            output_filename
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ffmpeg execution error: {e}")

    def divde_screen_vp8_vp9(self):
        """
        Download video with two different screens of the same video, one using vp8 codec
        and the other vp9 codec.

        INPUT:
            There is no needed input

        OUTPUT:
            Save the video in the folder output_folder_SP3_Arnau_Adan.
        """

        output_filename = os.path.join(self.output_directory, "vp8_vp9.mkv")

        command = [
            'ffmpeg',
            "-i", self.path,
            "-i", self.path,
            "-filter_complex", # Let us divide in two different screens
            "[0:v]pad=iw*2:ih[bg]; [bg][1:v]overlay=w",
            "-c:v:0", "vp8",
            "-b:v:0", "1M",
            "-c:v:1", "vp9",
            "-b:v:1", "2M",
            "-c:a", "aac",
            "-b:a", "394k",
            "-ar", "48000",
            "-ac", "6",
            "-s", "1280x720",
            "-map", "0",  # Mapp the flux on the screen
            "-map", "1",
            output_filename
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ffmpeg execution error: {e}")

if __name__ == "__main__":
    cr = ChangeResolution(input_path="BBB.mp4")
    #cr.change_resolution_and_codec('480p', 'vp8')
    #cr.divde_screen_vp8_vp9()

