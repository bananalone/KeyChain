from typing import List
import pickle

from data import Account, Group
from handlers import GroupsFilter, ManagerCleaner, ManagerExpander
from memory import BaseState
from copy import deepcopy


class _UiState:
    def __init__(self) -> None:
        self.current_selected_group: Group = None
        self.current_groups: List[Group] = []
        self.current_accounts: List[Account] = []
        self.current_selected_account: Account = None
        self.current_file = 'Untitled'
        self.saved = True
        self.windowStaysOnTop = False

ui_state = _UiState()


class UiState(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self._ui_state = deepcopy(ui_state)

    def recovery(self):
        ui_state.__dict__.update(self._ui_state.__dict__)


class ManagerState(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self._groups_bytes = pickle.dumps(GroupsFilter().set_manager().groups())

    def recovery(self):
        groups: List[Group] = pickle.loads(self._groups_bytes)
        ManagerCleaner().clean_all_groups()
        ManagerExpander().expand_groups(groups)


class AppState(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self.ui_state = UiState()
        self.manager_state = ManagerState()

    def recovery(self):
        self.ui_state.recovery()
        self.manager_state.recovery()

