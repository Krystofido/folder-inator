import argparse

def get_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add an argument for the path
    #those actually should be changed from default to required, but for testing this is fine
    parser.add_argument('--path', '-p', type=str, default=r"D:\0", help='Specify the path')
    parser.add_argument('--delimeter', '-d', type=str, default=r"_", help='Specify the path')
    #parser.add_argument('--printerrors', type=bool, required=True, help='Specify whether to print errors (True/False)') # Just some random argument for example uses

    # optional arguments
    parser.add_argument('--ignore_folders', type=bool, default=True, help='Ignores folders if set True.') # TODO test behaviour when set to false
    parser.add_argument('--ignore_singles', type=bool, default=False, help='Ignores single files if set True. No folder will be created for it.\
                         You have a single file if your pattern creates a file_base_name that matches only 1 file.')
    
    # Amount of delimeter-steps, go_until excludes the other two
    # TODO
    parser.add_argument('--go_until', type=int, default=None, help='')
    parser.add_argument('--start_at', type=int, default=None, help='')
    parser.add_argument('--stop_at', type=int, default=None, help='')


    # Parse the command-line arguments
    args = parser.parse_args()
    return args

get_arguments()