from typing import List

from data import Account, Group
from utils import singleton


@singleton
class _State:
    def __init__(self) -> None:
        self.current_selected_group: Group = None
        self.current_groups: List[Group] = []
        self.current_accounts: List[Account] = []


state = _State()