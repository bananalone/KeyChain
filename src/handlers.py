from typing import List, Callable

from data import Account, Group, Manager


class GroupsFilter:
    def __init__(self) -> None:
        self._all_groups: List[Group] = []
        self._groups: List[Group] = []
        
    def set_groups(self, groups: List[Group]):
        self._all_groups = groups.copy()
        self._groups = groups.copy()
        return self
    
    def set_manager(self):
        self._groups = []
        manager = Manager()
        for group_name in manager.group_name_list:
            self._groups.append(manager.get_group(group_name))
        self._all_groups = self._groups.copy()
        return self

    def filter(self, key: Callable):
        groups = []
        for group in self._groups:
            if key(group):
                groups.append(group)
        self._groups = groups
        return self
    
    def empty_group(self):
        groups = []
        for group in self._groups:
            if len(group.username_list) == 0:
                groups.append(group)
        self._groups = groups
        return self

    def groups(self, reverse: bool = False) -> List[Group]:
        if not reverse:
            groups = self._groups
        else:
            groups = []
            for group_a in self._all_groups:
                find = False
                for group_b in self._groups:
                    if group_a.name == group_b.name:
                        find = True
                if not find:
                    groups.append(group_a)
        self._groups = []
        self._all_groups = []
        return groups
    
    def group_name_list(self, reverse: bool = False) -> List[str]:
        groups = self.groups(reverse)
        gro_name_list = []
        for group in groups:
            gro_name_list.append(group.name)
        return gro_name_list

    
class AccountsFilter:
    def __init__(self) -> None:
        self._accounts: List[Account] = []
        self._all_accounts: List[Account] = []
        
    def set_accounts(self, accounts: List[Account]):
        self._accounts = accounts.copy()
        self._all_accounts = accounts.copy()
        return self
        
    def set_group(self, group: Group):
        accounts = []
        for username in group.username_list:
            accounts.append(group.get_account(username))
        self._accounts = accounts
        return self

    def filter(self, key: Callable):
        accounts = []
        for account in self._accounts:
            if key(account):
                accounts.append(account)
        self._accounts = accounts
        return self
        
    def accounts(self, reverse: bool = False) -> List[Account]:
        if not reverse:
            accounts = self._accounts
        else:
            accounts = []
            for account_a in self._all_accounts:
                find = False
                for account_b in self._accounts:
                    if account_a.username == account_b.username:
                        find = True
                if not find:
                    accounts.append(account_a)
        self._accounts = []
        self._all_accounts = []
        return accounts

    def username_list(self, reverse: bool = False) -> List[str]:
        accounts = self.accounts(reverse)
        uname_list = []
        for account in accounts:
            uname_list.append(account.username)
        return uname_list


class GroupExpander:
    def __init__(self, group: Group) -> None:
        self._group = group
    
    def expand_accounts(self, accounts: List[Account], replace: bool = True):
        for account in accounts:
            if account.username not in self._group.username_list:
                self._group.add_account(account)
            elif replace:
                    self._group.remove_account(account.username).add_account(account)
        return self
    
    def expand_accounts_in_group(self, group: Group, replace: bool = True):
        accounts = AccountsFilter().set_group(group).accounts()
        return self.expand_accounts(accounts, replace)


class ManagerExpander:
    def __init__(self) -> None:
        self._manager = Manager()
    
    def expand_groups(self, groups: List[Group], replace: bool = True):
        for group in groups:
            if group.name not in self._manager.group_name_list:
                self._manager.add_group(group)
            elif replace:
                self._manager.remove_group(group.name).add_group(group)
        return self


class GroupCleaner:
    def __init__(self, group: Group) -> None:
        self._group = group
        
    def clean_accounts(self, accounts: List[Account]):
        for account in accounts:
            self._group.remove_account(account.username)
        return self
    
    def clean_username_list(self, username_list: List[str]):
        for username in username_list:
            self._group.remove_account(username)
        return self
        
    def clean_all_accounts(self):
        for username in self._group.username_list:
            self._group.remove_account(username)
        return self


class ManagerCleaner:
    def __init__(self) -> None:
        self._manager = Manager()
        
    def clean_groups(self, groups: List[Group]):
        for group in groups:
            self._manager.remove_group(group.name)
        return self
    
    def clean_group_name_list(self, group_name_list: List[str]):
        for group_name in group_name_list:
            self._manager.remove_group(group_name)
        return self
    
    def clean_all_groups(self):
        for group_name in self._manager.group_name_list:
            self._manager.remove_group(group_name)
        return self
    