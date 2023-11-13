import glob
from pathlib import Path
import os.path
import shutil
import re

import arguments as args


# illegal folder charachters: * " / \ < > : | ?

### Ideas
# limit folder name length
# dont create folder if only one pattern file
# make folders have more extensive name than pattern
# (not necessarily absolute path)
# gui
# add tqdm for more visual progress
# save the ran configuration
# print the amount of the moved files + the amount of all files at all


def main():
    arg = args.get_arguments()

    for file in Path(arg.path).glob("*"):

        # Skipping folders if ignore_folders == true
        if arg.ignore_folders and os.path.isdir(file):
            continue

        if arg.delimeter is not None:
            outdir, skip_file = delimeter_variant(arg, file)
        elif arg.regex_pattern is not None:
            outdir, skip_file = regex_pattern_variant(arg, file)

        # Skipping if skip_file == true
        if skip_file:
            continue

        # Skip if file- and outdir-path are identical (this might happen if folders are not skipped)
        if file == outdir:
            continue

        outdir.mkdir(exist_ok=True)

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
        except Exception as e:
            print(e)
            continue
    
    print("Done")

# Move every file that matches the given regex expression to the "custom_regex_pattern" folder
def regex_pattern_variant(arg, file):
    outdir = Path(arg.path) / "custom_regex_pattern"
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
    delimeter_separated = file.stem.split(arg.delimeter)

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

if __name__ == '__main__':
    main()

