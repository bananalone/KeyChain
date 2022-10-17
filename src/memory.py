import time
import pickle
from typing import List

from data import Account, Group
from handlers import GroupsFilter, ManagerCleaner, ManagerExpander


class ManagerState:
    def __init__(self) -> None:
        self._time = time.time()
        self._groups_bytes = pickle.dumps(GroupsFilter().set_manager().groups())
    
    @property
    def time(self):
        return self._time

    def recovery(self):
        groups: List[Group] = pickle.loads(self._groups_bytes)
        ManagerCleaner().clean_all_groups()
        ManagerExpander().expand_groups(groups)


class ManagerStateRecorder:
    def __init__(self, interval: float = 10) -> None:
        self._interval = interval
        self._history: List[ManagerState] = []
        self._last_state = None
        
    def record(self):
        current_state = ManagerState()
        if self._last_state:
            if len(self._history) == 0 or self._last_state.time - self._history[-1].time >= self._interval:
                self._history.append(self._last_state)
        self._last_state = current_state

    def recovery(self):
        if self._last_state:
            self._last_state.recovery()
            self._last_state = self._history.pop() if len(self._history) > 0 else None

    

if __name__ == '__main__':
    from data import Manager
    from utils import load, dump
    
    def print_manager():
        manager = Manager()
        for group_name in manager.group_name_list:
            group = manager.get_group(group_name)
            print(f'group: {group.name}')
            for username in group.username_list:
                acc = group.get_account(username)
                print(f'username: {acc.username}')

    m = Manager()
    g = Group('g')
    g.add_account(Account('a1')).add_account(Account('a2'))
    m.add_group(g)
    print('before remove ...')
    print_manager()
    s = ManagerState()
    g.remove_account('a1')
    print('after remove ...')
    print_manager()
    s.recovery()
    print('recovery ...')
    print_manager()
    f = 'test/key_chain.pkl'
    dump(s, f)
    m.get_group('g').remove_account('a2')
    print()
    print('before load ...')
    print_manager()
    s2: ManagerState = load(f)
    s2.recovery()
    print('after load ...')
    print_manager()
    