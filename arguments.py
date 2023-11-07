import argparse

def get_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    required = parser.add_argument_group('required named arguments')
    requiredExcluding = parser.add_argument_group('required named arguments, excluding each other: EITHER occurence_at OR start_at and end_at')
    optional = parser.add_argument_group('optional named arguments')

    # Add an argument for the path
    #those actually should be changed from default to required, but for testing this is fine
    required.add_argument('--path', type=str, required=True, help='Specify the path')

    #group = parser.add_mutually_exclusive_group(required=True)
    required.add_argument('--delimeter', type=str, help='Specify the delimeter. A delimeter is the pattern at which occurence the filename will be\
                       split. Multiple characters as delimeter are allowed. Example: "_" would split the name "2000_01_02" to "2000", "01" and "02".')
    # group.add_argument('--pattern', type=str, help='Specify the path') # Since delimeter supports multiple characters, this feels redundant.

    # optional arguments
    optional.add_argument('--ignore_folders', type=bool, default=True, help='Ignores folders if set True. Default value is True (it\'s safer this way).')
    optional.add_argument('--ignore_singles', type=bool, default=False, help='Ignores single files if set True. No folder will be created for it.\
                         You have a single file if your pattern creates a file_base_name that matches only 1 file. Default value is False.')
    
    # Amount of delimeter-steps, go_until excludes the other two. Can't add to mutually exclusive groups because of too complex logic
    requiredExcluding.add_argument('--occurence_at', type=int, default=None, help='Take exactly one element from the split name. Keep in mind that\
                         the first element is at 0. You can give negative numbers if you want to count backwards, -1 would be the last element.')
    requiredExcluding.add_argument('--start_at', type=int, default=None, help='Define at which split element of the name to start. the same counting rules as in --occurence_at.')
    requiredExcluding.add_argument('--end_at', type=int, default=None, help='Define at which split element of the name to start. The named element is not included. Example: If you want the first 2\
                        elements you need to define --end_at 2.\ Otherwise the same counting rules as in --occurence_at.')

    #parser.add_argument('--skip', action='store_true', help='Skip the process') some random argument for sake of example

    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Check if passed argument combination is legal
    if not ((args.occurence_at is not None) ^ ((args.start_at is not None) or (args.end_at is not None))):
        parser.error("Either --occurence_at or (--start_at or --end_at) is required.")

    print(args)
    return args

get_arguments()