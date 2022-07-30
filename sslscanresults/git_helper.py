from git import Repo
import os
import shutil
import subprocess

PATH_OF_GIT_REPO = r'/tmp/SSLLab_hosts_and_report'
SSLLab_hosts_and_report_GIT_REPO = "https://manjku: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@github.com/manjku/SSLLab_hosts_and_report.git"
COMMIT_MESSAGE = 'New reports'
DESTINATION_PATH_OF_GIT_REPO = os.path.join(PATH_OF_GIT_REPO, ".git")

def clone_report_repo():
    try:
        print(f"Removing any existing Repo {PATH_OF_GIT_REPO}") 
        shutil.rmtree("/tmp/SSLLab_hosts_and_report", ignore_errors=True)
        print(f"Cloning Report repo at {PATH_OF_GIT_REPO}")
        Repo.clone_from(SSLLab_hosts_and_report_GIT_REPO, PATH_OF_GIT_REPO)
        print(f"Successfully Cloned rep at [{PATH_OF_GIT_REPO}]")
    except Exception as Err:
        print(f"ERROR: Could not clone the Report repo at {PATH_OF_GIT_REPO} due to error: \n{Err}")
        return 1

def git_push3():
    try:
        print("\n\n\n****** Starting git push for new reports ******\n\n\n")
        cur_dir = os.getcwd()
        print(f"current working directory {cur_dir}")
        os.chdir(PATH_OF_GIT_REPO)
        print(f"current working directory {os.getcwd()}")
        print("Executing subprocess_run")
        os.system("git status")
        os.system("ls")
        os.system("git add . ")
        os.system("git commit -m 'new_report'")
        os.system("git push")
        print("Completed subprocess_run")
        os.chdir(cur_dir)
        print(f"current working directory {os.getcwd()}")
        print("\n\n\n****** Completed git push ******\n\n\n")
    except Exception as Err:
        print(f"ERROR: Could not push the Report repo at {PATH_OF_GIT_REPO} due to error: \n{Err}")
        return 1

def git_push2():
    try:
        print("\n\n\n****** Starting git push for new reports ******\n\n\n")
        cur_dir = os.getcwd()
        print(f"current working directory {cur_dir}")
        os.chdir(PATH_OF_GIT_REPO)
        print(f"current working directory {os.getcwd()}")
        print("Executing subprocess_run")
        subprocess.call(["git", "status"])
        subprocess.call(["ls"])
        subprocess.call(["git", "add", "/tmp/SSLLab_hosts_and_report/."])
        subprocess.call(["git", "commit", "-m", "'new_report'"])
        subprocess.call(["git", "push"])
        print("Completed subprocess_run")
        os.chdir(cur_dir)
        print(f"current working directory {os.getcwd()}") 
        print("\n\n\n****** Completed git push ******\n\n\n")
    except Exception as Err:
        print(f"ERROR: Could not push the Report repo at {PATH_OF_GIT_REPO} due to error: \n{Err}")
        return 1
 
def git_push():
    try:
        repo = Repo(DESTINATION_PATH_OF_GIT_REPO)
        repo.git.add("--all")
        repo.index.commit(COMMIT_MESSAGE)
        repo.git.push()
        print(f"Successfully pushed new Reports at [{PATH_OF_GIT_REPO}]")
    except Exception as Err:
        print(f"ERROR: Could not push the Report repo at {PATH_OF_GIT_REPO} due to error: \n{Err}")
        return 1

