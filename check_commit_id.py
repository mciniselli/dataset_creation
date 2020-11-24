import json

from utils.input_output import *

from utils.github_api import Repository

from utils.textprocessing import TextProcessing

from utils.method_parsing import Method

from utils.utilities import getListOfFiles

import sys
import os
from utils.progress import read_progress_file, get_progress_value, update_progress_bar

def main():
    json_file = "json_data/results.json"
    file_data = read_file(json_file)
    data = json.loads(file_data[0])
    items = (data["items"])
    print(len(items))


    file_name="results.json"

    for i, item in enumerate(items):


        repo_name = item["name"]
        repo_commit = item["lastCommitSHA"]
        
        if repo_commit=="f3abb4eb19357ac353d4a1e59d2920135619ad9a":
            print(i)


if __name__ == "__main__":
    main()
