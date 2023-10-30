########################################################################################################################################################
#               LAB 2 - VIDEO CODIFICATION              ARNAU ADAN I SOLÀ           NIA: 24201
########################################################################################################################################################

## Here we put the needed imports
import subprocess
import re
import os
import ffmpeg
import cv2
import requests

###########################
###### 1. MP2 to MP4 ######
###########################

"""""
MP4is a widely used digital multimedia container format that is capable of storing audio, video, 
and even subtitles in a single file. 
It was developed as a standard for multimedia compression and is part of the MPEG-4 standard.
AVI is an older multimedia container format developed by Microsoft. 
It's a common format for storing audio and video data in a single file. 
INPUT:
    - input: path of the video 
OUTPUT:
    - print('...'): if the converstion was succesful or not
    - return None: if it is not possible to open the path with ffmpeg
 """""  

def MP4toAVI(input):
    try: 
        # Extract the base file name (without extension) from the input path
        input_name = os.path.basename(input)
        input_name_without_extension = os.path.splitext(input_name)[0]
        # Construct the output file name with "_toAVI.avi" extension
        output_name = f"{input_name_without_extension}_toAVI.avi"
        # Then we declare the comand
        comand = f'ffmpeg "{input}" -i "{output_name}"'
        # Now we execute the corresponding comand 
        result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # Wait for the process to complete
        result.wait()
        # Return is the result was successful
        if result.returncode == 0:
            print('Succesful conversion')
        else :
            print('Conversion failed')

    # If we can't read the input file 
    except Exception as e:
        return None

######################################
###### 2. CHANGE THE RESOLUTION ######
######################################

"""""
Change the resolution is to change the amount of pixel projected in the screen.
In order to complete it, we can use the current width and height of the video and change it.
This function perform the resoltuion change using ffmpeg libary. 
INPUT:
    - input: the video path
    - resolution_factor: the factor do you want to change the resolution
OUTPUT:
    - print('...'): if the converstion was succesful or not
    - return None: if it is not possible to open the path with ffmpeg
"""""  

# This function scale by a factor the .mp4 video input changing the resolution
def changeResolution(input, resolution_factor):
    try:
        # Using the ffmpeg library to read the input 
        probe = ffmpeg.probe(input, v='error', select_streams='v:0', show_entries='stream=width,height')
        # Take from ffmpeg information the resolution and divide by the factor
        width = int(probe['streams'][0]['width'] / resolution_factor)
        height = int(probe['streams'][0]['height'] /resolution_factor)

        # Name of the output
        output = f"{input}_resolution_{width}x{height}.mp4"

        # Declare the needed comand to implement the resolution change of the ffmpeg
        comand = f'ffmpeg -i {input} -vf "scale={width}:{height}" {output}'

        # Now we execute the corresponding comand 
        result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result.wait()

        # Check if the resolution change was successful
        if result.returncode == 0:
            print('Succesful resolution changed')
        else:
            print('Resolution changed failed')

    # If we can't read the input file 
    except Exception as e:
        return None


###################################
###### 3. CHROMA SUBSAMPLING ######
###################################

"""""
Chroma Subsampling is a digital compression technique that change the color stored form of every pixel. 
FFmpeg uses pixel formats to define how color information is encoded, so we have this three common pixel formats:
    1. 'yuv420p': U and V channels are subsampled horizontally and vertically,
    2. 'yuv422p': U and V channels are subsampled horizontally, but not vertically.
    3. 'yuv444p': where there is no subsampling, and every pixel has full color information.
INPUT:
    - input: path of the video
    - format: one of the 3 formats above
OUTPUT:
    - print('...'): if the converstion was succesful or not
    - return None: if it is not possible to open the path with ffmpeg
"""""  

def chromaSubsampling(input, format):
    try:
       # Construct the FFmpeg command to change the chroma subsampling and save the new video
        output = f"{input}_chromaSubsampled_{format}.mp4"
        # Using the ffmpeg library to read the input 
        comand = f'ffmpeg -i {input} -vf "format={format}" {output}'
        # Now we execute the corresponding comand 
        result = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result.wait()

        # Check if the chroma subsampled was successful
        if result.returncode == 0:
            print('Succesful chroma subsampled')
        else:
            print('Chroma subsampled failed')

    # If we can't read the input file 
    except Exception as e:
        return None
    

###################################
######  4. 5 RELEVANT DATA   ######
###################################

"""""
Using the ffmpeg libary we can know some data from the video read. 
This function returns 5 selected data from the input video:
    1. Video Duration
    2. Video Resolution
    3. Video Codec
    4. Frame Rate
    5. Bitrate
    6. Audio information
    7. Container Format
    8. File Size
INPUT:
    Data needed to start the function is an array of different data selected and 
    the input path.
OUTPUT:
    dataArray dictionary related every data selected with their own data.
"""""  

def relevantData(input, dataArray):
    try:
        # Generate the correspoding comand
        comand = f'ffmpeg -i {input} -hide_banner -loglevel error'
        # Execute the comand
        run = subprocess.Popen(comand, stderr=subprocess.PIPE, text=True)
        # Capture output
        output, _ = run.communicate()
    
        # We incilize an empty dictionary for the data
        dictionary_data = {}

        # Iterate into the dataArray for every data
        for data in dataArray:

            # Depending on the asked data
            if (data == 'Video Duration'):
                # Use regular expressions to extract the video duration
                duration_match = re.search(r"Duration: (\d+:\d+:\d+\.\d+)", output)
                # Add to dictionary if is possible to find the duration
                if duration_match:
                    duration = duration_match.group(1)
                    dictionary_data['Video Duration'] = duration
                else:
                    dictionary_data['Video Duration'] = 'DURATION NOT FOUND'

            if (data == 'Video Resoltuion'):
                # Use regular expressions to extract the video resolution
                resolution_match = re.search(r"Stream #0:0.* (\d+)x(\d+)", output)
                if resolution_match:
                    # As in the previous exercice ask for the width and the height
                    width = int(resolution_match.group(1))
                    height = int(resolution_match.group(2))
                    dictionary_data['Video Resolution'] = width + ':' + height
                else:
                    dictionary_data['Video Resolution'] = 'RESOLUTION NOT FOUND'
                
            if (data == 'Video Codec'):
                # Use regular expressions to extract the video codec
                codec_match = re.search(r"Stream #0:0: Video: ([\w]+)", output)
                if codec_match:
                    # Add to dictionary if it is possible to find the video codec
                    video_codec = codec_match.group(1)
                    dictionary_data['Video Codec'] = video_codec
                else:
                    dictionary_data['Video Codec'] = 'VIDE CODEC NOT FOUND'
                
            if (data == 'Frame Rate'):
                # Use regular expressions to extract the frame rate
                frame_rate_match = re.search(r"Stream #0:0: Video: .*? (\d+(\.\d+)? fps,", output)
                if frame_rate_match:
                    # Add to dictionary if it is possible to find the frame rate
                    frame_rate = frame_rate_match.group(1)
                    dictionary_data['Frame Rate'] = frame_rate
                else:
                    dictionary_data['Frame Rate'] = 'FRAME RATE NOT FOUND'
                
            if (data == 'Bitrate'):
                # Use regular expressions to extract the video bitrate
                bitrate_match = re.search(r"bitrate: (\d+) kb/s", output)
                if bitrate_match:
                    # Add to dictionary if it is possible to find the bitrate
                    bitrate = int(bitrate_match.group(1))
                    dictionary_data['Bitrate'] = bitrate
                else:
                    dictionary_data['Bitrate'] = 'BITRATE NOT FOUND'
                
            if (data == 'Audio information'):
                # Use regular expressions to extract audio information
                audio_stream_regex = re.compile(r"Stream #0:\d.*Audio: (\w+), (\d+) Hz, (\d+) channels, (\d+) kb/s")
                audio_streams = audio_stream_regex.findall(output)

                if audio_streams:
                    # Empty dictionary for every audio information
                    audio_info = {}
                    # Iterate into the audio information and generate a diciontary with the information
                    for i, stream in enumerate(audio_streams):
                        audio_info[f"Audio Stream {i + 1}"] = {
                            "Codec": stream[0],
                            "Sample Rate": int(stream[1]),
                            "Channels": int(stream[2]),
                            "Bitrate": int(stream[3]),
                        }

                    dictionary_data['Audio information'] = audio_info
                else:
                    dictionary_data['Audio information'] = 'AUDIO INFO NOT FOUND'
                
            if (data == 'Container Format'):
                # Use regular expressions to extract the container format
                format_match = re.search(r"Input #0, (\w+),", output)
                if format_match:
                    # Add to dictionary if it is possible to find the container format
                    container_format = format_match.group(1)
                    dictionary_data['Container Format'] = container_format
                else:
                    dictionary_data['Container Format'] = 'CONATINER FORMAT NOT FOUND'
                
            if (data == 'File Size'):
                # Use regular expressions to extract the file size information
                file_size_match = re.search(r"size=\s*(\d+)kB", output)
                if file_size_match:
                    # Add to the dictionary the File size in bytes
                    file_size_kb = int(file_size_match.group(1))
                    # Convert kilobytes to bytes
                    file_size_bytes = file_size_kb * 1024
                    dictionary_data['File Size'] = file_size_bytes
                else:
                    dictionary_data['File Size'] = 'FILE SIZE NOT FOUND'
                
            else :
                dictionary_data[data] = 'UNAVAILABLE INFORMATION'

        # Return the dictionary  
        return dictionary_data
    
    # If we can't read the input file 
    except Exception as e:
        return None


#######################################
######  5. INTERACITON WITH P1   ######
#######################################

"""""
To achive the inherete the previous python script,
the next function call the Git repository and return a variable to use one of these 
function available on the previous one:
    1. 
INPUT:
    - empty
OUTPUT:
    - script_content
"""""  

def interactionP1():
    github_url = f'https://github.com/ArnauAdan/Video_Codification/blob/main/P1JPEGMPEG-1.py'
    response = requests.get(github_url)

    if response.status_code == 200:
        script_content = response.text
        # You can use script_content in your code
        return script_content
    else:
        return None

if __name__ == '__main__':

    # First we declare for all the exercices the proposed video
    input_mp4 = 'Desktop/BBB.mp4'

    ###########################
    ###### 1. MP2 to MP4 ######
    ###########################
    
    MP4toAVI(input_mp4)

    ######################################
    ###### 2. CHANGE THE RESOLUTION ######
    ######################################

    resolution_factor = 2
    changeResolution(input_mp4, resolution_factor)

    ###################################
    ###### 3. CHROMA SUBSAMPLING ######
    ###################################

    format = 'yuv422p'
    chromaSubsampling(input_mp4, format)
        
    ###################################
    ######  4. 5 RELEVANT DATA   ######
    ###################################

    dataArray = ['Video Duration', 'Video Resolution', 'Video Codec', 'Frame Rate', 'Bitrate']
    relevantData(input_mp4, dataArray)
    
    #######################################
    ######  5. INTERACITON WITH P1   ######
    #######################################

    script_content = interactionP1()
    
    # Let's show the 
    if script_content:
        try:
            # Execute the script content within a separate namespace
            namespace = {}
            exec(script_content, namespace)

            # Check if the RGBtoYUV function exists in the namespace
            if 'RGBtoYUV' in namespace:
                # Now you can call the RGBtoYUV function from the downloaded script
                rgb_array = [1, 2, 3]  # Replace with your RGB array
                yuv_array = namespace['RGBtoYUV'](rgb_array)
                # Now you can use yuv_array in your code
            else:
                print("RGBtoYUV function not found in the script.")
        except Exception as e:
            print(f"An error occurred while executing the script: {e}")
        else:
            print("Failed to download script content.")
    