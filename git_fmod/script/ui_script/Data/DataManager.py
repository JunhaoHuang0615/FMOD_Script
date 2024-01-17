from Data import GitRepoData

class DataManager:
    def __init__(self):
        self.data = {}  #初始化字典
        self.opened_git_group = None 

    def add_git_group(self, git_group):
        if isinstance(git_group, GitRepoData.GitGroup):  #检查对象类型是否为GitGroup
            self.data[git_group.group_name] = git_group  #如果是，添加到字典
        else:
            print("Provided object is not of type GitGroup")  #如果不是，输出错误消息
    def get_prefered_git_group(self):
        if self.opened_git_group != None:
            return self.opened_git_group
        else:
            #先创建一个空的
            git_repo_data_list = {}
            default_group_name = "New Templete"
            default_prefered = True
            self.opened_git_group = GitRepoData.GitGroup(default_group_name,git_repo_data_list,default_prefered)
            self.add_git_group(self.opened_git_group)
            return self.opened_git_group
    def init():
        
        pass