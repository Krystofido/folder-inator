import glob
from pathlib import Path
import os.path
import shutil

import arguments as args


# illegal folder charachters: * " / \ < > : | ?

### Ideas
# Ignore other folder or include them
# choose delimeter
# limit folder name length
# make possible for pattern be at the start, end or middle
# dont create folder if only one pattern file
# make folders have more extensive name than pattern
# (not necessarily absolute path)
# gui
# add tqdm for more visual progress
# enter a certain pattern and look after it
# save the ran configuration
# suport regex?


def main():
    arg = args.get_arguments()

    for file in Path(arg.path).glob("*"):

        # Skipping folders if ignore_folders == true
        if arg.ignore_folders and os.path.isdir(file):
            continue


        delimeter_separated = file.stem.split(arg.delimeter)

        file_base_name = "_".join(delimeter_separated[0:2]) # filename without last part for the folder to be named after
        # Folder names can't end with dots (.) and are automatically removed by the OS. Thus if the file_base_name ends with dots they need to be stripped
        file_base_name = file_base_name.rstrip(".")

        # # Skipping folders if ignore_singles == true
        if arg.ignore_singles and check_amount_files(arg.path, file_base_name) < 2:
            print("skipping")
            continue

        outdir = Path(arg.path) / file_base_name
        outdir.mkdir(exist_ok=True)

        target = outdir / file.name
        # The shutil.move() method (or any other file moving function in Python known to me) can't have a target-path () longer than 259 characters.
        # If I understand correctly, it's because of OS restrictions.
        # Note that you can still move the file manually to paths longer than 259 characters.
        if len(str(target)) > 259:
            print(f"The target path:\n{target}\nis too long (has {len(str(target))} characters, only up to 259 possible).\
                   \nPlease choose a shorter file_base_name, move your files to a lower/shorter directory or move them manually.\n")
            continue

        try:
            shutil.move(file, target)
        except Exception as e:
            print(e)
            continue
    
    print("Done")

# Checks amount of files with given pattern
def check_amount_files(basepath, file_base_name):
    file_count = len(glob.glob1(basepath, f"{file_base_name}*"))
    return file_count

if __name__ == '__main__':
    main()

