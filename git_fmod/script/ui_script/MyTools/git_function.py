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
    remote_branches = [str(ref).replace("origin/", "") for ref in repo.remotes.origin.refs]

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