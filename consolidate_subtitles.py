import re
from pathlib import Path
from parse_subtitle_content import parse_subtitle_content

def consolidate_subtitles(extracted_files, output_path=None, source_path=None):
    """
    ## combines all subtitle files into one organized document
    creates markdown format with proper course structure
    """
    if output_path is None:
        output_path = Path('formatted.md')
    else:
        output_path = Path(output_path)
    
    ## sort files by course structure
    sorted_files = sort_by_course_structure(extracted_files)
    
    ## extract course name from source path if provided, otherwise from first file
    if source_path:
        course_name = extract_course_name(source_path)
    else:
        course_name = extract_course_name(sorted_files[0]) if sorted_files else "Course"
    
    consolidated_content = []
    consolidated_content.append(f"# {course_name}\n")
    
    current_chapter = None
    
    for file_path in sorted_files:
        ## extract structure info from filename
        chapter, lesson = extract_structure_info(file_path)
        
        ## add chapter heading if new chapter
        if chapter != current_chapter:
            consolidated_content.append(f"\n## {chapter}\n")
            current_chapter = chapter
        
        ## add lesson heading
        consolidated_content.append(f"\n### {lesson}\n")
        
        ## parse and add subtitle content
        try:
            content = parse_subtitle_content(file_path)
            if content.strip() and not content.startswith('[Error'):
                consolidated_content.append(content + "\n")
            elif content.startswith('[Error'):
                consolidated_content.append(content + "\n")
        except Exception as e:
            consolidated_content.append(f"[Error parsing {file_path.name}: {e}]\n")
    
    ## write consolidated file
    final_content = '\n'.join(consolidated_content)
    output_path.write_text(final_content, encoding='utf-8')
    
    return output_path

def sort_by_course_structure(file_paths):
    """
    ## sorts subtitle files by chapter and lesson numbers
    handles various numbering formats
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

def extract_course_name(source_path):
    """
    ## extracts course name from source directory path
    uses the actual course folder name, not output paths
    """
    source_path = Path(source_path) if isinstance(source_path, str) else source_path
    
    ## get the actual course folder name
    course_name = source_path.name
    
    ## clean up the name
    course_name = course_name.replace('_', ' ').replace('-', ' ')
    
    return course_name or "Course"

def extract_structure_info(file_path):
    """
    ## extracts chapter and lesson info from filename
    """
    filename = Path(file_path).stem
    parts = filename.split('_')
    
    chapter = "Unknown Chapter"
    lesson = "Unknown Lesson"
    
    ## look for chapter info (first part with number)
    for i, part in enumerate(parts):
        if re.match(r'\d+', part):
            ## found chapter number, get chapter name
            if i + 1 < len(parts):
                chapter_parts = []
                j = i
                while j < len(parts) and not re.match(r'\d+', parts[j][0:1]) or j == i:
                    chapter_parts.append(parts[j].replace('_', ' '))
                    j += 1
                    if j < len(parts) and re.match(r'\d+', parts[j]):
                        break
                chapter = ' '.join(chapter_parts)
            
            ## look for lesson info after chapter
            for k in range(i + 1, len(parts)):
                if re.match(r'\d+', parts[k]):
                    lesson_parts = parts[k:]
                    lesson = ' '.join(lesson_parts).replace('_', ' ')
                    break
            break
    
    ## clean up names
    chapter = re.sub(r'^(\d+\s*[._-]*\s*)', '', chapter).strip()
    lesson = re.sub(r'^(\d+\s*[._-]*\s*)', '', lesson).strip()
    
    return chapter or "General", lesson or "Lesson"