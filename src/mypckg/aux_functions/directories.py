
import os,re

def create_dir_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print("Created directory: "+str(folder_name))


def join_sufix_to_dir(folder_name,sufix):
    if folder_name[-1] == "/":
        fn = folder_name[0:-1]
        return fn + sufix + "/"
    else:
        return folder_name + sufix



def find_files_containing(dir,patterns,mode ="all",give_filenames=None):
    '''

    :param dir:
    :param patterns: should be a vector of strings
    :param mode: all or any
    :return: file string if found all patterns on files dir. False otherwise
    '''
    if give_filenames is None:
        files_names=os.listdir(dir)
    else:
        files_names = give_filenames
    files=[]
    for f in files_names:
        if mode == "all":
            if all([re.search(pattern, f) for pattern in patterns]):
                files.append(f)
        elif mode == "any":
            if any([re.search(pattern, f) for pattern in patterns]):
                files.append(f)
        else:
            raise
    return files



def filenames_starting_with(path, prefix):
    return [filename for filename in os.listdir(path) if filename.startswith(prefix)]


def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return total, used, free

def disk_usage_MB(path):
    total, used, free = disk_usage(path)
    return round(float(total)/1024/1024,1), round(float(used)/1024/1024,1), round(float(free)/1024/1024,1)

def disk_usage_GB(path):
    total, used, free = disk_usage(path)
    return round(float(total)/1024/1024/1024,1), round(float(used)/1024/1024/1024,1), round(float(free)/1024/1024/1024,1)