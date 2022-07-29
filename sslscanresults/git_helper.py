from git import Repo
import os
import shutil

PATH_OF_GIT_REPO = r'/tmp/SSLLab_hosts_and_report'
SSLLab_hosts_and_report_GIT_REPO = "https://github.com/manjku/SSLLab_hosts_and_report.git"
COMMIT_MESSAGE = 'New reports'

def git_push():
    try:
        DESTINATION_PATH_OF_GIT_REPO = os.path.join(PATH_OF_GIT_REPO, ".git")
        shutil.rmtree("/tmp/SSLLab_hosts_and_report", ignore_errors=True)
        Repo.clone_from(SSLLab_hosts_and_report_GIT_REPO, PATH_OF_GIT_REPO)
        os.system("touch /tmp/SSLLab_hosts_and_report/test6")
        repo = Repo(DESTINATION_PATH_OF_GIT_REPO)
        repo.git.add("--all")
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    

git_push()
