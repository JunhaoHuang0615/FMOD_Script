from git import Repo
## git function
def clone_repo(url, dest):
    """
    克隆git仓库到指定的目录
    :param url: git仓库的URL
    :param dest: 克隆到的目标路径
    :return: None
    """
    Repo.clone_from(url, dest)

def pull_repo(path):
    """
    更新已克隆的git仓库
    :param path: git仓库的本地路径
    :return: None
    """
    repo = Repo(path)
    origin = repo.remotes.origin
    origin.pull()

def get_all_remote_branches(repo_path):
    """
    获取远程仓库的所有分支
    :param repo_path: git仓库的本地路径
    :return: 所有分支的列表
    """
    repo = Repo(repo_path)
    all_branches = [ref.name for ref in repo.remote().refs]
    return all_branches

def get_unique_branches(repo_path):
    # 创建Repo对象
    repo = Repo(repo_path)

    # 获取所有本地分支名称的列表
    local_branches = [str(b) for b in repo.heads]

    # 获取所有远程分支，但是移除'origin/'部分
    # remote_branches = [str(ref).replace("origin/", "") for ref in repo.remotes.origin.refs]
    remote_branches = [str(ref).replace("origin/", "") for ref in repo.remotes.origin.refs if str(ref) != 'origin/HEAD']

    # 将本地分支和处理过的远程分支合村到一起
    all_branches = local_branches + remote_branches

    # 移除重复的分支名
    unique_branches = list(set(all_branches))

    return unique_branches

def discard_all_changes(repo_path):
    """
    对应 'git checkout .' ，会丢弃所有未提交的修改
    :param repo_path: git仓库的本地路径
    :return: None
    """
    repo = Repo(repo_path)
    repo.git.checkout('.')

def clean_untracked_files(repo_path):
    """
    对应 'git clean -f -d'，会删除所有未跟踪的文件和目录
    :param repo_path: git仓库的本地路径
    :return: None
    """
    repo = Repo(repo_path)
    repo.git.clean('-f', '-d')

def reset_hard_previous_commit(repo_path):
    """
    对应 'git reset --hard HEAD^'，会退回到上一个提交
    :param repo_path: git仓库的本地路径
    :return: None
    """
    repo = Repo(repo_path)
    repo.git.reset('--hard', 'HEAD^')
    
def get_current_branch(repo_path):
    # 创建Repo对象
    repo = Repo(repo_path)

    # 如果HEAD是分离的，返回一个特殊的消息
    if repo.head.is_detached:
        return "HEAD is detached, there is no active branch."

    # 否则，获取并返回当前活动分支的名称
    current_branch = repo.active_branch.name

    return current_branch

def switch_branch(repo_path, branch_name):
    # 创建一个Repo对象
    repo = Repo(repo_path)

    if branch_name in [str(b) for b in repo.heads]:
        # 如果分支在本地存在，直接切换
        print("切换到本地分支: " + branch_name)
        repo.git.checkout(branch_name)
    else:
        # 如果分支在远程存在
        if "origin/" + branch_name in [str(ref) for ref in repo.remotes.origin.refs]:
            print("切换到远程分支: " + branch_name)
            # 先创建远程分支到本地，再切换
            repo.git.checkout('-b', branch_name, 'origin/' + branch_name)
        else:
            print(f'未找到指定的分支: {branch_name}')

def get_modified_files(repo_path):
    # 创建一个Repo对象
    repo = Repo(repo_path)

    # 获取被修改的文件列表
    modified_files = [item.a_path for item in repo.index.diff(None)]
    
    return modified_files

def get_modified_file(repo_path, file_path):
    repo = Repo(repo_path)
    with open(repo.working_tree_dir + '/' + file_path, 'r', encoding='utf-8') as file:  
        file_text = file.read()
        return file_text.splitlines()  # 使用`splitlines()`去掉行结束符

def get_original_file(repo_path, file_path):
    repo = Repo(repo_path)
    blob = repo.head.commit.tree / file_path
    file_content = blob.data_stream.read().decode('utf-8')  
    return file_content.splitlines()  # 使用`splitlines()`去掉行结束符

def diff_file(repo_path, file_path):
    # 创建一个Repo对象
    repo = Repo(repo_path)

    # 获取文件的diff
    diffs = repo.git.diff(None, file_path)

    return diffs

# def get_original_file(repo_path, file_path):
#     # 创建一个Repo对象
#     repo = Repo(repo_path)

#     # 获取blob对象，即文件的原始内容
#     blob = repo.head.commit.tree / file_path

#     # 将blob对象转换为字符串，即文件的内容
#     file_content = blob.data_stream.read().decode('utf-8')

#     return file_content

def get_all_changes(repo_path):
    # 创建Repo对象
    repo = Repo(repo_path)

    # 获取被修改的文件列表
    modified_files = [item.a_path for item in repo.index.diff(None)]

    # 获取新增的文件列表
    new_files = [item.a_path for item in repo.index.diff('HEAD')]

    # 获取删除的文件列表
    deleted_files = [item.a_path for item in repo.index.diff(None) if item.b_path is None]

    # 获取未跟踪的文件列表
    untracked_files = repo.untracked_files

    # 将所有的更改整合到一起
    all_changes = modified_files + new_files + deleted_files + untracked_files

    return all_changes

def isdirty(repo_path):
    repo = Repo(repo_path)
    return repo.is_dirty()

def isUpdated(repo_path):
    repo = Repo(repo_path)
    repo.remotes.origin.fetch()
    local_commit = repo.head.commit
    remote_branch = 'origin/' + repo.active_branch.name
    remote_commit = repo.commit(remote_branch)
    return local_commit==remote_commit
    
