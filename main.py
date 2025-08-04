#!/usr/bin/env python3
import argparse
from pathlib import Path
from find_subtitle_files import find_subtitle_files
from extract_subtitles import extract_subtitles
from consolidate_subtitles import consolidate_subtitles

def main():
    parser = argparse.ArgumentParser(description='Extract subtitle files from nested directories')
    parser.add_argument('source', help='Source directory to search for subtitles')
    parser.add_argument('-o', '--output', help='Output directory (default: extracted_subtitles)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be extracted without copying')
    parser.add_argument('--consolidate', action='store_true', help='Also create consolidated course document')
    
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
    
    print(f"\nExtracting to: {args.output or 'extracted_subtitles'}")
    extracted = extract_subtitles(subtitle_files, args.output)
    print(f"\nSuccessfully extracted {len(extracted)} files")
    
    ## consolidate if requested
    if args.consolidate:
        output_dir = Path(args.output or 'extracted_subtitles')
        consolidated_path = output_dir / 'consolidated_course.md'
        print(f"\nConsolidating subtitles into: {consolidated_path}")
        consolidate_subtitles(extracted, consolidated_path)
        print("Consolidation complete!")

if __name__ == "__main__":
    main()