from git import Repo,GitCommandError
import os
import chardet
from enum import Enum
## git function

class GitFileStatus(Enum):
    UNTRACKED = 1
    MODIFIED = 2
    ADDED = 3
    CLEAN = 4
    
def check_git_status(repo_path,file_path):
    repo = Repo(repo_path)
    
    file_relative_path = file_path.replace(repo_path, '')  # 获取文件在仓库中的相对路径

    if file_relative_path in repo.untracked_files:
        return GitFileStatus.UNTRACKED
    elif file_relative_path in [item.a_path for item in repo.index.diff(None)]:
        return GitFileStatus.MODIFIED
    elif file_relative_path in [item.a_path for item in repo.index.diff('HEAD')]:
        return GitFileStatus.ADDED
    else:
        return GitFileStatus.CLEAN
    
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

    # 获取被修改的文件列表，转换为绝对路径
    modified_files = [os.path.abspath(os.path.join(repo_path, item.a_path)) for item in repo.index.diff(None)]
  
    # 获取新增的文件列表，转换为绝对路径
    untracked_files = [os.path.abspath(os.path.join(repo_path, item)) for item in repo.untracked_files]
  
    # 检查复杂的更改
    diff_index = repo.index.diff(repo.head.commit)
    
    added = [os.path.abspath(os.path.join(repo_path, d.a_path)) for d in diff_index.iter_change_type('A')]
    deleted = [os.path.abspath(os.path.join(repo_path, d.a_path)) for d in diff_index.iter_change_type('D')]
    renamed = [f"{os.path.abspath(os.path.join(repo_path, d.a_path))} -> {os.path.abspath(os.path.join(repo_path, d.b_path))}" for d in diff_index.iter_change_type('R')]

    result = {
        'modified': modified_files,
        'untracked': untracked_files,
        'added': added,
        'deleted': deleted,
        'renamed': renamed,
    }
    
    # 数量统计
    result['modified_count'] = len(modified_files)
    result['untracked_count'] = len(untracked_files)
    result['added_count'] = len(added)
    result['deleted_count'] = len(deleted)
    result['renamed_count'] = len(renamed)
    result['total_count'] = sum(result[key] for key in result if key.endswith('_count'))

    return result

def get_original_file(repo_path, file_path):
    repo = Repo(repo_path)
    blob = repo.head.commit.tree / file_path
    file_data = blob.data_stream.read()
    
    try:
        result = chardet.detect(file_data)
        encoding = result['encoding']
        
        file_content = file_data.decode(encoding)  
        return file_content.splitlines()
    except Exception as e:
        print(str(e))  # 输出错误信息
        return "Can not be read"  # 返回预设的信息

def get_modified_file(repo_path, file_path):
    repo = Repo(repo_path)
    file_path = repo.working_tree_dir + '/' + file_path

    try:
        with open(file_path, 'rb') as file:  # 先以二进制模式打开文件
            file_data = file.read()
            
        result = chardet.detect(file_data)  # 检测文件编码
        encoding = result['encoding']
        
        with open(file_path, 'r', encoding=encoding) as file:  # 再以检测到的编码打开文件
            file_text = file.read()
            return file_text.splitlines()
    except Exception as e:
        print(str(e))  # 输出错误信息
        return "Can not be read"  # 返回预设的信息

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

def git_commit(repo_path, commit_message):
    try:
        repo = Repo(repo_path)
        repo.git.add(update=True)
        repo.index.commit(commit_message)
        return 'Commit successful'
    except GitCommandError as error:
        return f'Error: {error}'
    
def git_push(repo_path):
    try:
        repo = Repo(repo_path)
        origin = repo.remote(name='origin')
        origin.push()
        return 'Push successful'
    except GitCommandError as error:
        return f'Error: {error}'

def git_pull(repo_path):
    try:
        repo = Repo(repo_path)
        origin = repo.remote(name='origin')
        origin.pull()
        return 'Pull successful'
    except GitCommandError as error:
        return f'Error: {error}'
