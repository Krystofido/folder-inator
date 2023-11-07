import argparse

def get_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add an argument for the path
    #those actually should be changed from default to required, but for testing this is fine
    parser.add_argument('--path', type=str, required=True, help='Specify the path')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--delimeter', type=str, help='Specify the path')
    group.add_argument('--pattern', type=str, help='Specify the path')

    # optional arguments
    parser.add_argument('--ignore_folders', type=bool, default=True, help='Ignores folders if set True.') # TODO test behaviour when set to false
    parser.add_argument('--ignore_singles', type=bool, default=False, help='Ignores single files if set True. No folder will be created for it.\
                         You have a single file if your pattern creates a file_base_name that matches only 1 file.')
    
    # Amount of delimeter-steps, go_until excludes the other two
    parser.add_argument('--occurence_at', type=int, default=None, help='')
    parser.add_argument('--start_at', type=int, default=None, help='')
    parser.add_argument('--end_at', type=int, default=None, help='')

    #parser.add_argument('--skip', action='store_true', help='Skip the process') some random argument for sake of example

    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Check if passed argument combination is legal
    if not ((args.occurence_at is not None) ^ ((args.start_at is not None) or (args.end_at is not None))):
        parser.error("Either --occurence_at or (--start_at or --end_at) is required.")

    print(args)
    return args

get_arguments()