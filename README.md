# Samsung_motion_picture_extractor
Samsung motion picture extractor

I need a tool to extract the motion part of samsung motion pictures, that run on linux
This does just this, and leave the original .jpg file alone.

Run by:

  find "/share/path/upload" -type f -name "*.jpg" -exec python split_motion_photo.py {} \;
