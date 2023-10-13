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


    # run this version loop if you want to ignore single files
    #file_count = len(glob.glob1(path, f"{file_base_name}*"))
    #if file_count > 1 or Path(file_base_name).is_dir(): 
    #    outdir = Path(path) / file_base_name
    #    outdir.mkdir(exist_ok=True)
    #    zuio = outdir / fn.name
    #    fn.rename(outdir / fn.name)

def main():
    for file in Path(path).glob("*"):

        if os.path.isdir(file):
            #test = file.stem
            #if "." in test:
            #    print("contains .")
            #print("isdir")
            continue

        delimeter_separated = file.stem.split("_")

        almost = "_".join(delimeter_separated[0:2]) # filename without last part for the folder to be named after

        file_base_name = delimeter_separated[0] # pattern to be sorted after

        #asdf = file.stem.split("_")[:1]
        #asdfg = file.stem.split("_")
        #qwer = "_".join(asdf)
        #qwert = "AAA".join(asdf)
        #yxcv = file.stem
        #what = glob.glob1(path, f"{file_base_name}*")

        outdir = Path(path) / almost
        outdir.mkdir(exist_ok=True)

        #asdf = outdir / file.name
        #if asdf.is_file():
        #    continue
        try:
            target = outdir / file.name
            if len(str(target)) < 260:
                print(len(str(target)))
                print(((target)))

            #print(type(target))
            #file.replace(target)
            shutil.move(file, target)
        except Exception as e:
            #print(e)
            #print("some problem")
            continue;
    
    print("Done")


if __name__ == '__main__':
    main()