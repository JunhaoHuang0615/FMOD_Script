from Data import GitRepoData
from MyTools import My_QTTool
class DataManager:
    def __init__(self):
        self.data = {}  #初始化字典
        self.opened_git_group = None
        self.opened_git_group_id = None 
        self.init()

    def add_git_group(self, git_group):
        if isinstance(git_group, GitRepoData.GitGroup):  #检查对象类型是否为GitGroup
            self.data[git_group.guid] = git_group  #如果是，添加到字典
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
            self.opened_git_group_id = self.opened_git_group.guid
            return self.opened_git_group
    
    def save_to_file(self):
        data_group_ls = list(self.data.values())
        if len(data_group_ls) > 0:
            GitRepoData.write_gitgroups_json(data_group_ls)
        else:
            My_QTTool.show_message("No Group Found",True)
            
    def read_from_file(self):
        read_groups = GitRepoData.read_gitgroups_json()
        if len(read_groups) >0:
            for group in read_groups:
            # Do something with 'group'
                self.add_git_group(group)
                if(group.preferred == True):
                    self.opened_git_group = group
                    self.opened_git_group_id = group.guid
        else:
            self.get_prefered_git_group()
        
    def init(self):
        self.read_from_file()
        pass