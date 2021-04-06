'''
Git hub related funtions

@autor: MiguelB
'''

from git import Repo
from os import path

AMBIENT = None


def get_git_ambient(dir = None):
    '''

    :param dir: string directory where u wanna check if u are in dev or in production: this command can be usefull : path.join(__file__ ,"../..")
    :return: AMBIENT or PRODUCTION
    '''
    if dir is None:
        dir = path.join(__file__ ,"../..")

    repofolder              = path.abspath(dir)
    repo                    = Repo(repofolder)
    global AMBIENT

    if "dev" in str(repo.active_branch) :
        AMBIENT             = "DEVELOPMENT"
    elif str(repo.active_branch) == "master":
        AMBIENT             = "PRODUCTION"

    print("Repository/Branch\n- repository folder: {}\n- repository branch: {}\n".format(repofolder, str(repo.active_branch)))

    return AMBIENT

def git_ambient_is_dev(dir = None):
    get_git_ambient(dir)
    if AMBIENT is not None and AMBIENT == "DEVELOPMENT": return True
    return False

def git_ambient_is_production(dir = None):
    get_git_ambient(dir)
    if AMBIENT is not None and AMBIENT == "PRODUCTION": return True
    return False


# Just for tests
if __name__ == "__main__":
    print(get_git_ambient())