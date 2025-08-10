# Markdown to HTML Python Converter

This is a simple Python program that converts Markdown files to HTML files.

It's a handy tool for creating content for your website since Markdown is faster to write and convert using this script.
This way you can save time by not having to write HTML code directly.

## Requirements
- Python 3.10 or higher
- Standard Python libraries:
    - `os`
    - `re`
    - `json`


### Bundled Libraries
- [`Syhmmac's Simple Logger`](https://github.com/Syhmac/simple_logger)

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
- Including a paragraph in the list takes a bit of different syntax than in Markdown.
    ```md
    Traditional Markdown syntax:
  
    - List item
        
        Paragraph in the list item.
  
    In this script, you need to use a different syntax:
  
    - List item
        Paragraph in the list item.
  
    Note that you don't need that additional blank line before the paragraph.
    If you want to include the blank line, make sure fill it with as many spaces
    as the indentation for the paragraph.
    ```
- Indentations in list need to be done with spaces, not tabs, and should be consistently long.
- Code blocks do not support syntax highlighting.

## Known Issues
So far there is no known issues with the script.
