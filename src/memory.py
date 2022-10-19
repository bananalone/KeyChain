import time
from typing import List

from utils import singleton


class BaseState:
    def __init__(self) -> None:
        self._time = time.time()
    
    @property
    def time(self):
        return self._time

    def recovery(self):
        raise NotImplementedError


@singleton
class StateRecorder:
    def __init__(self) -> None:
        self._interval = 10
        self._history: List[BaseState] = []
        self._last_state = None

    def record(self, state: BaseState):
        if self._last_state:
            if len(self._history) == 0 or self._last_state.time - self._history[-1].time >= self._interval:
                self._history.append(self._last_state)
        self._last_state = state

    def pop_state(self):
        if self._last_state:
            last_state = self._last_state
            if len(self._history) == 0:
                self._last_state = None
            else:
                self._last_state = self._history.pop()
            return last_state
        return None
    
    def last_state(self):
        if self._last_state:
            return self._last_state
        return None

    def empty(self):
        return True if not self._last_state else False

    def reset(self):
        self._history: List[BaseState] = []
        self._last_state = None
        return self



# class ManagerStateRecorder:
#     def __init__(self) -> None:
#         self._interval = 10
#         self._history: List[ManagerState] = []
#         self._last_state = None

#     def record(self):
#         current_state = ManagerState()
#         if self._last_state:
#             if len(self._history) == 0 or self._last_state.time - self._history[-1].time >= self._interval:
#                 self._history.append(self._last_state)
#         self._last_state = current_state

#     def pop_state(self):
#         if self._last_state:
#             last_state = self._last_state
#             if len(self._history) == 0:
#                 self._last_state = None
#             else:
#                 self._last_state = self._history.pop()
#             return last_state
#         return ManagerState()
    
#     def last_state(self):
#         if self._last_state:
#             return self._last_state
#         return ManagerState()

#     def empty(self):
#         return True if not self._last_state else False

#     def reset(self):
#         self._history: List[ManagerState] = []
#         self._last_state = None
#         return self
