from typing import List

from PyQt5.QtWidgets import QMainWindow

from data import Account, Group
from utils import singleton


@singleton
class _State:
    def __init__(self) -> None:
        self.current_selected_group: Group = None
        self.current_groups: List[Group] = []
        self.current_accounts: List[Account] = []
        self.current_selected_account: Account = None


state = _State()