import re
from pathlib import Path

def parse_subtitle_content(file_path):
    """
    ## extracts clean text content from subtitle files
    supports srt, vtt, ass formats
    """
    file_path = Path(file_path)
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    
    if file_path.suffix.lower() == '.srt' or 'srt' in file_path.name:
        return parse_srt(content)
    elif file_path.suffix.lower() == '.vtt' or 'vtt' in file_path.name:
        return parse_vtt(content)
    elif file_path.suffix.lower() in ['.ass', '.ssa'] or 'ass' in file_path.name:
        return parse_ass(content)
    else:
        ## fallback: try to extract any text lines
        return parse_generic(content)

def parse_srt(content):
    """
    ## parses srt format subtitles
    removes sequence numbers and timestamps
    """
    lines = content.strip().split('\n')
    text_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        ## skip sequence numbers
        if line.isdigit():
            i += 1
            continue
            
        ## skip timestamp lines
        if '-->' in line:
            i += 1
            continue
            
        ## collect text content
        if line and not line.isdigit():
            text_lines.append(line)
        
        i += 1
    
    return ' '.join(text_lines)

def parse_vtt(content):
    """
    ## parses vtt format subtitles
    removes webvtt headers and timestamps
    """
    lines = content.strip().split('\n')
    text_lines = []
    
    for line in lines:
        line = line.strip()
        
        ## skip vtt headers
        if line.startswith('WEBVTT') or line.startswith('NOTE'):
            continue
            
        ## skip timestamp lines
        if '-->' in line:
            continue
            
        ## skip empty lines and cue settings
        if not line or line.startswith('<'):
            continue
            
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