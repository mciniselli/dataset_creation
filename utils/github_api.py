import os
from shutil import rmtree

from utils.utilities import run_command

class Repository:
    def __init__(self, repo_full_name):
        self.repo_name = repo_full_name
        if not os.path.isdir('temp'):
            os.makedirs('temp')
        self.repo_dir = os.path.join(os.getcwd(), 'temp', self.repo_name.replace('/', '_'))
        self.repo_dir = os.path.join(os.getcwd(), 'temp')
        self.ok_repo = True

        try:

            # oo=run_command('git clone https://test:test@github.com/{}.git {}'.format(repo_full_name,  self.repo_dir ), self.repo_dir)
            oo="ok"
            if "failed" in oo:
               self.ok_repo=False

        except Exception as e:
            self.ok_repo=False
            print("ERRORRRR {}".format(e))



    def cleanup(self):
        if os.path.isdir(self.repo_dir):
            rmtree(self.repo_dir)