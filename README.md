# Make-Note 🎓

Extract and consolidate video course subtitles into study-ready documents. Transform scattered subtitle files into organized study materials perfect for AI-powered note generation.

## Features ✨

- **🔍 Smart Extraction**: Recursively finds subtitle files in any nested directory structure
- **📝 Dual Output**: Generates both clean markdown and timestamped raw text
- **🎯 Multiple Formats**: Supports SRT, VTT, ASS, SSA, SUB, SBV, TTML, and more
- **🧠 LLM-Ready**: Clean formatted output perfect for ChatGPT, Claude, or other AI tools
- **📁 Organized Output**: Course-specific directories with logical structure
- **⚡ Edge Case Handling**: Robust parsing for malformed subtitles, encoding issues, multi-line blocks
- **🎨 Clean Naming**: Intelligent course and lesson name extraction

## Quick Start 🚀

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/make-note.git
   cd make-note
   ```

2. **Install Python 3.6+** (if not already installed)

3. **Run the tool**
   ```bash
   python3 main.py "/path/to/your/course/folder" --consolidate
   ```

### Basic Usage

Extract subtitles from a course folder:
```bash
# Basic extraction (individual files only)
python3 main.py "/Users/john/Downloads/Python Course"

# Full processing with consolidated output
python3 main.py "/Users/john/Downloads/Python Course" --consolidate

# Preview what would be extracted
python3 main.py "/Users/john/Downloads/Python Course" --dry-run
```

## Output Structure 📁

The tool creates organized output in the `data/output/` directory:

```
data/
└── output/
    └── Python_Course/
        ├── combined/
        │   ├── formatted.md    # Clean text for LLM processing
        │   └── raw.txt         # Original subtitles with timestamps
        └── extracted/
            ├── 01_Introduction_1_Welcome.srt
            ├── 01_Introduction_2_Setup.srt
            └── ... (all individual subtitle files)
```

## Output Formats 📋

### 1. Formatted Markdown (`formatted.md`)
Clean, structured document perfect for AI processing:
```markdown
# Python Course

## Introduction

### Welcome

Welcome to this comprehensive Python course. In this lesson we'll cover...

### Course Setup

Let's start by setting up your development environment...
```

### 2. Raw Text (`raw.txt`)
Original subtitles with timestamps preserved:
```
=== Introduction 1 Welcome ===

WEBVTT

00:00.150 --> 00:02.460
Welcome to this comprehensive Python course.

00:02.460 --> 00:10.710
In this lesson we'll cover the fundamental concepts...
```

## Supported Formats 🎬

| Format | Extension | Description |
|--------|-----------|-------------|
| SubRip | `.srt` | Most common subtitle format |
| WebVTT | `.vtt` | Web standard, used by YouTube |
| Advanced SubStation Alpha | `.ass/.ssa` | Feature-rich with styling |
| MicroDVD | `.sub` | Frame-based timing |
| YouTube | `.sbv` | YouTube's simple format |
| TTML | `.ttml` | XML-based format |
| Scenarist | `.scc` | Closed captions |
| Others | `.stl/.sup/.idx/.usf` | Various proprietary formats |

## Command Options 🛠️

```bash
python3 main.py <source_directory> [options]
```

### Options:
- `--consolidate`: Create consolidated markdown and raw text files
- `--dry-run`: Preview what files would be extracted without copying
- `-h, --help`: Show help message

### Examples:
```bash
# Extract from course with spaces in name
python3 main.py "/Users/jane/Courses/Machine Learning Bootcamp" --consolidate

# Preview extraction
python3 main.py "~/Downloads/React Course" --dry-run

# Basic extraction only
python3 main.py "./course-materials"
```

## Use Cases 💡

### 1. AI-Powered Study Notes
Copy `formatted.md` content to ChatGPT/Claude:
```
"Please create comprehensive study notes from this course transcript, 
including key concepts, examples, and practice questions."
```

### 2. Course Summaries
Generate chapter summaries and main takeaways for quick review.

### 3. Searchable Content
Convert video courses into searchable text documents.

### 4. Subtitle Editing
Use `raw.txt` with timestamps for subtitle editing or sync verification.

## Project Structure 🏗️

```
make-note/
├── main.py                     # CLI entry point
├── find_subtitle_files.py      # Recursive file discovery
├── extract_subtitles.py        # File extraction and organization
├── parse_subtitle_content.py   # Format-specific parsing
├── consolidate_subtitles.py    # Markdown generation
├── create_raw_combined.py      # Raw text with timestamps
├── config.py                   # Settings and file extensions
└── data/
    ├── test/                   # Test data and samples
    └── output/                 # Generated output files
```

## Troubleshooting 🔧

### Common Issues:

**"No subtitle files found"**
- Check that your course folder contains subtitle files (.srt, .vtt, etc.)
- Verify the path is correct and accessible

**"Encoding errors"**
- The tool handles multiple encodings automatically (UTF-8, Latin-1, CP1252, UTF-16)
- Malformed files are gracefully skipped with error messages

**"Permission denied"**
- Ensure you have read access to the source directory
- Check write permissions for the output location

### Getting Help:
1. Run with `--dry-run` to preview the extraction
2. Check the console output for specific error messages
3. Verify your course folder structure matches expected patterns

## Contributing 🤝

Contributions are welcome! Here's how you can help:

1. **Bug Reports**: Open an issue with details about the problem
2. **Feature Requests**: Suggest new functionality or improvements
3. **Code Contributions**: Fork, create a feature branch, and submit a PR
4. **Documentation**: Help improve this README or add code comments

### Development Setup:
```bash
git clone https://github.com/imf4isal/subscript.git
cd make-note
# Make your changes
python3 main.py "test/sample_course" --consolidate  
```


## What's Next? 🚀

Once you've extracted your course subtitles, here are powerful ways to leverage the generated content:

### 1. AI-Enhanced Learning 🤖
- **Feed to LLMs**: Copy `formatted.md` content to ChatGPT, Claude, or Gemini for personalized study materials
- **Generate Summaries**: "Summarize the key concepts from each chapter in bullet points"
- **Create Flashcards**: "Generate flashcards from this content for spaced repetition learning"
- **Practice Questions**: "Create quiz questions with answers based on this course material"

### 2. Deep Topic Exploration 🔍
- **Elaborate Concepts**: "Explain [specific topic] in more detail with real-world examples"
- **Connect Ideas**: "How does [concept A] relate to [concept B] from this course?"
- **Compare Approaches**: "What are alternative approaches to the methods discussed?"
- **Industry Context**: "How is this concept applied in modern software development?"

### 3. Practical Application 💼
- **Code Examples**: "Show me practical code examples implementing these concepts"
- **Project Ideas**: "Suggest projects that would help me practice these skills"
- **Best Practices**: "What are the industry best practices for the topics covered?"
- **Troubleshooting**: "What are common mistakes when implementing these concepts?"

### 4. Study Optimization 📚
- **Learning Path**: "Create a learning roadmap based on this course content"
- **Prerequisite Check**: "What should I learn before diving into [advanced topic]?"
- **Progress Tracking**: Use the structured format to mark completed sections
- **Review Schedule**: Create spaced repetition schedules for key concepts

### 5. Content Enhancement 🎯
- **Research Extensions**: Use course topics as starting points for deeper research
- **Current Updates**: "What recent developments exist in [course topic]?"
- **Tool Recommendations**: "What tools and libraries support these concepts?"
- **Community Resources**: Find relevant documentation, tutorials, and communities

### Pro Tips for AI Integration:
```
"I have course material on [topic]. Please:
1. Identify the 5 most important concepts
2. Create a mind map showing relationships
3. Suggest 3 hands-on projects to practice
4. List common interview questions on these topics"
```

Transform passive video consumption into active, AI-powered learning! 🎓✨

---

