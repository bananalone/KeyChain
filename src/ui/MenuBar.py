from pathlib import Path

from PyQt5.QtWidgets import QMenuBar, QFileDialog, qApp, QMessageBox, QInputDialog

from ui.state import ui_state, ManagerState, AppState
from ui.interface import Paintable
from utils import dump, load
from data import Group, Manager
from handlers import GroupsFilter, ManagerCleaner
from memory import StateRecorder


class MenuBar(QMenuBar, Paintable):
    def __init__(self, parent: Paintable) -> None:
        super().__init__()
        self._parent = parent
        self._manager = Manager()
        self._recorder = StateRecorder()
        self._file_path = None
        self._file_menu = self.addMenu('File')
        self._edit_menu = self.addMenu('Edit')
        self._setting_menu = self.addMenu('Setting')
        self._help_menu = self.addMenu('Help')
        
    def paint(self):
        self._create_file_menu()
        self._create_edit_menu()
        self._create_setting_menu()
        self._create_help_menu()

    def repaint(self):
        self._parent.repaint()

    def _create_file_menu(self):
        self._file_menu.clear()
        new_file = self._file_menu.addAction('New')
        new_file.triggered.connect(self._new_file)
        open_file = self._file_menu.addAction('Open')
        open_file.triggered.connect(self._open_file)
        self._file_menu.addSeparator()
        save = self._file_menu.addAction('Save')
        save.triggered.connect(self._save)
        save_as = self._file_menu.addAction('Save as')
        save_as.triggered.connect(self._save_as)
        self._file_menu.addSeparator()
        quit_app = self._file_menu.addAction('Quit')
        quit_app.triggered.connect(self.quit_app)

    def _create_edit_menu(self):
        self._edit_menu.clear()
        if not self._recorder.empty():
            undo = self._edit_menu.addAction('Undo')
            undo.triggered.connect(self._undo)
        add_group = self._edit_menu.addAction('Add group')
        add_group.triggered.connect(self._add_group)
        remove_group = self._edit_menu.addAction('Remove group')
        remove_group.triggered.connect(self._remove_group)

    def _create_setting_menu(self):
        self._setting_menu.clear()
        stays_on_top = self._setting_menu.addAction('Stays on top')
        stays_on_top.setCheckable(True)
        stays_on_top.triggered.connect(self._stays_on_top)
        stays_on_top.setChecked(ui_state.windowStaysOnTop)

    def _create_help_menu(self):
        self._help_menu.clear()
        help_key_chain = self._help_menu.addAction('KeyChain')
        help_key_chain.triggered.connect(self._help)
        self._help_menu.addSeparator()
        about_key_chain = self._help_menu.addAction('About')
        about_key_chain.triggered.connect(self._about)

    def _new_file(self):
        if not self._save_with_question():
            return
        self._file_path = None
        self._recorder.reset()
        ManagerCleaner().clean_all_groups()
        ui_state.current_file = 'Untitled'
        ui_state.saved = True
        ui_state.current_selected_group = None
        ui_state.current_groups = []
        ui_state.current_selected_account = None
        ui_state.current_accounts = []
        self.repaint()

    def _open_file(self):
        if not self._save_with_question():
            return
        file_path, file_types = QFileDialog.getOpenFileName(self, 'Open file', '/', '*.kc')
        if len(file_path) > 0:
            manager_state: ManagerState = load(file_path)
            manager_state.recovery()
            self._recorder.reset()
            self._file_path = file_path
            ui_state.current_file = Path(file_path).stem
            ui_state.current_selected_account = None
            ui_state.current_selected_group = None
            ui_state.current_groups = GroupsFilter().set_manager().groups()
            ui_state.current_accounts = []
            ui_state.saved = True
            self.repaint()

    def _save(self):
        if ui_state.saved:
           return
        if self._file_path:
            current_state: AppState = self._recorder.last_state()
            if not current_state:
                current_state = AppState()
            if current_state:
                dump(current_state.manager_state, self._file_path)
                ui_state.current_file = Path(self._file_path).stem
                ui_state.saved = True
                self.repaint()
        else:
            self._save_as()
    
    def _save_as(self):
        file_path, file_type = QFileDialog.getSaveFileName(self, 'Save as', '/', '*.kc')
        current_state: AppState = self._recorder.last_state()
        if not current_state:
            current_state = AppState()
        if len(file_path) > 0 and current_state:
            dump(current_state.manager_state, file_path)
            self._file_path = file_path
            self._recorder.reset()
            ui_state.current_file = Path(self._file_path).stem
            ui_state.saved = True
            self.repaint()

    def _save_with_question(self):
        if not ui_state.saved:
            btn = QMessageBox.question(
                self,
                'Notice', 'File not saved, do you want to save it?', 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            if btn == QMessageBox.StandardButton.Yes:
                self._save()
                if not ui_state.saved:
                    return False
            elif btn == QMessageBox.StandardButton.Cancel:
                return False
        return True

    def quit_app(self):
        if not self._save_with_question():
            return
        qApp.exit()

    def _undo(self):
        if not self._recorder.empty():
            current_state = self._recorder.pop_state()
            if not current_state:
                return
            current_state.recovery()
            self.repaint()

    def _add_group(self):
        text, ok = QInputDialog.getText(self, 'Add group', 'Input group name:')
        if ok:
            if len(text) > 0 and text in GroupsFilter().set_manager().group_name_list():
                QMessageBox.about(self, 'Add group error', f'{text} already exists')
                return
            group = Group(text)
            self._recorder.record(AppState())
            self._manager.add_group(group)
            ui_state.current_selected_account = None
            ui_state.current_accounts = []
            ui_state.current_selected_group = group
            ui_state.current_groups = GroupsFilter().set_manager().groups()
            ui_state.saved = False
            self.repaint()

    def _remove_group(self):
        text, ok = QInputDialog.getText(self, 'Delete group', 'Input group name:')
        if ok:
            if len(text) > 0 and text not in GroupsFilter().set_manager().group_name_list():
                QMessageBox.about(self, 'Delete group error', f'{text} not exists')
                return
            self._manager.remove_group(text)
            ui_state.current_selected_group = ui_state.current_selected_group if text == ui_state.current_selected_group else None
            ui_state.current_groups = GroupsFilter().set_manager().groups()
            if not ui_state.current_selected_group:
                ui_state.current_selected_account = None
                ui_state.current_accounts = []
            ui_state.saved = False
            self.repaint()

    def _stays_on_top(self):
        ui_state.windowStaysOnTop = not ui_state.windowStaysOnTop
        self.repaint()

    def _help(self):
        QMessageBox.about(
            self,
            'Help',
            'Keychain is an offline password manager, which supports the classification of account passwords by group, and the import and export of files'
        )

    def _about(self):
        QMessageBox.about(
            self,
            'About',
            'Made by bananalone'
        )
