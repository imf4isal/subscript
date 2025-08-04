from pathlib import Path
import re

def create_raw_combined(extracted_files, output_path=None):
    """
    ## creates raw file with original subtitle content including timestamps
    preserves file titles and sequential order with timestamps
    """
    if output_path is None:
        output_path = Path('raw.txt')
    else:
        output_path = Path(output_path)
    
    ## sort files by course structure
    sorted_files = sort_by_course_structure(extracted_files)
    
    raw_content = []
    
    for file_path in sorted_files:
        try:
            ## extract lesson title from filename
            lesson_title = extract_lesson_title(file_path)
            raw_content.append(f"=== {lesson_title} ===\n")
            
            ## read original subtitle content with timestamps
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            if content.strip():
                raw_content.append(content.strip() + "\n")
            
        except Exception as e:
            raw_content.append(f"[Error reading {file_path.name}: {e}]\n")
    
    ## combine all content
    final_content = '\n'.join(raw_content)
    
    ## write raw file
    output_path.write_text(final_content, encoding='utf-8')
    
    return output_path

def extract_lesson_title(file_path):
    """
    ## extracts clean lesson title from filename
    """
    filename = Path(file_path).stem
    
    ## remove file extension indicators
    title = filename.replace('_vtt', '').replace('_srt', '').replace('_ass', '')
    
    ## convert underscores to spaces and clean up
    title = title.replace('_', ' ').replace('  ', ' ')
    
    ## remove leading numbers and dots
    title = re.sub(r'^\d+\s*[._-]*\s*', '', title)
    
    return title.strip() or "Unknown Lesson"

def sort_by_course_structure(file_paths):
    """
    ## sorts subtitle files by chapter and lesson numbers
    reused from consolidate_subtitles.py
    """
    def extract_sort_key(file_path):
        filename = Path(file_path).name
        
        ## extract chapter and lesson numbers
        chapter_match = re.search(r'(\d+)', filename)
        chapter_num = int(chapter_match.group(1)) if chapter_match else 999
        
        ## look for lesson number after chapter
        lesson_match = re.search(r'_(\d+)_', filename)
        lesson_num = int(lesson_match.group(1)) if lesson_match else 999
        
        return (chapter_num, lesson_num, filename)
    
    return sorted(file_paths, key=extract_sort_key)