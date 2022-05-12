import time
from functools import partial
from PyQt5 import *
from vvs_app.master_window import *
from vvs_app.QRoundPB import QRoundProgressBar


class SettingsWidget(QWidget):
    def __init__(self, masterRef, parent=None):
        super().__init__(parent)

        self.masterRef = masterRef

        self.progress_counter = 1

        self.settingsLayout = QVBoxLayout()
        self.setLayout(self.settingsLayout)

        self.settingsSplitter = QSplitter(Qt.Horizontal)
        self.settingsLayout.addWidget(self.settingsSplitter)
        self.settingsSplitter.setChildrenCollapsible(False)
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)

        self.settingsTree = QTreeWidget()
        self.settingsTree.header().hide()
        self.settingsTree.setMaximumWidth(250)
        self.settingsTree.setMinimumWidth(150)
        self.settingsSplitter.addWidget(self.settingsTree)

        self.holderWdg = QStackedWidget()
        self.settingsSplitter.addWidget(self.holderWdg)

        self.init_appearance_wdg()
        self.init_system_wdg()
        self.init_key_mapping_wdg()

        self.settingsTree.clicked.connect(self.set_current_wdg)

        self.settingsTree.setCurrentItem(self.settingsTree.topLevelItem(0))
        self.set_current_wdg()

    def set_current_wdg(self):
        current_item = self.settingsTree.currentItem().data(5, 6)
        self.holderWdg.setCurrentWidget(current_item)
        self.fill()
        self.settingsTree.currentItem().data(9, 10).setText("")

    def init_wdg_ui(self, wdg, name):
        self.v_layout = QVBoxLayout()
        wdg.setLayout(self.v_layout)
        wdg.layout().setAlignment(Qt.AlignTop)

        self.appearance_wnd_name = QLabel(name)
        self.v_layout.addWidget(self.appearance_wnd_name)

        self.spacer1 = QSpacerItem(50, 50)
        self.v_layout.addItem(self.spacer1)

        self.Grid_Layout = QGridLayout()
        self.v_layout.addLayout(self.Grid_Layout)

        self.spacer2 = QWidget()
        self.spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.v_layout.addWidget(self.spacer2)

        name_item = QTreeWidgetItem([name])
        name_item.setData(5, 6, wdg)
        name_item.setData(7, 8, self.Grid_Layout)
        self.settingsTree.addTopLevelItem(name_item)
        self.holderWdg.addWidget(wdg)

        # Add The Buttons Layout
        self.h_layout = QHBoxLayout()
        self.v_layout.addLayout(self.h_layout)
        self.h_layout.setAlignment(Qt.AlignBottom)

        self.reset_btn = QPushButton("Rest")
        self.h_layout.addWidget(self.reset_btn)
        self.reset_btn.setFixedWidth(100)

        self.reset_fun()

        self.message = QLabel("")
        self.h_layout.addWidget(self.message)
        name_item.setData(9, 10, self.message)

        self.spacer3 = QWidget()
        self.spacer3.setMinimumWidth(QSizePolicy.Expanding)
        self.h_layout.addWidget(self.spacer3)

        self.apply_close_btn = QPushButton("Save & Close")
        self.h_layout.addWidget(self.apply_close_btn)
        self.apply_close_btn.setFixedWidth(100)

        self.apply_btn = QPushButton("Save")
        self.h_layout.addWidget(self.apply_btn)
        self.apply_btn.setFixedWidth(100)
        self.apply_btn.clicked.connect(lambda: self.apply_or_reset(False))

        self.cancel_btn = QPushButton("Close")
        self.h_layout.addWidget(self.cancel_btn)
        self.cancel_btn.setFixedWidth(100)
        self.cancel_btn.clicked.connect(self.closeEvent)
        self.cancel_btn.clicked.connect(self.fill)

        self.apply_close_btn.clicked.connect(lambda: self.apply_or_reset(False, True))

    def reset_fun(self):
        progress = QRoundProgressBar()
        progress.setTextVisabile(False)
        progress.setDataPenWidth(2.5)
        progress.setValue(0)

        progress.setBarStyle(QRoundProgressBar.BarStyle.LINE)
        progress.setStyleSheet("background-color: #565656")
        progress.setFixedSize(30, 30)
        progress.hide()

        palette = QPalette()
        brush = QBrush(QColor("#ffffff"))
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        progress.setPalette(palette)
        # name_item.setData(11, 12, progress)
        self.h_layout.addWidget(progress)

        timer_button = QTimer()
        self.reset_btn.pressed.connect(lambda: self.button_pressed(progress, timer_button))
        self.reset_btn.released.connect(lambda: self.button_released(progress, timer_button))
        timer_button.timeout.connect(lambda: self.button_event_check(progress, timer_button))

    def init_appearance_wdg(self):
        self.appearance_wdg = QWidget()

        self.init_wdg_ui(self.appearance_wdg, "Appearance")

        # self.setStyleSheet("QWidget {font: 32px}")

        self.appearance_settings_list = {"Theme": QComboBox(), "Font Size": QSpinBox()}

        for item in self.appearance_settings_list:
            lbl = QLabel(item)
            self.Grid_Layout.addWidget(lbl, list(self.appearance_settings_list.keys()).index(item), 0, Qt.AlignRight)

            variable = self.appearance_settings_list[item]
            self.Grid_Layout.addWidget(variable, list(self.appearance_settings_list.keys()).index(item), 1, 1, 10, Qt.AlignLeft)
            variable.setMinimumWidth(70)

    def init_system_wdg(self):
        self.system_wdg = QWidget()

        self.init_wdg_ui(self.system_wdg, "System")

        # Content
        self.system_settings_list = {"AutoSave Steps": QSpinBox(),
                                     "AutoSave Folder MaxSize": QDoubleSpinBox(),
                                     "Always Save Before Closing": QRadioButton(),
                                     "Save New Project Folder On Close": QRadioButton()}

        for item in self.system_settings_list:
            lbl = QLabel(item)
            self.Grid_Layout.addWidget(lbl, list(self.system_settings_list.keys()).index(item), 0, Qt.AlignRight)

            variable = self.system_settings_list[item]
            self.Grid_Layout.addWidget(variable, list(self.system_settings_list.keys()).index(item), 1, 1, 10,
                                       Qt.AlignLeft)
            variable.setMinimumWidth(120)
            if type(variable) == QDoubleSpinBox:
                variable.setMaximum(100000.000)

    def init_key_mapping_wdg(self):
        self.key_mapping_wdg = QWidget()

        self.init_wdg_ui(self.key_mapping_wdg, "Key Mapping")

        # Content
        self.Key_Mapping_settings_list = ["New Graph", "Open", "Set Project Location", "Save", "Save As", "Exit",
                                          "Undo", "Redo", "Select All", "Cut", "Copy", "Paste", "Delete", "Settings Window"]

        for item in self.Key_Mapping_settings_list:
            lbl = QLabel(item)
            self.Grid_Layout.addWidget(lbl, self.Key_Mapping_settings_list.index(item), 0, Qt.AlignRight)

            KeySequence = QKeySequenceEdit()
            self.Grid_Layout.addWidget(KeySequence, self.Key_Mapping_settings_list.index(item), 1, 1, 10, Qt.AlignLeft)
            KeySequence.setMaximumWidth(150)
            KeySequence.setStat = setStat
            KeySequence.__init__ = QSEnewinit(KeySequence)

    def fill(self):
        grid_layout = self.settingsTree.currentItem().data(7, 8)
        grid_row_count = grid_layout.rowCount()
        for i in range(grid_row_count):
            lbl_wdg = grid_layout.itemAtPosition(i, 0).widget()
            variable_wdg = grid_layout.itemAtPosition(i, 1).widget()
            try:
                if grid_layout.itemAtPosition(i, 0).widget():
                    if type(variable_wdg) == QComboBox:
                        variable_wdg.clear()
                    lbl = self.masterRef.get_QWidget_content(lbl_wdg)
                    self.masterRef.set_QWidget_content(variable_wdg, self.masterRef.global_switches.switches_Dict[lbl])
            except Exception as e:
                print("Window Has Fields to fill that's why", e)

    def apply_or_reset(self, reset, close=False):
        if close:
            self.close()

        if self.settingsTree.currentItem().data(7, 8).itemAtPosition(0, 0):

            self.settingsTree.currentItem().data(9, 10).show()
            current_widget = self.settingsTree.currentItem().data(5, 6)
            grid_layout = self.settingsTree.currentItem().data(7, 8)
            grid_row_count = grid_layout.rowCount()

            changed_settings_dict = {}
            for i in range(grid_row_count):
                wdg = grid_layout.itemAtPosition(i, 1).widget()

                if wdg.isWindowModified() or type(wdg) != QKeySequenceEdit:
                    lbl = self.masterRef.get_QWidget_content(grid_layout.itemAtPosition(i, 0).widget())
                    if type(wdg) == QComboBox:
                        current = wdg.currentText()
                        wdg.removeItem(wdg.currentIndex())

                        content_list = [current]
                        for index in range(wdg.__len__()):
                            content_list.append(wdg.itemText(index))
                        wdg.clear()
                        wdg.addItems(content_list)

                        if lbl == "Theme":
                            self.masterRef.global_switches.change_theme(self.masterRef.get_QWidget_content(wdg)[0])
                    elif lbl == "Font Size":
                        self.masterRef.global_switches.update_font_size(self.masterRef.get_QWidget_content(wdg))

                    txt = self.masterRef.get_QWidget_content(wdg)
                    grid_layout.itemAtPosition(i, 1).widget().setWindowModified(False)
                    changed_settings_dict[lbl] = txt

            if changed_settings_dict:
                for i in range(len(changed_settings_dict)):
                    lbl, txt = list(changed_settings_dict.keys())[i], list(changed_settings_dict.values())[i]
                    self.masterRef.global_switches.switches_Dict[lbl] = txt
                    self.settingsTree.currentItem().data(9, 10).setText("Applied")
                if current_widget == self.key_mapping_wdg:
                    for i in range(grid_row_count):
                        lbl = self.masterRef.get_QWidget_content(grid_layout.itemAtPosition(i, 0).widget())
                        txt = self.masterRef.get_QWidget_content(grid_layout.itemAtPosition(i, 1).widget())
                        self.masterRef.actions_list[lbl].setShortcut(txt)
                elif current_widget == self.system_wdg:
                    if self.masterRef.currentNodeEditor():
                        self.masterRef.currentNodeEditor().scene.history.Edits_Counter = 0
            else:
                self.settingsTree.currentItem().data(9, 10).setText("No Changed")
                self.fill()
                for i in range(grid_row_count):
                    grid_layout.itemAtPosition(i, 1).widget().setStyleSheet("background-color: transparent")

            if reset:
                for i in range(grid_row_count):
                    wdg = grid_layout.itemAtPosition(i, 1).widget()
                    lbl = self.masterRef.get_QWidget_content(grid_layout.itemAtPosition(i, 0).widget())
                    self.masterRef.global_switches.switches_Dict[lbl] = self.masterRef.global_switches.Default_switches_Dict[lbl]
                    if type(wdg) == QKeySequenceEdit:
                        wdg.setStyleSheet("background-color: transparent")
                self.fill()
                self.settingsTree.currentItem().data(9, 10).setText("Reset")

            self.masterRef.global_switches.save_settings_to_file(self.masterRef.global_switches.switches_Dict, self.masterRef.global_switches.Settings_File)

    def closeEvent(self, event):
        self.masterRef.settingsBtn.setChecked(False)
        self.hide()

    def toggle_text_message_stat(self):
        self.settingsTree.currentItem().data(9, 10).setText("")
        i = self.settingsTree.currentItem().data(9, 10)
        if i.isHidden():
            i.show()
        else:
            i.hide()

    # Reset btn Events
    def button_pressed(self, progress, timer_button):
        self.toggle_text_message_stat()
        timer_button.start(10)
        progress.show() # progress

    def button_released(self,  progress, timer_button):
        timer_button.stop()
        progress.setValue(0) # progress
        self.progress_counter = 1
        self.toggle_text_message_stat()
        progress.hide() # progress

    def button_event_check(self,  progress, timer_button):
        if self.progress_counter == 100:
            timer_button.stop()
            self.apply_or_reset(True)
        progress.setValue(float(self.progress_counter)) # progress
        self.progress_counter += 1

def QSEnewinit(self, *__args):
    self.editingFinished.connect(lambda: self.setStat(self))

def setStat(self):
    grid_layout = self.parentWidget().layout().itemAt(2)
    grid_row_count = self.parentWidget().layout().itemAt(2).rowCount()
    count = 0

    for i in range(grid_row_count):
        txt = grid_layout.itemAtPosition(i, 1).widget().keySequence().toString()
        if txt == self.keySequence().toString() or self.keySequence().toString() == "Shift+Del":
            count += 1

    if count > 1:
        self.setStyleSheet("background-color: red")
    else:
        self.setWindowModified(True)
