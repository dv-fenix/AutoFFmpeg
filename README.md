# AutoFFmpeg
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![build](https://img.shields.io/circleci/project/github/badges/shields/master)

A tool to automatically generate and debug ffmpeg commands using natural language queries. Generation powered by ChatGPT, debugging by GPT-3.

## Setup

1) Clone this repository.  
   `git clone https://github.com/dv-fenix/AutoFFmpeg.git`  
   `cd AutoFFmpeg`
   
2) Install the requirements given in `requirements.txt`.  
   `python -m pip install -r requirements.txt`

3) Alias the python command for ease of use
    `alias ffmpeg_app='/usr/bin/python <path to ffmpeg_app.py>'`

## Usage

1) Generate and add your OpenAI API key in the `.env` file.

2) Add the input files to the root directory.

3) Call the ffmpeg_app. An example is provided below:
    ```
    fmpeg_app --request "Concatenate the two videos side by side, then increase the contrast of the first video by 25%." --input_files video_a.mp4 video_b.mp4 --preview
    ```

## Example Output
Original video input

![ Alt text](samples/sample.gif)

Natural language request: "Increase the contrast of the video by 75%" <br>
Output ffmpeg command: `ffmpeg -i sample.gif -vf eq=contrast=1.75 output.gif` 

Output video

![ Alt text](samples/video_a_contrast.gif)