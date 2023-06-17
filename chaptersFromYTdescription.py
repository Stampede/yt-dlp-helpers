#!/usr/bin/env python3
# chaptersFromYT.py - parses Youtube video description to format the text for
# encoding chapter marks into the video metadata.
# June 17, 2023

# USAGE: Put video file in its own directory, along with a text file containing the video description.
# The video file should be in an mp4 container. Video description filename needs a *.description extension
# EXAMPLE yt-dlp command to do this: $ yt-dlp --write-description -f mp4 https://www.youtube.com/watch?v=xxx

# TODO: add something to the wrangle_description function that will exit the program if the regex
#       fails to match any timestamps. Currently, the program crashes if regex fails to match timestamps.
#       Maybe even give user the option to still write the description to the video metadata even if
#       there are no chapters

# Also TODO: Put video destription text that comes after the timestamps in the metadata as well.

from pathlib import Path
import re, datetime, subprocess, shutil
import videochaptermaker

def check_4_chapters_file():
    if (Path.cwd() / 'chapters.txt').exists():
        print("There's an existing chapters.txt file. Exiting.")
        exit(1)

def check_4_name_and_description():
    descriptions = list(Path.cwd().glob('*.description'))
    if len(descriptions) != 1:
        print('There needs to be one file whose name ends with ".description".')
        print('That is not the case. Good bye.')
        exit(1)
    else:
        shutil.copy(descriptions[0], 'description.txt')

    
    mp4_files = list(Path.cwd().glob('*.mp4'))
    if len(mp4_files) != 1:
        print('There should be one .mp4 file in this directory.')
        print('That is not the case. Good bye.')
        exit(1)
    else:
        return(mp4_files[0])

def wrangle_description():
    # The chapter embedding script needs a chapters.txt file specifically formatted like this:
    # [H]H:MM:SS <Some Chapter Title>
    # Much of this function is making sure it gets formatted that way.

    def convert_to_dto(entire_ts):
        hms = [int(x) for x in entire_ts.split(':')]
        while len(hms) < 3:   # add hours and minutes in if they are not there yet
            hms.insert(0, 0)
        return datetime.datetime(*((1900, 1, 1) + tuple(hms)))  # Give it a fake date so time delta addition works.

    with open('description.txt', 'r') as f:
        desc_text = f.read()

    timestamp_regex = r'^((?:\d:)?\d{1,2}:\d{2})(?:\W+)(\w.+)'
        # Group 1 is the timestamp
        # Group 2 is the chapter title

    matches = re.finditer(timestamp_regex, desc_text, re.MULTILINE)
    chapters = []
    for matchNum, match in enumerate(matches, start=1):
        if matchNum == 1:
            timestamps_beginning = match.start()
        timestamp = convert_to_dto(match.group(1))
        chapters.append([timestamp, match.group(2)])
        last_timestamp = timestamp
        timestamps_ending = match.end()
    
    chapters.sort(key=lambda x: x[0])   # put timestamps in chronological order, otherwise ffmpeg gets angry

    # chapters.txt file need a final chapter even tho it's not actually recorded to metadata
    dummy_time = last_timestamp + datetime.timedelta(seconds=5)
    chapters.append([dummy_time, "ending chapter (placeholder)"])
    
    for i, _ in enumerate(chapters):
        chapters[i][0] = chapters[i][0].strftime("%H:%M:%S")
        chapters[i] = ' '.join(chapters[i]) + '\n'

    with open('chapters.txt', 'w') as f:
        f.writelines(chapters)

    # Function returns the video description but truncates the timestamps and everything that follows them
    #return(desc_text[:timestamps_beginning].strip(",.:\n "))
    return(desc_text[:timestamps_beginning])

def add_description_to_mdatafile(contents):
    contents = contents.replace('\n', '\\\n')
    with open('FFMETADATAFILE', 'a') as f:
        f.write('\n')
        f.write(f'comment={contents}')
    Path('description.txt').unlink()
    return None
    
def apply_metadata(original_video):
    yes_responses = ('y', 'yes')
    no_responses = ('n', 'no', 'q', 'quit', 'exit')
    valid_responses = yes_responses + no_responses

    response = 'Praise Jesus!'
    print()
    print("""
    A metadata file has been created that will be used to embed chapter timestamps and descriptions.
    Do you want to create the new video file now? If you want to change the chapters and timestamps,
    you should say no and manually edit chapters.txt""")
    
    while response not in valid_responses:
        response = input('Create new video now? ')
        response = response.lower()
    
    ffmpeg_cmd = ['ffmpeg', '-i', original_video, '-i', 'FFMETADATAFILE', 
                  '-map_metadata', '1', '-codec', 'copy', 'OUTPUT_WITH_CHAPTERS.mp4']
    
    print()
    if response in yes_responses:
        videochaptermaker.main()    # edits the metadata file to add chapter information
        subprocess.run(ffmpeg_cmd)
        print()
        print('A new video file has been created. ', end='')

    elif response in no_responses:
        print('* When you are satisfied with chapters.txt, you will have to run the videochaptermaker.py script and then')
        print('run ffmpeg yourself to apply changes.\nInscrutions for the videochaptermaker script are written in the comments at the end of the script.')
        print()


def main():
    check_4_chapters_file()
    input_f = check_4_name_and_description()

    # Create the starting ffmetadata file:
    subprocess.run(['ffmpeg', '-i', str(input_f), '-f', 'ffmetadata', 'FFMETADATAFILE'])

    description = wrangle_description() # this function also creates a chapters.txt file
    add_description_to_mdatafile(description)
    
    apply_metadata(str(input_f.name))
    print('Good bye.')


if __name__ == '__main__':
    main()