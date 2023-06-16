#!/usr/ben/env python3
# videochaptermaker.py - modify an FFMPEG metadata file to add user-defined chapters.
# Adapted from a script by Kyle Howells. Original Source: https://ikyle.me/blog/2020/add-mp4-chapters-ffmpeg

# See usage instructions at end of this file.
# June 8, 2023 edition

import re

def main():
   chapters = list()

   with open('chapters.txt', 'r') as f:
      for line in f:
         x = re.match(r"(\d{1,2}):(\d{2}):(\d{2}) (.*)", line)
         hrs = int(x.group(1))
         mins = int(x.group(2))
         secs = int(x.group(3))
         title = x.group(4)

         minutes = (hrs * 60) + mins
         seconds = (minutes * 60) + secs
         timestamp = (seconds * 1000)
         chap = {
            "title": title,
            "startTime": timestamp
         }
         chapters.append(chap)

   text = ""

   for i in range(len(chapters)-1):
      chap = chapters[i]
      title = chap['title']
      start = chap['startTime']
      end = chapters[i+1]['startTime']-1
      text += f"""
[CHAPTER]
TIMEBASE=1/1000
START={start}
END={end}
title={title}
"""


   with open("FFMETADATAFILE", "a") as myfile:
      myfile.write(text)

if __name__ == '__main__':
   main()

"""
How it works:
It expects to be in the same directory as a 'chapters.txt' file to read from, and an 'FFMETADATAFILE' file to output to.
It expects the chapters.txt file to be a txt file with 1 chapter per line starting with 0:00:00 style time stamps and followed by the title of the chapter
It appends to an existing FFMETADATAFILE
It expects no existing chapters in the file
It expects an final END chapter which is ignored, but provides the end point for the last real chapter.

Example chapters.txt:

0:00:00 Introduction
0:40:30 First Performance
0:40:56 Break
1:04:44 Second Performance
1:24:45 Crowd Shots
1:27:45 Credits
1:29:33 Dummy End Chapter (As this is at the end, it will not show up in VLC, so just set it 1-2 seconds short of the total video length)

These timestamps are for the START of the chapter. Remember to put a dummy chapter at the very end

HOW TO USE:
Get existing video metadata:

$ ffmpeg -i INPUT.mp4 -f ffmetadata FFMETADATAFILE

Verify that there are no existing chapters in the FFMETADATAFILE.
Watch the video, noting chapters into a chapters.txt file as you go.
Place FFMETADATAFILE, chapters.txt, and the video file in the same directory.

Run the helper script to append chapters to FFMETADATAFILE.

Create a new video, copying the video and audio from the original without re-encoding.

ffmpeg -i INPUT.mp4 -i FFMETADATAFILE -map_metadata 1 -codec copy OUTPUT.mp4
"""