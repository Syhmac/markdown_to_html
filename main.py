# Version: 1.0
# Markdown to HTML converter by Syhmac

# imports
import json, os, re
import simple_logger

# Initialize the logger
log = simple_logger.LOG(0, 'latest.log', 'logs/')

# Global variables
cl = 'cls' if os.name == 'nt' else 'clear'

def clear():
    """
    Clears the console screen based on the operating system.
    :return:
    """
    os.system(cl)

def main_menu() -> int:
    """
    Main menu function to display options to the user.
    :return: 0 - Success, 1 - Error, 2 - Exit, -1 - Critical Error
    """
    try:
        clear()
    except Exception as e:
        log.warn(f"Error clearing screen: {e}")

    print("Markdown to HTML Converter")
    print("1. Convert Markdown to HTML")
    print("2. Configuration (Will be implemented later)")
    print("3. Exit")

    choice = input("Enter your choice: ")

    try:
        choice = int(choice)
    except ValueError:
        log.error(f"Invalid main menu choice: {choice}")
        return 1

    match choice:
        case 1:
            convert_markdown_to_html()
            return 0
        case 2:
            return 0
        case 3:
            log.info("Exiting the program.")
            return 2
        case _:
            log.error(f"Unexpected choice in main menu: {choice}")
            return -1

def config():
    pass

def convert_markdown_to_html() -> int:
    """
    Converts Markdown file to HTML file.
    :return: -1 - Error, 0 - Success
    """
    input_path = input("Enter path to the Markdown file: ")
    if not os.path.exists(input_path):
        log.error(f"Markdown file does not exist: {input_path}")
        return -1
    output_path = input("Enter file to save the HTML file: ")
    if not output_path.endswith('.html'):
        log.error("Output file must have .html extension.")
        return -1

    log.info("Loading Markdown file.")

    input_file = open(input_path, 'r', encoding='utf-8')
    output_file = open(output_path, 'w', encoding='utf-8')

    lines = input_file.readlines()
    input_file.close()

    log.info("Converting Markdown to HTML.")
    output_html = handle_conversion(lines)

    log.info("Writing HTML to file.")
    output_file.write(output_html)
    output_file.close()

    return 0

def handle_conversion(lines: list) -> str:
    """
    Handles the conversion of Markdown lines to HTML.
    :param lines:
    :return: output HTML as a string
    """
    output = ""
    currently_open = []  # track currently open tags. Last is the latest.
    skip_lines = 0
    for i in range(len(lines)):
        if skip_lines > 0:
            skip_lines -= 1
            continue
        # Check if the line is empty - closing the currently open tag if it is.
        if lines[i].startswith("\n"):
            if currently_open != []:
                output += f"</{currently_open[-1]}>\n"
                currently_open.pop(-1)
            continue
        # Check for headers
        if lines[i].startswith('#'):  # We check for any number of '#' first, so we don't check every length option for the lines that are not headers.
            temp = close_any_open_paragraph(currently_open, output)
            currently_open = temp[0]
            output = temp[1]
            if lines[i].startswith('# '):  # H1
                currently_open.append("h1")
                lines[i] = lines[i].lstrip('# ')
            elif lines[i].startswith('## '):  # H2
                currently_open.append("h2")
                lines[i] = lines[i].lstrip('## ')
            elif lines[i].startswith('### '):  # H3
                currently_open.append("h3")
                lines[i] = lines[i].lstrip('### ')
            elif lines[i].startswith('#### '):  # H4
                currently_open.append("h4")
                lines[i] = lines[i].lstrip('#### ')
            elif lines[i].startswith('##### '):  # H5
                currently_open.append("h5")
                lines[i] = lines[i].lstrip('##### ')
            elif lines[i].startswith('###### '):  # H6
                currently_open.append("h6")
                lines[i] = lines[i].lstrip('###### ')
            else:
                log.warn(f"Unexpected header format! Too many #: {lines[i]}")
                log.warn(f"Treating the line as H6 header.")
                currently_open.append("h6")
                lines[i] = lines[i].lstrip('######')
            lines[i] = lines[i].rstrip('\n')
            formatted_output = check_for_formatting(lines[i])
            output += f"<{currently_open[-1]}>{formatted_output}"
        # Check for blockquotes
        elif lines[i].startswith('>'):
            temp = close_any_open_paragraph(currently_open, output)
            currently_open = temp[0]
            output = temp[1]
            blockquote_lines = []
            blockquote_ended = False
            line_count = 0
            while not blockquote_ended:
                try:
                    blockquote_lines.append(lines[i + line_count])
                    line_count += 1
                    if not lines[i + line_count].startswith(">"):
                        blockquote_ended = True
                except IndexError:
                    blockquote_ended = True
            skip_lines += line_count - 1
            blockquote_output = handle_blockquote(blockquote_lines)
            output += blockquote_output
        # Check for ordered lists
        elif lines[i].startswith('1. '):
            temp = close_any_open_paragraph(currently_open, output)
            currently_open = temp[0]
            output = temp[1]
            ordered_list_lines = []
            ordered_list_ended = False
            line_count = 0
            while not ordered_list_ended:
                try:
                    ordered_list_lines.append(lines[i + line_count])
                    line_count += 1
                    # Check the line using regex to see if it starts with a number followed by a dot and space.
                    if not re.match(r'^\d+\.\s', lines[i + line_count]) and not lines[i + line_count].startswith(' '):
                        ordered_list_ended = True
                except IndexError:
                    ordered_list_ended = True
            skip_lines += line_count - 1
            ordered_list_output = handle_ordered_list(ordered_list_lines)
            output += ordered_list_output
        # Check for unordered lists
        elif lines[i].startswith('- ') or lines[i].startswith('* ') or lines[i].startswith('+ '):
            temp = close_any_open_paragraph(currently_open, output)
            currently_open = temp[0]
            output = temp[1]
            unordered_list_lines = []
            unordered_list_ended = False
            line_count = 0
            while not unordered_list_ended:
                try:
                    unordered_list_lines.append(lines[i + line_count])
                    line_count += 1
                    if not (lines[i + line_count].startswith('- ') or lines[i + line_count].startswith('* ') or lines[i + line_count].startswith('+ ') or lines[i + line_count].startswith(' ')):
                        unordered_list_ended = True
                except IndexError:
                    unordered_list_ended = True
            skip_lines += line_count - 1
            unordered_list_output = handle_unordered_list(unordered_list_lines)
            output += unordered_list_output
        # Check for code blocks
        elif lines[i].startswith('```'):
            temp = close_any_open_paragraph(currently_open, output)
            currently_open = temp[0]
            output = temp[1]
            code_block_lines = []
            code_block_ended = False
            line_count = 0
            while not code_block_ended:
                try:
                    code_block_lines.append(lines[i + line_count])
                    line_count += 1
                    if not lines[i + line_count].startswith('```'):
                        continue
                    else:
                        code_block_ended = True
                except IndexError:
                    code_block_ended = True
            skip_lines += line_count
            code_block_output = handle_code_block(code_block_lines)
            output += code_block_output
        # Check for paragraphs
        # If nothing else is found, we treat the line as a paragraph.
        else:
            if (currently_open != [] and currently_open[-1] != "p") or currently_open == []:
                currently_open.append("p")
                output += f"<{currently_open[-1]}>"
            elif currently_open != [] and currently_open[-1] == "p":
                if not output.endswith("<br>"):
                    output += " "
            lines[i] = lines[i].rstrip('\n')
            formatted_output = check_for_formatting(lines[i])
            output += formatted_output

    if currently_open != []:
        while len(currently_open) > 0:
            output += f"</{currently_open[-1]}>\n"
            currently_open.pop(-1)

    return output

def close_any_open_paragraph(currently_open: list, output: str) -> list:
    """
    Closes any open paragraph tags in the output.
    :param currently_open: list of currently open tags
    :param output: current output string
    :return: newly updated currently_open list and output string
    """
    if currently_open != [] and currently_open[-1] == "p":
        output += "</p>\n"
        currently_open.pop(-1)
    output_list = [currently_open, output]
    return output_list

def check_for_formatting(line: str) -> str:
    """
    Checks for Markdown formatting in the line and returns the formatted line.
    :param line: line from the Markdown file
    :return: Text formatted as HTML
    """
    found_formating = True
    while found_formating:
        found_formating = False
        if line.find("***") != -1:
            found_formating = True
            line = line.replace("***", "<b><i>", 1)
            line = line.replace("***", "</i></b>", 1)
        if line.find("___") != -1:
            found_formating = True
            line = line.replace("___", "<b><i>", 1)
            line = line.replace("___", "</i></b>", 1)
        if line.find("**_") != -1:
            found_formating = True
            line = line.replace("**_", "<b><i>", 1)
            line = line.replace("_**", "</i></b>", 1)
        if line.find("__*") != -1:
            found_formating = True
            line = line.replace("__*", "<b><i>", 1)
            line = line.replace("*__", "</i></b>", 1)
        if line.find("**") != -1:
            found_formating = True
            line = line.replace("**", "<b>", 1)
            line = line.replace("**", "</b>", 1)
        if line.find("__") != -1:
            found_formating = True
            line = line.replace("__", "<b>", 1)
            line = line.replace("__", "</b>", 1)
        if line.find("*") != -1:
            found_formating = True
            line = line.replace("*", "<i>", 1)
            line = line.replace("*", "</i>", 1)
        if line.find("_") != -1:
            found_formating = True
            line = line.replace("_", "<i>", 1)
            line = line.replace("_", "</i>", 1)
        if line.find("~~") != -1:
            found_formating = True
            line = line.replace("~~", "<s>", 1)
            line = line.replace("~~", "</s>", 1)
        if line.find("~") != -1:
            found_formating = True
            line = line.replace("~", "<sub>", 1)
            line = line.replace("~", "</sub>", 1)
        if line.find("^") != -1:
            found_formating = True
            line = line.replace("^", "<sup>", 1)
            line = line.replace("^", "</sup>", 1)
        if line.find("`") != -1:
            found_formating = True
            line = line.replace("`", "<code>", 1)
            line = line.replace("`", "</code>", 1)
        if line.find("==") != -1:
            found_formating = True
            line = line.replace("==", "<mark>", 1)
            line = line.replace("==", "</mark>", 1)
    if line.endswith("  "):
        line = line.rstrip("  ")
        line += "<br>"
    return line

def handle_blockquote(lines: list) -> str:
    """
    Handles blockquotes
    :param lines: all lines that belong to the blockquote
    :return: Formatted blockquote as HTML
    """
    output = "<blockquote>\n"
    for i in range (len(lines)):
        if lines[i].startswith("> "):
            lines[i] = lines[i].lstrip('> ')
        elif lines[i].startswith(">"):
            lines[i] = lines[i].replace('>', '', 1)

    output += handle_conversion(lines)
    output += "</blockquote>\n"

    return output

def handle_ordered_list(lines: list) -> str:
    """
    Handles ordered lists
    :param lines: lines that belong to the ordered list
    :return: Formatted ordered list as HTML
    """
    output = "<ol>\n"
    skip_lines = 0
    for i in range(len(lines)):
        if skip_lines > 0:
            skip_lines -= 1
            continue
        if re.match(r'^\d+\.\s', lines[i]):
            lines[i] = re.sub(r'^\d+\.\s', '', lines[i], count=1)
            output += f'<li>{check_for_formatting(lines[i].rstrip("\n"))}</li>\n'
        elif lines[i].startswith(' '):
            deeper_lines_ended = False
            deeper_lines_count = 0
            deeper_lines = []
            indent_depth = len(lines[i]) - len(lines[i].lstrip(" "))
            while not deeper_lines_ended:
                try:
                    line = lines[i + deeper_lines_count].replace(' ', '', indent_depth)
                    deeper_lines.append(line)
                    deeper_lines_count += 1
                    if not lines[i + deeper_lines_count].startswith(" "):
                        deeper_lines_ended = True
                except IndexError:
                    deeper_lines_ended = True
            skip_lines += deeper_lines_count - 1
            output += handle_conversion(deeper_lines)
    output += "</ol>\n"
    return output

def handle_unordered_list(lines: list) -> str:
    """
    Handles unordered lists
    :param lines: lines that belong to the unordered list
    :return: Formatted unordered list as HTML
    """
    output = "<ul>\n"
    skip_lines = 0
    for i in range(len(lines)):
        if skip_lines > 0:
            skip_lines -= 1
            continue
        if re.match(r'^[-*+]\s', lines[i]):
            lines[i] = re.sub(r'^[-*+]\s', '', lines[i], count=1)
            output += f'<li>{check_for_formatting(lines[i].rstrip("\n"))}</li>\n'
        elif lines[i].startswith(' '):
            deeper_lines_ended = False
            deeper_lines_count = 0
            deeper_lines = []
            indent_depth = len(lines[i]) - len(lines[i].lstrip())
            while not deeper_lines_ended:
                try:
                    line = lines[i + deeper_lines_count].replace(' ', '', indent_depth)
                    deeper_lines.append(line)
                    deeper_lines_count += 1
                    if not lines[i + deeper_lines_count].startswith(" "):
                        deeper_lines_ended = True
                except IndexError:
                    deeper_lines_ended = True
            skip_lines += deeper_lines_count - 1
            output += handle_conversion(deeper_lines)
    output += "</ul>\n"
    return output

def handle_code_block(lines: list) -> str:
    """
    Handles code blocks
    :param lines: lines that belong to the code block
    :return: Formatted code block as HTML
    """
    output = "<pre><code>\n"
    for line in lines:
        if line.startswith('```'):
            continue
        output += f"{line.rstrip()}\n"
    output += "</code></pre>\n"
    return output

def handle_table(lines: list) -> str:
    """
    Handles tables
    :param lines: lines that belong to the table
    :return: Formatted table as HTML
    """
    pass
    #return output

def handle_task_list(lines: list) -> str:
    """
    Handles task lists
    :param lines: lines that belong to the task list
    :return: Formatted task list as HTML
    """
    pass
    #return output

if __name__ == "__main__":
    """
    Main entry point of the program.
    
    :return: 0 - Exit, -1 - Error
    """
    log.debug("Program started.")

    # Main loop
    while True:
        try:
            exit_code = main_menu()
            match exit_code:
                case 0:
                    log.debug("Returning to main menu.")
                case 1:
                    log.warn("Returning to main menu after an error.")
                case 2:
                    exit(0)
                case -1:
                    log.critical("Critical error encountered in main menu, exiting.")
                    exit(-1)
                case _:
                    log.critical(f"Unexpected exit code from main menu {exit_code}, exiting.")
                    exit(-1)
        except Exception as e:
            log.critical(f"Unexpected error in the main loop, exiting: {e}")
            exit(-1)
