import shutil
from pathlib import Path
from config import DEFAULT_OUTPUT_DIR

def extract_subtitles(subtitle_files, output_dir=None):
    """
    ## copies subtitle files to output directory
    handles naming conflicts by preserving directory structure in filename
    """
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    extracted_files = []
    
    for file_path in subtitle_files:
        ## create safe filename from course structure only
        relative_path = file_path.parts
        ## find the course folder (skip system path, keep only course structure)
        course_parts = []
        for i, part in enumerate(relative_path):
            if any(char.isdigit() for char in part) or 'chapter' in part.lower():
                course_parts = relative_path[i:]
                break
        if not course_parts:
            course_parts = relative_path[-2:]  # fallback: last folder + filename
        
        safe_filename = '_'.join(course_parts).replace(' ', '_').replace('.', '_')
        
        output_file = output_path / safe_filename
        
        ## handle duplicate filenames
        counter = 1
        original_output = output_file
        while output_file.exists():
            stem = original_output.stem
            suffix = original_output.suffix
            output_file = output_path / f"{stem}_{counter}{suffix}"
            counter += 1
        
        shutil.copy2(file_path, output_file)
        extracted_files.append(output_file)
        print(f"Extracted: {file_path} -> {output_file}")
    
    return extracted_files