import glob
from pathlib import Path
import os.path
import shutil
import re
import sys

import arguments

### Ideas
# limit folder name length
# make folders have more extensive name than pattern
# (not necessarily absolute path)
# gui
# add tqdm (or something else) for more visual progress
# log warnings/errors into file instead of console


def main():
    args = arguments.get_arguments()

    amount_total_files = 0
    amount_moved_files = 0
    amount_new_folders = 0

    for file in Path(args.path).glob("*"):
        amount_total_files += 1

        # Skipping folders if ignore_folders == true
        if args.ignore_folders and os.path.isdir(file):
            continue

        if args.delimeter is not None:
            outdir, skip_file = delimeter_variant(args, file)
        elif args.regex_pattern is not None:
            outdir, skip_file = regex_pattern_variant(args, file)

        # Skipping if skip_file == true
        if skip_file:
            continue

        # Skip if file- and outdir-path are identical (this might happen if folders are not skipped)
        if file == outdir:
            continue

        # Create new folder if not already existing
        folder_exists_before = os.path.exists(outdir)
        outdir.mkdir(exist_ok=True)
        folder_exists_after = os.path.exists(outdir)
        if not folder_exists_before and folder_exists_after:
            amount_new_folders += 1

        target = outdir / file.name
        # The shutil.move() method (or any other file moving function in Python known to me) can't have a target-path () longer than 259 characters.
        # If I understand correctly, it's because of OS restrictions.
        # Note that you can still move the file manually to paths longer than 259 characters.
        if len(str(target)) > 259:
            print(f"The target path:\n{target}\nis too long (has {len(str(target))} characters, only up to 259 possible)." +
                   "\nPlease choose a shorter file_base_name, move your files to a lower/shorter directory or move them manually.\n")
            continue

        try:
            shutil.move(file, target)
            amount_moved_files += 1
        except Exception as e:
            print(e)
            continue
    
    if args.save_arguments:
        save_arguments(args)

    print(f"Done: Moved {amount_moved_files} from {amount_total_files} available \
          file{'s' if amount_moved_files != 1 else ''} and folder{'s' if amount_moved_files != 1 else ''}. Created {amount_new_folders} new folder{'s' if amount_new_folders != 1 else ''}.")

# Move every file that matches the given regex expression to the "custom_regex_pattern" folder
def regex_pattern_variant(arg, file):
    clean_name = re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', '', arg.regex_pattern) # The second half of this expression are ASCII control characters. May be overkill but safe is safe.
    outdir = Path(arg.path) / clean_name
    regex_result = re.search(arg.regex_pattern, file.name)

    # Skip the file from moving if it doesn't match given regex expression
    skip_file = True
    if regex_result is not None:
        skip_file = False

    return outdir, skip_file

# Create a new folder for every newly discovered name pattern through the combination of --delimeter and --occurence_of or -start_at/--end_at
# and move every file matching this pattern into this folder
def delimeter_variant(arg, file):
    skip_file = False
    delimeter_separated = ""
    # Special case if delimeter is specified as empty string, else use split()
    if arg.delimeter == "":
        delimeter_separated = list(str(file.stem))
    else:
        delimeter_separated = file.stem.split(arg.delimeter)
    print(delimeter_separated)

    # Depending on the choice of either --occurence_at or the two arguments --start_at and/or --end_at, different naming process.
    file_base_name = None
    if(arg.occurence_at is not None):
        if (arg.occurence_at) < len(delimeter_separated):
            file_base_name = delimeter_separated[arg.occurence_at]
        else:
            print(f"Given --occurence_at is out of scope of the delimeter-separated list of strings. {file.name} will be skipped. " +
                 "Please consider setting a lower --occurence_at.")
            outdir = None
            skip_file = True
            return outdir, skip_file
            
    else:
        file_base_name = arg.delimeter.join(delimeter_separated[arg.start_at:arg.end_at])

    # Folder names can't end with dots (.) and are automatically removed by the OS. Thus if the file_base_name ends with dots they need to be stripped
    file_base_name = file_base_name.rstrip(".")

    outdir = Path(arg.path) / file_base_name

    # Skip file if there is only one matching the given pattern (and --ignore_singles is True)
    if arg.ignore_singles and check_amount_files(arg.path, file_base_name) < 2:
        skip_file = True

    return outdir, skip_file

# Checks amount of files with given pattern
def check_amount_files(basepath, file_base_name):
    file_count = len(glob.glob1(basepath, f"{file_base_name}*"))
    return file_count

# Remove any characters that would be illegal for a folder- or filename
def clean_string_for_filename(text):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F\x7F]', '', text) # The second half of this expression are ASCII control characters. May be overkill but safe is safe.

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

if __name__ == '__main__':
    main()

