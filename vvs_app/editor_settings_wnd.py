import time
from functools import partial
from PyQt5 import *
from vvs_app.master_window import *
from qroundprogressbar import QRoundProgressBar


class settingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterRef = None

        self.progress_counter = 1

        self.settingsLayout = QVBoxLayout()
        self.setLayout(self.settingsLayout)

        self.settingsSplitter = QSplitter(Qt.Horizontal)
        self.settingsLayout.addWidget(self.settingsSplitter)
        self.settingsSplitter.setChildrenCollapsible(False)

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

        self.settingsTree.clicked.connect(self.setCurrentWdg)

    def setCurrentWdg(self):
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
        # # reset btn
        # self.reset_btn = QPushButton("Rest")
        # self.h_layout.addWidget(self.reset_btn)
        # self.reset_btn.setFixedWidth(100)
        #
        # self.message = QLabel("")
        # self.h_layout.addWidget(self.message)
        # name_item.setData(9, 10, self.message)
        #
        # self.reset_btn.pressed.connect(self.button_pressed)
        # self.reset_btn.released.connect(self.button_released)
        #
        # self.timer_button = QTimer()
        # self.timer_button.timeout.connect(lambda: self.button_event_check())
        # self.button_held_time = 0
        # # reset btn
        self.spacer3 = QWidget()
        self.spacer3.setMinimumWidth(QSizePolicy.Expanding)
        self.h_layout.addWidget(self.spacer3)

        self.apply_btn = QPushButton("Apply")
        self.h_layout.addWidget(self.apply_btn)
        self.apply_btn.setFixedWidth(100)
        self.apply_btn.clicked.connect(lambda: self.apply_or_reset(False))

        self.cancel_btn = QPushButton("Close")
        self.h_layout.addWidget(self.cancel_btn)
        self.cancel_btn.setFixedWidth(100)
        self.cancel_btn.clicked.connect(self.closeEvent)

    def reset_fun(self):
        progress = QRoundProgressBar()
        progress.text_visiablity = False
        progress.m_dataPenWidth = 2.5
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

        self.Appearance_settings_list =[]

    def init_system_wdg(self):

        self.system_wdg = QWidget()

        self.init_wdg_ui(self.system_wdg, "System")

        # Content
        self.System_settings_list = ["AutoSave Trigger", "AutoSave Folder MaxSize"]

        # Edits AutoSave Trigger
        self.autoSaveLbl = QLabel("AutoSave Trigger")
        self.Grid_Layout.addWidget(self.autoSaveLbl, 0, 0, Qt.AlignRight)
        self.Grid_Layout.setColumnMinimumWidth(0, 50)

        self.autoSaveSteps = QSpinBox()
        self.Grid_Layout.addWidget(self.autoSaveSteps, 0, 1, 1, 10, Qt.AlignLeft)
        self.autoSaveSteps.setMinimumWidth(50)

        # Edit AutoSave Folder MaxSize
        self.autoSaveFolderMaxSizeLbl = QLabel("AutoSave Folder MaxSize")
        self.Grid_Layout.addWidget(self.autoSaveFolderMaxSizeLbl, 1, 0, Qt.AlignRight)
        self.Grid_Layout.setColumnMinimumWidth(0, 50)

        self.autoSaveFolderMaxSizeSB = QDoubleSpinBox()
        self.autoSaveFolderMaxSizeSB.setDecimals(3)
        self.autoSaveFolderMaxSizeSB.setMinimum(0.001)
        self.Grid_Layout.addWidget(self.autoSaveFolderMaxSizeSB, 1, 1, Qt.AlignLeft)
        self.autoSaveFolderMaxSizeSB.setMinimumWidth(50)

    def init_key_mapping_wdg(self):

        self.key_mapping_wdg = QWidget()

        self.init_wdg_ui(self.key_mapping_wdg, "Key Mapping")

        # Content
        self.Key_Mapping_settings_list = ["New Graph", "Open", "Set Project Location", "Save", "Save As", "Exit",
                                          "Undo", "Redo", "Cut", "Copy", "Paste", "Delete", "Settings Window"]

        for item in self.Key_Mapping_settings_list:
            lbl = QLabel(item)
            self.Grid_Layout.addWidget(lbl, self.Key_Mapping_settings_list.index(item), 0, Qt.AlignRight)

            KeySequence = QKeySequenceEdit()
            self.Grid_Layout.addWidget(KeySequence, self.Key_Mapping_settings_list.index(item), 1, 1, 10, Qt.AlignLeft)
            KeySequence.setMaximumWidth(100)

    def fill(self):
        grid_layout = self.settingsTree.currentItem().data(7, 8)
        grid_row_count = grid_layout.rowCount()

        for i in range(grid_row_count):
            try:
                if grid_layout.itemAtPosition(i, 1).widget():
                    lbl = self.masterRef.get_settings_content(grid_layout.itemAtPosition(i, 0).widget())
                    self.masterRef.set_settings_content(grid_layout.itemAtPosition(i, 1).widget(), self.masterRef.global_switches.switches_Dict[lbl])
            except Exception as e:
                print("Window Has Fields to fill that's why", e)

    def apply_or_reset(self, reset):
        self.settingsTree.currentItem().data(9, 10).show()
        grid_layout = self.settingsTree.currentItem().data(7, 8)
        grid_row_count = grid_layout.rowCount()

        if grid_layout.itemAtPosition(0, 0):
            if reset:
                for i in range(grid_row_count):
                    lbl = self.masterRef.get_settings_content(grid_layout.itemAtPosition(i, 0).widget())
                    self.masterRef.global_switches.switches_Dict[lbl] = self.masterRef.global_switches.Default_switches_Dict[lbl]
                self.fill()

                self.settingsTree.currentItem().data(9, 10).setText("Reset")
            else:
                self.settingsTree.currentItem().data(9, 10).setText("Applied")
                for i in range(grid_row_count):
                    lbl = self.masterRef.get_settings_content(grid_layout.itemAtPosition(i, 0).widget())
                    txt = self.masterRef.get_settings_content(grid_layout.itemAtPosition(i, 1).widget())
                    self.masterRef.global_switches.switches_Dict[lbl] = txt

            if self.settingsTree.currentItem().data(5, 6) == self.key_mapping_wdg:
                for i in range(grid_row_count):
                    lbl = self.masterRef.get_settings_content(grid_layout.itemAtPosition(i, 0).widget())
                    txt = self.masterRef.get_settings_content(grid_layout.itemAtPosition(i, 1).widget())
                    self.masterRef.actions_list[lbl].setShortcut(txt)
            elif self.settingsTree.currentItem().data(5, 6) == self.system_wdg:
                if self.masterRef.CurrentNodeEditor():
                    self.masterRef.CurrentNodeEditor().scene.history.Edits_Counter = 0

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
