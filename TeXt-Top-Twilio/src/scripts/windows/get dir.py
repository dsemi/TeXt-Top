# Returns the file path of the given file, user can specify the starting directory (default = root)

import os, sys

def get_dir(user_input='', start_dir='\\'):
    user_input = '"' + sys.argv[1] + '"'
    if len(sys.argv) > 2:
        start_dir = sys.argv[2] 
    command = 'dir ' + user_input + ' /s /b'

    try:
        os.chdir(start_dir)
        wdir = os.popen(command).read()
        wdir = wdir.split('C:\\')
        output = wdir[1]
        output = 'C:\\' + output[:len(output)-1]
        print output
        return output
    except:
        pass
        return 1, "Failed to find file directory."

if __name__ == "__main__":
    get_dir()