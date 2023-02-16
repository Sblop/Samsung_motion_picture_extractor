# Samsung_motion_picture_extractor
Samsung motion picture extractor

This is a Python script that splits motion photos taken with Samsung phones and saves the video component as a separate MP4 file.

The script takes one or more arguments, which should be the paths to one or more JPEG files containing motion photos. It first checks if the input file is a .jpg file and if it exists. If the output MP4 file already exists, it will not overwrite it unless the --force option is specified.

The script reads the contents of the input file into a temporary file, seeks the beginning of the file, and stores its contents in a variable. It then searches for a specific marker in the binary data of the file to locate the video component of the motion photo, and writes the video component to a separate MP4 file.

The script then retrieves the creation and modification timestamps of the input file and sets them as the creation and modification timestamps of the output file. Finally, the script checks if the output .mp4 file is valid using ffmpeg, and prints out information on the elapsed time and success of the operation.

The script uses the argparse module to parse command line arguments. The split function is the main function that handles the splitting of the JPEG file. The --force option can be used to overwrite any existing MP4 file.

Run by:

 python split_motion_photo.py /path/example.jpg
 python split_motion_photo.py /path/example.jpg --force 
 find "/share/path/upload" -type f -name "*.jpg" -exec python split_motion_photo.py {} --force \;
