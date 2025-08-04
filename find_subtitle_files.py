import os
from pathlib import Path
from config import SUBTITLE_EXTENSIONS

def find_subtitle_files(source_dir):
    """
    ## recursively finds all subtitle files in a directory
    returns list of pathlib.Path objects
    """
    subtitle_files = []
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in SUBTITLE_EXTENSIONS:
                subtitle_files.append(file_path)
    
    return sorted(subtitle_files)