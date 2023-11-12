import argparse
import smart_formatter


def get_arguments():
    # Create an ArgumentParser object

    text = """
    ---
    folder-inator v0
    
    Program to put files with defined delimeter or pattern to the same folder.
    ---"""

    parser = argparse.ArgumentParser(description=text, formatter_class=smart_formatter.SmartFormatter)

    required = parser.add_argument_group('required named arguments')
    requiredExcluding = parser.add_argument_group('required named arguments, excluding each other: \
                                                  \nEITHER --delimeter OR --regex_pattern (and vice versa)\
                                                  \nEITHER --occurence_at OR --start_at and --end_at (and vice versa)')
    optional = parser.add_argument_group('optional named arguments')

    # Add an argument for the path
    #those actually should be changed from default to required, but for testing this is fine
    required.add_argument('--path', type=str, required=True, help='Specify the path where the files are.')

    requiredExcluding.add_argument('--delimeter', type=str, help='Specify the delimeter. \nA delimeter is the pattern at which occurence the filename will be\
                       split. \nMultiple characters as delimeter are allowed. \nExample: "_" would split the name "2000_01_02" to "2000", "01" and "02".')
    requiredExcluding.add_argument('--regex_pattern', type=str, help='Unlike --delimeter creates only one folder called "custom_regex_pattern" and puts\
                                   every file that matches this pattern inside.')

    # optional arguments
    optional.add_argument('--ignore_folders', type=bool, default=True, help='Ignores folders if set True. \nDefault value is True (it\'s safer this way).')
    optional.add_argument('--ignore_singles', type=bool, default=False, help='Ignores single files if set True. \nNo folder will be created for it.\
                         \nYou have a single file if your pattern creates a file_base_name that matches only 1 file. \nDefault value is False.')
    
    # Amount of delimeter-steps, go_until excludes the other two. Can't add to mutually exclusive groups because of too complex logic
    requiredExcluding.add_argument('--occurence_at', type=int, default=None, help='Take exactly one element from the split name. \nKeep in mind that\
                         the first element is at 0. \nYou can give negative numbers if you want to count backwards, -1 would be the last element.')
    requiredExcluding.add_argument('--start_at', type=int, default=None, help='Define at which split element of the name to start. \nThe same counting rules as in --occurence_at.')
    requiredExcluding.add_argument('--end_at', type=int, default=None, help='Define at which split element of the name to start. \nThe named element is not included. \nExample: If you want the first 2\
                        elements you need to define --end_at 2.\ \nOtherwise the same counting rules as in --occurence_at.')

    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Check if passed argument combination is legal
    if not ((args.delimeter is not None) ^ (args.regex_pattern is not None)):
        parser.error("Arguments --delimeter and --regex_pattern exclude each other.")
    
    if not ((args.occurence_at is not None) ^ ((args.start_at is not None) or (args.end_at is not None))):
        parser.error("Arguments --occurence_at and (--start_at or --end_at) exclude each other.")

    print(args)
    return args

get_arguments()