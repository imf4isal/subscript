#!/usr/bin/env python3
import argparse
from pathlib import Path
from find_subtitle_files import find_subtitle_files
from extract_subtitles import extract_subtitles
from consolidate_subtitles import consolidate_subtitles
from create_raw_combined import create_raw_combined

def main():
    parser = argparse.ArgumentParser(description='Extract subtitle files from nested directories')
    parser.add_argument('source', help='Source directory to search for subtitles')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be extracted without copying')
    parser.add_argument('--consolidate', action='store_true', help='Also create consolidated course documents')
    
    args = parser.parse_args()
    
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source directory '{args.source}' does not exist")
        return
    
    print(f"Searching for subtitle files in: {source_path}")
    subtitle_files = find_subtitle_files(source_path)
    
    if not subtitle_files:
        print("No subtitle files found")
        return
    
    print(f"Found {len(subtitle_files)} subtitle files:")
    for file in subtitle_files:
        print(f"  {file}")
    
    if args.dry_run:
        print("\n--dry-run mode: no files were copied")
        return
    
    ## create data directories with course name structure
    course_name = source_path.name.replace(' ', '_').replace('-', '_')
    data_dir = Path('data') / 'output' / course_name
    extracted_dir = data_dir / 'extracted'
    combined_dir = data_dir / 'combined'
    
    extracted_dir.mkdir(parents=True, exist_ok=True)
    if args.consolidate:
        combined_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nExtracting to: {extracted_dir}")
    extracted = extract_subtitles(subtitle_files, extracted_dir)
    print(f"\nSuccessfully extracted {len(extracted)} files")
    
    ## consolidate if requested
    if args.consolidate:
        formatted_path = combined_dir / 'formatted.md'
        raw_path = combined_dir / 'raw.txt'
        
        print(f"\nCreating combined files:")
        print(f"  Formatted: {formatted_path}")
        consolidate_subtitles(extracted, formatted_path, source_path)
        
        print(f"  Raw text: {raw_path}")
        create_raw_combined(extracted, raw_path)
        
        print("Consolidation complete!")

if __name__ == "__main__":
    main()