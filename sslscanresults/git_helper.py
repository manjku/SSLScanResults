from git import Repo
import os
import shutil

PATH_OF_GIT_REPO = r'/tmp/SSLLab_hosts_and_report'
SSLLab_hosts_and_report_GIT_REPO = "https://github.com/manjku/SSLLab_hosts_and_report.git"
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
        print(f"ERROR: Could not clone the Report repo at {PATH_OF_GIT_REPO} due to error: \nErr")
        return 1
   
def git_push():
    try:
        repo = Repo(DESTINATION_PATH_OF_GIT_REPO)
        repo.git.add("--all")
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
        print(f"Successfully pushed new Reports at [{PATH_OF_GIT_REPO}]")
    except Exception as Err:
        print(f"ERROR: Could not push the Report repo at {PATH_OF_GIT_REPO} due to error: \nErr")
        return 1
