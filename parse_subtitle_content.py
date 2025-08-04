import re
from pathlib import Path

def parse_subtitle_content(file_path):
    """
    ## extracts clean text content from subtitle files
    supports srt, vtt, ass formats with robust edge case handling
    """
    file_path = Path(file_path)
    
    try:
        ## try different encodings
        content = None
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'utf-16']:
            try:
                content = file_path.read_text(encoding=encoding)
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        if content is None:
            return f"[Error: Could not decode {file_path.name}]"
            
        ## detect format and parse
        if file_path.suffix.lower() == '.srt' or 'srt' in file_path.name:
            return parse_srt(content)
        elif file_path.suffix.lower() == '.vtt' or 'vtt' in file_path.name:
            return parse_vtt(content)
        elif file_path.suffix.lower() in ['.ass', '.ssa'] or 'ass' in file_path.name:
            return parse_ass(content)
        else:
            ## fallback: try to extract any text lines
            return parse_generic(content)
            
    except Exception as e:
        return f"[Error parsing {file_path.name}: {str(e)}]"

def parse_srt(content):
    """
    ## parses srt format subtitles with edge case handling
    removes sequence numbers and timestamps, handles multi-line text
    """
    lines = content.strip().split('\n')
    text_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        ## skip empty lines
        if not line:
            i += 1
            continue
            
        ## skip sequence numbers (pure digits)
        if re.match(r'^\d+$', line):
            i += 1
            continue
            
        ## skip timestamp lines (flexible pattern matching)
        if re.search(r'\d{1,2}:\d{2}:\d{2}[,\.]\d{3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[,\.]\d{3}', line):
            i += 1
            continue
            
        ## collect text content (anything that's not timestamp or sequence)
        if line and not re.match(r'^\d+$', line) and '-->' not in line:
            ## handle multi-line text blocks
            text_block = [line]
            j = i + 1
            while j < len(lines) and lines[j].strip() and not re.match(r'^\d+$', lines[j].strip()) and '-->' not in lines[j]:
                text_block.append(lines[j].strip())
                j += 1
            text_lines.append(' '.join(text_block))
            i = j
            continue
        
        i += 1
    
    return ' '.join(text_lines)

def parse_vtt(content):
    """
    ## parses vtt format subtitles with edge case handling
    removes webvtt headers and timestamps, handles cue settings
    """
    lines = content.strip().split('\n')
    text_lines = []
    
    for line in lines:
        line = line.strip()
        
        ## skip empty lines
        if not line:
            continue
            
        ## skip vtt headers and metadata
        if line.startswith(('WEBVTT', 'NOTE', 'STYLE', 'REGION')):
            continue
            
        ## skip timestamp lines - more flexible pattern for VTT format
        if re.search(r'\d{1,2}:\d{2}\.\d{3}\s*-->\s*\d{1,2}:\d{2}\.\d{3}', line):
            continue
        if re.search(r'\d{1,2}:\d{2}:\d{2}[,\.]\d{3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[,\.]\d{3}', line):
            continue
            
        ## skip cue settings and positioning
        if re.match(r'^(align|line|position|size|vertical):', line) or line.startswith('<'):
            continue
            
        ## skip lines that are just numbers (cue identifiers)
        if re.match(r'^\d+$', line):
            continue
            
        ## collect actual text content
        text_lines.append(line)
    
    return ' '.join(text_lines)

def parse_ass(content):
    """
    ## parses ass/ssa format subtitles
    extracts dialogue text only
    """
    lines = content.strip().split('\n')
    text_lines = []
    
    for line in lines:
        line = line.strip()
        
        ## look for dialogue lines
        if line.startswith('Dialogue:'):
            ## dialogue format: Dialogue: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
            parts = line.split(',', 9)
            if len(parts) >= 10:
                dialogue_text = parts[9]
                ## remove ass formatting tags
                dialogue_text = re.sub(r'\{[^}]*\}', '', dialogue_text)
                text_lines.append(dialogue_text.strip())
    
    return ' '.join(text_lines)

def parse_generic(content):
    """
    ## fallback parser for unknown formats
    extracts text lines, skips timestamps
    """
    lines = content.strip().split('\n')
    text_lines = []
    
    for line in lines:
        line = line.strip()
        
        ## skip common subtitle metadata
        if '-->' in line or line.isdigit() or not line:
            continue
            
        text_lines.append(line)
    
    return ' '.join(text_lines)