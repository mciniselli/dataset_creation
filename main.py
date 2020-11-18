import json

from utils.input_output import *

from utils.github_api import Repository

from utils.textprocessing import TextProcessing

from utils.method_parsing import Method

from utils.utilities import getListOfFiles

import sys

def main():
    json_file="json_data/results.json"
    file_data=read_file(json_file)
    data=json.loads(file_data[0])
    items=(data["items"])
    print(len(items))
    print(items[0])
    print(type(items[0]))
    for k in items[0]:
        print(k, items[0][k])

    item_0=items[0]
    repo_name=item_0["name"]
    repo_commit=item_0["lastCommitSHA"]
    repo_url="https://github.com/{}".format(repo_name)
    r=None

    try:
        r=Repository(repo_name)

        files=getListOfFiles(r.repo_dir)
        java_files=[f for f in files if f.endswith(".java")]
        print(java_files)
        for f in java_files:

            textprocessing=TextProcessing(f)

            textprocessing.srcml_process()

            textprocessing.remove_comments()
            textprocessing.remove_tags()

            methods=textprocessing.get_list_of_methods()

            for m in methods:
                m_obj=Method(m, repo_name, repo_commit, repo_url)
                m_obj.get_all_conditions()
                m_obj.export_method_and_masked_method()

    except Exception as e:
        print(e)
    finally:
        # r.cleanup()
        print("cleaned")


if __name__=="__main__":
    main()