import re
import os
import logging
from pathlib import Path
import sys


# Little spinning symbol to show that there is work in progress
def progress_spin(elements):
    spinner = ['-', '\\', '|', '/']
    for el in elements:
        for char in spinner:
            print(f'\r Work in Progress: {char}', end='', flush=True)
        yield el
    print('\r', end='', flush=True)  # Clear the spinner

# Count the number of lines in file
def count_lines_in_file(file):
    with open(file, 'r') as file:
        line_count = sum(1 for line in file)
    return line_count

# Remove any characters that would be illegal for a folder- or filename
def clean_string_for_filename(text):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', '', text) # The second half of this expression are ASCII control characters. May be overkill but safe is safe.

# Set up the logger
def set_up_logger(log_directory, log_file_name):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)   
    log_file = os.path.join(log_directory, log_file_name)    
    initial_line_count = count_lines_in_file(log_file)
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return log_file, initial_line_count

# Save the just ran command for reuse to a script file 
def save_arguments(args):
    file_base_name = "folder-inator_script"
    file_extension = ".bat"

    if args.save_name is not None and len(args.save_name) > 0:
        file_base_name = args.save_name
        
    file_name = file_base_name + file_extension
    file_name = clean_string_for_filename(file_name)

    directory = Path("saved_folder-inator_scripts")
    directory.mkdir(exist_ok=True)
    file_path = directory/file_name

    # In case such file exists already, find a name-number combination, that does not exist yet
    counter = 1
    while os.path.exists(file_path):
        file_path = directory / (file_base_name + f"({counter})" + file_extension)
        counter += 1
        
    # check if program is ran as .exe or .py
    if getattr(sys, 'frozen', False):
        command_prefix = sys.executable
    else:
        command_prefix = "python " + os.path.abspath(__file__)

    # Write everything in a file
    with open(file_path, 'w') as file:
        file.write(f'{command_prefix}')

        # Loop through the arguments and add them to the script
        for arg in vars(args):
            value = getattr(args, arg)
            if value:
                # Leave out --save_arguments as this would cause creating the same file over and over again
                if arg == "save_arguments":
                    continue
                file.write(f' --{arg} {value}')

