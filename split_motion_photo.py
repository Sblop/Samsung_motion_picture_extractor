#!/usr/bin/env python3

import sys
import os
import tempfile
import subprocess
from datetime import datetime
import argparse

# Set the search data as a binary string
searchdata = b'\x4D\x6F\x74\x69\x6F\x6E\x50\x68\x6F\x74\x6F\x5F\x44\x61\x74\x61'

def split(input_file, force=False):
    # Check if the input file exists and is a .jpg file
    if not os.path.isfile(input_file):
        print(f"Error: Input file does not exist: {input_file}")
        return False
    if not input_file.lower().endswith('.jpg'):
        print(f"Error: Only .jpg files are supported: {input_file}")
        return False

    # Define output file paths
    base_name, _ = os.path.splitext(input_file)
    output_mp4 = base_name + ".mp4"
    
    # Check if the output file already exists
    if os.path.isfile(output_mp4) and not force:
        print(f"Error: Output file already exists for: {input_file}")
        return False
    
    # Read the contents of the input file into a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        with open(input_file, 'rb') as input:
            temp_file.write(input.read())

        # Seek to the beginning of the file and store its contents in a variable
        temp_file.seek(0)
        data = temp_file.read()

        # Search for the marker in the binary data and split the file
        pos = data.find(searchdata)
        if pos == -1:
            print(f"Error: File does not contain required marker: {input_file}")
            return False

        with open(output_mp4, 'wb') as output:
            output.write(data[pos + len(searchdata):])

        # Get the creation and modification timestamps of the input file
        st = os.stat(input_file)
        create_time = st.st_ctime
        mod_time = st.st_mtime

        # Set the creation and modification timestamps of the output file
        os.utime(output_mp4, (create_time, mod_time))

        # Check if the output .mp4 file is valid
        try:
            subprocess.check_call(['ffmpeg', '-v', 'error', '-fflags', '+genpts', '-i', output_mp4, '-f', 'null', '-'])
        except subprocess.CalledProcessError:
            print(f"Error: Invalid .mp4 file: {output_mp4}")
            os.remove(output_mp4)
            return False

        # Print output info
        print(f"Successfully split {input_file} into {output_mp4}.")
        print(f"Elapsed time: {datetime.now() - start_time}")

    return True


# Record the start time
start_time = datetime.now()

# Parse command line arguments
parser = argparse.ArgumentParser(description='Split .jpg files and create .mp4 files.')
parser.add_argument('input_file', nargs='+', help='The input .jpg file to split')
parser.add_argument('--force', action='store_true', help='Overwrite existing .mp4 file')
args = parser.parse_args()

# Split each .jpg file specified on the command line
for input_file in args.input_file:
    split(input_file, args.force)
