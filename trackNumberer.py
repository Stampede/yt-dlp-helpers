#! /usr/bin/env python3
# trackNumberer.py - for numbering tracks for albums ripped from Bandcamp
# Run Script from directory containing the tracks. Script will show the track name and prompt for track number, then rename file.
# January 24, 2023 Edition

from pathlib import Path
import pyinputplus as pyip

#musicdir = Path('/home/bobo/Downloads/2 months to live/Music/Froglord/Amphibian Ascending')
#dirlist = list(musicdir.glob('*'))

dirlist = list(Path.cwd().glob('*'))
zeropad = 0 if len(dirlist) < 10 else 1

track_numbers = set()  # Will use this to ensure that same no. ain't entered twice.
renamers = []   #will contain tuples: (old path, new filename)

print()
print('This script assumes that the only files in this directory are tracks from the same album.')


for song in dirlist:    
    track_number = 666
    orig_name = song.name
    extension = song.suffix
    song_title = song.name.split('-')[1].strip()
    
    new_fname = song_title + extension
    track_number = pyip.inputInt(prompt=f'Enter track number for {new_fname}. Or blank to skip: ', blank=True, min=1)
    if track_number == '': continue
    if track_number in track_numbers:
        raise Exception('You already used that track number.')
    track_numbers.add(track_number)
        
    new_fname = str(track_number).zfill(zeropad) + ' - ' + new_fname
    renamers.append((song, new_fname))

for oldpath, newname in renamers:
    oldpath.rename(newname)

print()
print('Good bye.')
