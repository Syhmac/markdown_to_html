# Markdown to HTML Python Converter

This is a simple Python program that converts Markdown files to HTML files.

It's a handy tool for creating content for your website since Markdown is faster to write and convert using this script.
This way you can save time by not having to write HTML code directly.

## Requirements
- Python 3.10 or higher

## Usage
1. Clone the repository or download the script.
2. Place your Markdown files in the same directory as the script.
3. Run the cript from the command line or Python executable.
4. Follow the directions in the script to convert your Markdown files to HTML.

If there is no config file, the script will create a default one for you.

## Features
- Converts Markdown files to HTML format.
- Can be configured to include default CSS classes for every element.
- Supported elements from Markdown syntax:
    - [x] Headers (from h1 to h6)
    - [ ] Headers with IDs
    - [ ] Alternative header syntax (=== or --- below the text)
    - [x] Paragraphs
    - [x] Line breaks
    - [x] Bold text (both ** and __)
    - [x] Italic text (both * and _)
    - [x] Bold and italic text (\*\*\*, \_\_\_, \_\_\*, \*\*\_)
    - [x] Strikethrough text (~~)
    - [x] Blockquotes
    - [x] Lists (ordered and unordered)
    - [x] Elements within lists
    - [x] Code
    - [ ] Code blocks
    - [x] Fenced code blocks
    - [ ] Syntax highlighting
    - [x] Horizontal rules
    - [x] Links
    - [ ] Reference-style links
    - [x] Images
    - [x] Escaped characters
    - [x] Tables
    - [x] Tables with alignment
    - [ ] Footnotes
    - [ ] Definition lists
    - [x] Task lists
    - [ ] Emojis
    - [x] Highlighted text
    - [x] Subscript text
    - [x] Superscript text
    - [ ] Auto-linking URLs

## Configuration
You can configure the script by editing the `mc_to_html_config.json` file.
This will allow you to set default CSS classes for each HTML element generated from Markdown.

You can also set everything up by using the settings menu in the script.

## Limitations
- The script does not support all Markdown features, such as footnotes, definition lists, and reference-style links.
- Some advanced Markdown features may not be fully supported.
- The script may not handle all edge cases in Markdown syntax.

## Known Issues
So far there is no known issues with the script.