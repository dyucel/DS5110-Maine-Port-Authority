# IMPORTS
import os
import sys
from datetime import datetime

# FUNCTIONS
def get_file_metadata(path):

    '''
    Parameter: full file path
    Returns: N/A

    Takes a file path as its only parameter, prints various attributes of the file stats.
    '''

    # returns an object containing various attributes for the file 
    file_stats = os.stat(path)

    # get our variables
    file_type = file_stats.st_mode
    file_inode = file_stats.st_ino
    file_size = file_stats.st_size
    most_recent_access_date = datetime.fromtimestamp(file_stats.st_atime)
    last_modified_date = datetime.fromtimestamp(file_stats.st_mtime)
    creation_date = datetime.fromtimestamp(file_stats.st_ctime)

    # print statements
    print(f'File Type: {file_type}')
    print(f'File Inode: {file_inode}')
    print(f'File Size: {file_size} bytes')
    print(f'Most Recent Access: {most_recent_access_date}')
    print(f'Last Modified: {last_modified_date}')
    print(f'Creation Time: {creation_date}')
    

# MAIN
def main():
    
    input_directory = sys.argv[1]
    # input_directory = r"C:\Users\jovie\DS5100\DS5110-Maine-Port-Authority\testing_code\data\Leases-Licenses"
    for file in os.listdir(input_directory):
        path = os.path.join(input_directory, file)
        print(f'\nProcessing {file}...')
        get_file_metadata(path)

    
if __name__ == "__main__":
    main()
    
