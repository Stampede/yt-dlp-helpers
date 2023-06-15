#!/usr/bin/python3

# videolistculler.py - a script to quickly cull out media files

# HOW TO USE:
# When you have a lot of media files and many of them are junk, put them in 
# 1 directory and create a VLC playlist of all of the files.
# As you watch/listen to them, delete them from your playlist if they suck. Save the VLC playlist when done.
# 
# Run this script from that directory. It will parse the .xspf file (the VLC playlist)
# and delete any FILES in the directory that are not in the playlist.

from pathlib import Path
from bs4 import BeautifulSoup
from os import sys
from urllib.parse import unquote
import pyinputplus as pyip

folder_list = list(Path.cwd().resolve().glob('*'))

# Initialize the keeper file list with the VLC playlist file itself.
files_to_keep = [x for x in folder_list if x.suffix.lower() == '.xspf']

print()

if len(files_to_keep) == 0:
    print('Did not find a .xspf playlist file. Exiting.', 'Good bye.', sep='/n')
    sys.exit(1)

elif len(files_to_keep) > 1:
    print('Found more than one .xspf playlist file:')
    for _ in files_to_keep: print(_.name)
    print()
    print('Can only accept 1 of those. Good bye.')
    sys.exit(1)

with open(files_to_keep[0], 'r') as f:
    soup = BeautifulSoup(f, 'lxml-xml')

'''
find_all picks everything in the XML file with the location tag. x.text turns that
from a BS4 object into a string. [7: slices] the "file://" characters off the front
of the string wich should be an absolute path, which we then turn into a Path object
'''
files_to_keep += [Path(unquote(x.text)[7:]).resolve() for x in soup.find_all('location')]

files_to_delete = [x for x in folder_list if (x.is_file()) and (x not in files_to_keep)]

if len(files_to_delete) == 0:
    raise Exception('Did not find anything to delete.')

for deletion in files_to_delete: print(deletion.name)

print(); print()
print(f'Working directory: {Path.cwd()}')
print(f'The {len(files_to_delete)} files above will be permanently deleted.')
print()

keep_going = pyip.inputYesNo(prompt='Do you want to continue? ', limit=3, default='no')

if keep_going == 'yes':
    for deletion in files_to_delete: deletion.unlink()
    print('Files deleted. ', end='')

print('Good bye.')
