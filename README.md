# Scripts to assist with managing local multimedia files

## Summaries of this suite
1. `chaptersFromYTdescription.py` - Parses the YouTube video description and will make a new copy that contains chapter marks so you can quickly flip through the original timestamps, even on your locally saved copy. It also embeds the description text into the metadata of the new video file.
2. `trackNumberer.py` - If you use youtube-dl or yt-dlp to rip music from BandCamp, this script reformats the filenames to put the track numbers first so they are alphabetized properly.
3. `videochaptermaker.py` - all this does is create a copy of a video with embedded chapter marks. This is different from `chaptersFromYTdescription.py` in that you have to supply your own chapters and timestamps.
4. `videolistculler.py` Helps you quickly sort through a bunch of video files (audio files, too, I guess) and delete the ones you don't want. I use this when I review videos from my game camera to save cool videos of animals and easily delete videos shot when the camera triggered on a tree branch in the wind.

## How to use
Most of these have use instructions in the code comments. Most of them expect that the relevant files are in the pwd when you trigger the script.

### Chapters from YouTube Description
1. If using yt-dlp or youtube-dl, then run the command `$ yt-dlp -f mp4 --write-description <URLHERE>`
2. Don't have other files in the same directory
3. Have ffmpeg installed on your system
4. Run the script.

This one is really handy with educational or "How To" type videos so you can easily skip forward to the part that you want to see.

`-f mp4` option is because YouTube likes to send .webm files and I don't think those support chapter marks. So this will ensure you get the mp4 version downloaded.

`--write-description` will save the video description in a sidecar file. The script expects there to be a file called `*.description` in the same directory (yt-dlp does this by default if you use that option)

### Track Numberer
This works with music downloaded via yt-dlp from Bandcamp. Put all the tracks into their own directory, run the script and follow the prompts.

### Video Chapter Maker
Original script by Kyle Howells ([here](https://ikyle.me/blog/2020/add-mp4-chapters-ffmpeg)). I've made a couple small improvements. Look at the code. There is a pretty good explanation at the end of it. The *Chapters from YouTube Description* script actually uses this script to write the metadata.

### Video List Culler
See instructions in the comments at the top of the code. They are pretty good. Even though it's called Video List Culler, it would work with any media that VLC can play. You basically make a VLC playlist of your media files, and as you review the playlist, delete the stuff you don't want. The script later reads the playlist and will delete the files that are not in the playlist.

Be careful with this one...if you have **any files** in the same folder that are not in the playlist, then this script will nuke them also.
