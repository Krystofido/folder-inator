import glob
from pathlib import Path
import os.path
import shutil

path = r"D:\0"

delimeter = "_"
ignore_folders = True # if not ignore folders I'd need to implement many failsafes
ignore_singles = True # do not put single files 

# Amount of delimeter-steps, go_until excludes the other two
go_until = None
start_at = None
stop_at = None



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


def main():
    for file in Path(path).glob("*"):

        # Skipping folders if ignore_folders == true
        if ignore_folders and os.path.isdir(file):
            continue

        delimeter_separated = file.stem.split("_")

        file_base_name = "_".join(delimeter_separated[0:2]) # filename without last part for the folder to be named after
        # Folder names can't end with dots (.) and are automatically removed by the OS. Thus if the file_base_name ends with dots they need to be stripped
        file_base_name = file_base_name.rstrip(".")

        # # Skipping folders if ignore_singles == true
        if ignore_singles and check_amount_files(file_base_name) < 2:
            print("skipping")
            continue

        outdir = Path(path) / file_base_name
        outdir.mkdir(exist_ok=True)

        #asdf = outdir / file.name
        #if asdf.is_file():
        #    continue
        try:
            target = outdir / file.name
            #if len(str(target)) < 260:
            #    print(len(str(target)))
            #    print(((target)))
            shutil.move(file, target)
        except Exception as e:
            continue
    
    print("Done")

# Checks amount of files with given pattern
def check_amount_files(file_base_name):
    file_count = len(glob.glob1(path, f"{file_base_name}*"))
    return file_count

if __name__ == '__main__':
    main()

