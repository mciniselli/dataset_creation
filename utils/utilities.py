import os
from subprocess import Popen, PIPE, STDOUT

'''
get the list of all files
'''
# import timeout_decorator
#
# @timeout_decorator.timeout(15)
def popen(p, cmd, cur_work_dir):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=cur_work_dir)

    output = p.communicate(timeout=30)[0]

    # output = p.stdout.read()

    output2 = str(output)
    return output2

def run_command(cmd, cwd=None):  # run a specific command and return the output

    cur_work_dir = cwd

    if cur_work_dir is None:
        cur_work_dir = os.getcwd()

    p = None
    output2=None

    try:

        output2=popen(p, cmd, cur_work_dir)

    except Exception as e:
        print("TIMEOUT")

    return output2


def run_command_clone(cmd, cwd=None):  # run a specific command and return the output

    cur_work_dir = cwd

    if cur_work_dir is None:
        cur_work_dir = os.getcwd()

    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=cur_work_dir)

    output = p.communicate(timeout=300)[0]

    output2 = str(output)
    return output2

    return output2

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles
