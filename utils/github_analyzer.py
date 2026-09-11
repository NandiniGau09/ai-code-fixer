import os
import shutil
from git import Repo

TEMP_REPO_DIR = "temp_repo"


def clone_repo(repo_url):

    # remove old repo
    if os.path.exists(TEMP_REPO_DIR):
        shutil.rmtree(TEMP_REPO_DIR)

    Repo.clone_from(repo_url, TEMP_REPO_DIR)

    return TEMP_REPO_DIR


def get_code_files(repo_path):

    code_files = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:

            if file.endswith((
                ".py",
                ".java",
                ".cpp",
                ".js"
            )):
                code_files.append(
                    os.path.join(root, file)
                )

    return code_files


def read_file_content(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    except:
        return ""