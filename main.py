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
    # print(items[0])
    # print(type(items[0]))
    # for k in items[0]:
    #     print(k, items[0][k])

    read_progress_file()

    max_value=9999999
    if os.path.exists("max_value.txt"):
        max_value=int(read_file("max_value.txt")[0])

    file_name="results.json"

    for i, item in enumerate(items):

        index_start = get_progress_value(file_name)
        if i <= index_start or i>max_value:
            continue

        print("Processed {} repositories of out {}".format(i, len(items)))
        write_file("current_file.txt", ["Processed {} repositories of out {}".format(i, len(items))], "a+" )

        repo_name = item["name"]
        repo_commit = item["lastCommitSHA"]
        repo_url = "https://github.com/{}".format(repo_name)
        r = None

        try:
            r = Repository(repo_name)
            if not r.ok_repo:
                continue
            files = getListOfFiles(r.repo_dir)
            java_files = [f for f in files if f.endswith(".java")]
            # print(java_files)



            for f in java_files:

                textprocessing = TextProcessing(f)

                textprocessing.srcml_process()

                textprocessing.remove_comments()
                textprocessing.remove_tags()

                methods = textprocessing.get_list_of_methods()

                for m in methods:
                    m_obj = Method(m, repo_name, repo_commit, repo_url)
                    m_obj.get_all_conditions()
                    m_obj.export_method_and_masked_method()

        except Exception as e:
            print(e)
        finally:
            r.cleanup()
            update_progress_bar(file_name, i)

            # print("cleaned")


if __name__ == "__main__":
    main()
