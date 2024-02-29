import os
import json
from git import Repo
import uuid
from MyTools import My_QTTool


class GitRepoInfo:
    def __init__(self, name="", remote_url="", local_path="", id=None):
        self.id = id if id else str(uuid.uuid4())
        self.name = name  # 名称
        self.remote_url = remote_url  # 远程仓库地址
        self.local_path = local_path  # 本地路径

        try:
            repo = Repo(local_path)
            self.branch = repo.active_branch.name
        except:
            self.branch = None 
            
    def setName(self,name):
        self.name = name
        
    def setremote_url(self,remote_url):
        self.remote_url = remote_url
    
    def setlocal_path(self,local_path):
        self.local_path = local_path
    
    def console_data(self):
        # 返回一个包含GitRepoInfo信息的字符串
        return self.name + " | " + self.remote_url + " | " + self.local_path
    
            

class GitGroup:
    def __init__(self, group_name="", git_repos={}, preferred = False,id = None):
        self.group_name = group_name  # 组名
        self.preferred = preferred  # 是否首选
        self.guid = id if id else str(uuid.uuid4())
        self.git_repos = {}  # GitRepoInfo的字典
        if isinstance(git_repos, list):
            for repo in git_repos:
                assert isinstance(repo, GitRepoInfo)
                self.git_repos[repo.id] = repo  # 使用id作为键，GitRepoInfo实例作为值
        else:
            self.git_repos = git_repos
            
    def add_or_update_git_repo(self, git_repo:GitRepoInfo):
        self.git_repos[git_repo.id] = git_repo
    
    def modify_group_name(self,group_name):
        self.group_name = group_name
        
    def create_and_add_git_repo(self, name, remote_url, local_path, id=None):
        if id in self.git_repos:
            print(f"Object with name {id} already exists.")
            return

        git_repo = GitRepoInfo(name, remote_url, local_path, id)
        self.git_repos[git_repo.id] = git_repo
    
    def clear_git_repo(self):
        self.git_repos = {}
    
    def get_repo_info_strings(self):
        # 获取self.git_repos中所有GitRepoInfo的信息字符串
        info_strings = [repo.console_data() for repo in self.git_repos.values()]
        # 用换行符将所有的信息字符串拼接成一条长的字符串
        return '\n'.join(info_strings)
    

def write_gitgroups_json(git_groups):
    data = []

    for git_group in git_groups:
        group_data = {"group_name": git_group.group_name, "guid":git_group.guid, "preferred": git_group.preferred, "git_repos": {}}

        for id, repo in git_group.git_repos.items():
            group_data["git_repos"][id] = repo.__dict__

        data.append(group_data)

    target_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
    target_file = 'config.json'
    target_path = os.path.join(target_dir, target_file)
    
    # 检查目标目录是否存在，如果不存在则创建
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(target_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    My_QTTool.show_message("Config Saved to the Path: " + target_path)
    
    
        
def read_gitgroups_json():
    git_groups = []
    try:
        target_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json')
        with open(target_path, 'r') as f:
            data = json.load(f)

        for group_data in data:
            git_repos = {}
            for id, repo_data in group_data["git_repos"].items():
                # print(id)
                # print(repo_data['id'])
                # print(repo_data['name'])
                repo = GitRepoInfo(repo_data['name'], repo_data['remote_url'], repo_data['local_path'], id=repo_data['id'])
                git_repos[id] = repo
            # print(group_data['group_name'])
            # print(git_repos)
            # print(group_data['preferred'])
            # print(group_data['guid'])
            git_group = GitGroup(group_data['group_name'], git_repos, group_data['preferred'], group_data['guid'])
            git_groups.append(git_group)

        return git_groups

    except FileNotFoundError:
        print("The specified file could not be found.")
        return git_groups
    except json.JSONDecodeError:
        print("There was an error decoding the JSON file.")
        return git_groups
    except Exception as e:
        print(f"An error occurred: {e}")
        return git_groups

# # 使用这个方法
# group = read_gitgroup_json('gitgroup.json')

# # 使用这个方法
# repo1 = GitRepoInfo(True, "Repo1", "https://remote_url1", "/path/to/repo1")
# repo2 = GitRepoInfo(False, "Repo2", "https://remote_url2", "/path/to/repo2")

# group = GitGroup("MyGroup", [repo1, repo2])

# write_gitgroup_json(group, 'gitgroup.json')