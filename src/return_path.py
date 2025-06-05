# This program returns the path to the directory which is to be processed
from pathlib import Path
import subprocess
import shutil
import sys

# Returns path to a temp directory
def parserepo():
    repo_root = Path(__file__).parent.parent
    temp_path = repo_root / "temp"
    temp_path.mkdir(exist_ok=True)
    temp_repo_path = temp_path / "temp_repo"
    temp_repo_path.mkdir(exist_ok=True)
    return Path(temp_repo_path)

# Error handling for shutil
def handle(func, path, exc_info):
    import stat
    import os
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def save_directory(user_input: str):
    if "github.com" in user_input:
        temp_repo_path = parserepo()
        subprocess.run(["git", "clone", user_input, temp_repo_path])
        return temp_repo_path, True
    
    else:
        folder_path = Path(user_input)
        if folder_path.exists() and folder_path.is_dir():
            print("User input is correct")

        else:
            print("User input is invalid")
            sys.exit(1)
    return folder_path, False

def delete_link_repo(user_input: str, folder_path: Path):
    if "https://github.com/" in user_input:
        shutil.rmtree(str(folder_path), onexc=handle)