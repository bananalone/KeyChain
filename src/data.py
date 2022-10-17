import random

from utils import singleton


class Account:    
    def __init__(self, username: str, password: str = None, remark: str = None) -> None:
        self._username = username
        if password:
            self._password = password
        else:
            self.random_password()
        self._remark = remark
        
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password
    
    @property
    def remark(self):
        return self._remark
    
    def set_password(self, password: str):
        self._password = password
        
    def set_remark(self, remark: str):
        self._remark = remark

    def random_password(self):
        digits = [str(d) for d in range(10)]
        random.shuffle(digits)
        capital_latters = [chr(d) for d in range(ord('A'), ord('Z')+1)]
        random.shuffle(capital_latters)
        lower_case_latters = [chr(d) for d in range(ord('a'), ord('z')+1)]
        random.shuffle(lower_case_latters)
        special_symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', 
                           ';','<', '=', '>', '?', '@', '[', ']', '^', '_', '{', '|', '}', '~']
        random.shuffle(special_symbols)
        per_lenth = 5
        password = digits[:per_lenth] + capital_latters[:per_lenth] + lower_case_latters[:per_lenth] + special_symbols[:per_lenth]
        random.shuffle(password)
        self._password = ''.join(password)


class Group:
    def __init__(self, name: str) -> None:
        self._name = name
        self._accounts_table = dict()
        
    @property
    def name(self):
        return self._name
    
    @property
    def username_list(self):
        return list(self._accounts_table.keys())
    
    def get_account(self, username: str) -> Account:
        return self._accounts_table[username]
        
    def add_account(self, account: Account):
        if account.username in self._accounts_table:
            raise Exception(f'account[{account.username}] already in group[{self._name}]')
        self._accounts_table[account.username] = account
        return self

    def remove_account(self, username: str):
        if username in self._accounts_table:
            del self._accounts_table[username]
        return self
        

@singleton
class Manager:
    def __init__(self) -> None:
        self._group_table = dict()
        
    @property
    def group_name_list(self):
        return list(self._group_table.keys())
        
    def get_group(self, group_name: str) -> Group:
        return self._group_table[group_name]
        
    def add_group(self, group: Group):
        if group.name in self._group_table:
            raise Exception(f'group[{group.name}] already exists')
        self._group_table[group.name] = group
        return self
        
    def remove_group(self, group_name: str):
        if group_name in self._group_table:
            del self._group_table[group_name]
        return self
        


if __name__ == '__main__':
    group1 = Group('g1')
    group2 = Group('g2')
    group1.add_account(Account('a1')).add_account(Account('a2')).add_account(Account('a3'))
    group2.add_account(Account('a4')).add_account(Account('a5'))
    manager = Manager()
    manager.add_group(group1).add_group(group2)
    
    def print_manager(manager: Manager):
        for group_name in manager.group_name_list:
            group = manager.get_group(group_name)
            print(f'group: {group.name}')
            for username in group.username_list:
                acc = group.get_account(username)
                print(f'username: {acc.username}\npassword: {acc.password}\nremark: {acc.remark}')
    
    print('before remove ...')
    print_manager(Manager())
    group1.remove_account('a2')
    print('after remove ...')
    print_manager(Manager())
    print(id(Manager()) == id(Manager()))
