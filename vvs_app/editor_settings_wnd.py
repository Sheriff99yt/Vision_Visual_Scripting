import time
from functools import partial
from PyQt5 import *
from vvs_app.master_window import *
from vvs_app.QRoundPB import QRoundProgressBar


class SettingsWidget(QWidget):
    def __init__(self, masterRef, parent=None):
        super().__init__(parent)

        self.settings_Widgets = {"Appearance": {},
                                 "System": {},
                                 "Key Mapping": {}}

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
        self.settingsTree.setRootIsDecorated(False)

        current_theme = self.masterRef.global_switches.switches_Dict["Appearance"]["Theme"][0]
        searchBar = QTreeWidgetItem(self.settingsTree)
        searchBar.setIcon(0, QIcon(f"""icons/{current_theme}/search.png"""))
        searchBar.setDisabled(True)
        self.searchwdg = QLineEdit()
        searchBar.treeWidget().setItemWidget(searchBar, 0, self.searchwdg)
        self.searchwdg.editingFinished.connect(self.main_search)
        self.searchwdg.setContentsMargins(5, 5, 5, 5)

        self.holderWdg = QStackedWidget()
        self.settingsSplitter.addWidget(self.holderWdg)

        self.init_appearance_wdg()
        self.init_system_wdg()
        self.init_key_mapping_wdg()

        self.settingsTree.clicked.connect(self.set_current_wdg)

        # print(self.settingsTree.topLevelItem(1))
        self.settingsTree.currentItemChanged.connect(self.set_current_wdg)
        self.settingsTree.setCurrentItem(self.settingsTree.topLevelItem(1))

    def set_current_wdg(self):
        current_item = self.settingsTree.currentItem().data(256, 6)
        self.holderWdg.setCurrentWidget(current_item)
        self.fill()
        self.settingsTree.currentItem().data(256, 10).setText("")

    def main_search(self):
        if self.searchwdg.text() != "":
            for window in self.settings_Widgets:
                for option in self.settings_Widgets[window]:
                    if option == self.searchwdg.text():
                        self.settingsTree.setCurrentItem(self.settingsTree.findItems(window, Qt.MatchExactly)[0])
                        if window != "Key Mapping":
                            self.settings_Widgets[window][option].parent().parent().setCurrentItem(self.settings_Widgets[window][option].parent().parent().findItems(option, Qt.MatchExactly)[0])
                        return

            self.show_short_message(wdg=self.searchwdg, color="red")

    def init_settings_window_default_ui(self, wdg, name):
        self.v_layout = QVBoxLayout()
        wdg.setLayout(self.v_layout)
        wdg.layout().setAlignment(Qt.AlignTop)

        self.appearance_wnd_name = QLabel(name)
        self.v_layout.addWidget(self.appearance_wnd_name)

        self.spacer1 = QWidget()
        self.spacer1.setMinimumHeight(40)
        self.v_layout.addWidget(self.spacer1)

        self.Grid_Layout = QTreeWidget()
        self.v_layout.addWidget(self.Grid_Layout)
        self.Grid_Layout.setContentsMargins(0, 0, 0, 0)

        # self.spacer2 = QWidget()
        # # self.spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.v_layout.addWidget(self.spacer2)

        name_item = QTreeWidgetItem([name])
        name_item.setData(256, 6, wdg)
        name_item.setData(256, 8, self.Grid_Layout)
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
        name_item.setData(256, 10, self.message)

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

    def init_appearance_wdg(self):
        self.appearance_wdg = QWidget()

        self.init_settings_window_default_ui(self.appearance_wdg, "Appearance")

        self.appearance_settings_list = {"Theme": QComboBox(), "Font Size": QSpinBox(), "Grid Size": QSpinBox()}

        self.Grid_Layout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Grid_Layout.header().hide()
        self.Grid_Layout.setRootIsDecorated(False)
        self.Grid_Layout.setColumnCount(3)
        self.Grid_Layout.setColumnWidth(0, 150)
        self.Grid_Layout.setColumnWidth(1, 150)

        for item in self.appearance_settings_list:
            Tree_Item = QTreeWidgetItem(self.Grid_Layout, [item])
            Tree_Item.setSizeHint(0, QSize(6, 6))
            value_holder = self.appearance_settings_list[item]
            Tree_Item.treeWidget().setItemWidget(Tree_Item, 1, value_holder)
            value_holder.setMinimumWidth(70)

            self.settings_Widgets["Appearance"][item] = value_holder

    def Appearance(self):
        # Apply Theme change
        self.masterRef.global_switches.change_theme()
        self.masterRef.global_switches.update_font_size()

        for act in self.masterRef.actions_creation_dict["UI"]:
            icon = self.masterRef.actions_creation_dict["UI"][act][0].iconText()
            self.masterRef.actions_creation_dict["UI"][act][0].setIcon(QIcon(self.masterRef.global_switches.get_icon(icon)))
        self.masterRef.set_nodes_icons()
        self.masterRef.nodesListWidget.addMyFunctions()
        for window in self.masterRef.graphs_parent_wdg.subWindowList():
            window.widget().scene.grScene.update_background_color()
            window.widget().code_orientation_btn.setIcon(
                QIcon(self.masterRef.global_switches.get_icon(window.widget().code_orientation_btn.windowIconText())))
            window.widget().copy_code_btn.setIcon(
                QIcon(self.masterRef.global_switches.get_icon(window.widget().copy_code_btn.windowIconText())))
            window.widget().run_btn.setIcon(
                QIcon(self.masterRef.global_switches.get_icon(window.widget().run_btn.windowIconText())))
            for node in window.widget().scene.nodes:
                node.grNode.update_node_theme(True)

    def init_system_wdg(self):
        self.system_wdg = QWidget()

        self.init_settings_window_default_ui(self.system_wdg, "System")

        # Content
        self.system_settings_list = {"AutoSave Steps": QSpinBox(),
                                     "AutoSave Folder MaxSize": QDoubleSpinBox(),
                                     "Always Save Before Closing": QRadioButton(),
                                     "Save New Project Folder On Close": QRadioButton()}

        self.Grid_Layout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Grid_Layout.header().hide()
        self.Grid_Layout.setRootIsDecorated(False)
        self.Grid_Layout.setColumnCount(3)
        self.Grid_Layout.setColumnWidth(0, 250)
        self.Grid_Layout.setColumnWidth(1, 150)
        self.Grid_Layout.setColumnWidth(1, 1)

        for item in self.system_settings_list:
            Tree_Item = QTreeWidgetItem(self.Grid_Layout, [item])

            value_holder = self.system_settings_list[item]
            Tree_Item.treeWidget().setItemWidget(Tree_Item, 1, value_holder)
            value_holder.setMinimumWidth(70)

            if type(value_holder) == QDoubleSpinBox:
                value_holder.setMaximum(100000.000)

            self.settings_Widgets["System"][item] = value_holder

    def System(self):
        # Apply System change
        if self.masterRef.graphs_parent_wdg.subWindowList():
            for window in self.masterRef.graphs_parent_wdg.subWindowList():
                window.widget().scene.history.Edits_Counter = 0

    def init_key_mapping_wdg(self):
        self.key_mapping_wdg = QWidget()

        self.init_settings_window_default_ui(self.key_mapping_wdg, "Key Mapping")

        # Content
        self.Key_Mapping_settings_list = {"File Menu":
                                              ["New Graph",
                                               "Open",
                                               "Set Project Location",
                                               "Save",
                                               "Save As",
                                               "Exit"],
                                          "Edit Menu":
                                              ["Undo",
                                               "Redo",
                                               "Select All",
                                               "Cut",
                                               "Copy",
                                               "Paste",
                                               "Delete"],
                                          "Node Editor Menu":
                                              ["Close",
                                               "Close All",
                                               "Tile",
                                               "Next",
                                               "Previous"],
                                          "Tool Bar":
                                              ["Settings Window",
                                               "Node Editor Window",
                                               "Node Designer Window",
                                               "Library Window"]}

        self.Grid_Layout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Grid_Layout.header().hide()
        self.Grid_Layout.setRootIsDecorated(False)
        self.Grid_Layout.setColumnCount(2)
        self.Grid_Layout.setColumnWidth(0, 150)


        for item in self.Key_Mapping_settings_list:
            Menus = QTreeWidgetItem(self.Grid_Layout, [item])
            Menus.setFirstColumnSpanned(True)
            for action in self.Key_Mapping_settings_list[item]:
                Tree_Item = QTreeWidgetItem(Menus, [action])

                KeySequence = QKeySequenceEdit()
                KeySequence.setStat = setStat
                KeySequence.__init__ = QSEnewinit(KeySequence)

                Tree_Item.treeWidget().setItemWidget(Tree_Item, 1, KeySequence)
                KeySequence.setMaximumWidth(150)

                self.settings_Widgets["Key Mapping"][action] = KeySequence

    def Key_Mapping(self):
        grid_row_count = list(self.settings_Widgets["Key Mapping"].keys())

        # Apply Key_Mapping change
        self.masterRef.set_actions_shortcuts()
        self.fill()
        for i in grid_row_count:
            self.settings_Widgets["Key Mapping"][i].setStyleSheet("background-color: transparent")

    def get_current_settings(self):
        current = self.settingsTree.currentItem().data(0, 0)
        grid_row_count = list(self.settings_Widgets[current].keys())

        current_settings_dict = {}
        for i in grid_row_count:
            wdg = self.settings_Widgets[current][i]
            if wdg.isWindowModified():
                return {}
            txt = self.masterRef.get_QWidget_content(wdg)

            current_settings_dict[i] = txt
        return current_settings_dict

    def apply_or_reset(self, reset, close=False):
        if close:
            self.close()

        self.settingsTree.currentItem().data(256, 10).show()
        current_window_name = self.settingsTree.currentItem().data(0, 0)

        if reset:
            self.masterRef.global_switches.switches_Dict[current_window_name] = \
            self.masterRef.global_switches.Default_switches_Dict[current_window_name]
            self.fill()

        current_settings = self.get_current_settings()
        if current_settings:
            self.masterRef.global_switches.switches_Dict[current_window_name] = current_settings

            self.__getattribute__(current_window_name.replace(" ", "_"))()

            if not reset: self.show_short_message("Applied", self.settingsTree.currentItem().data(256, 10))
            self.masterRef.global_switches.save_settings_to_file()
        else:
            self.show_short_message("No Changed", self.settingsTree.currentItem().data(256, 10))

    def fill(self):
        current_window_name = self.settingsTree.currentItem().data(0, 0)

        for i in list(self.settings_Widgets[current_window_name].keys()):
            self.masterRef.set_QWidget_content(self.settings_Widgets[current_window_name][i],
                                               self.masterRef.global_switches.switches_Dict[current_window_name][i])

    def closeEvent(self, event):
        self.masterRef.settingsBtn.setChecked(False)
        self.hide()

    def show_short_message(self, text="", wdg=None, color=False):
        timer = QTimer()
        timer.start(2000)
        timer.timeout.connect(lambda: timer.stop())
        if wdg :
            if text != "":
                wdg.setText(text)
                timer.timeout.connect(lambda: wdg.setText(""))

            if color:
                wdg.setStyleSheet(f"background-color: {color}")
                timer.timeout.connect(lambda: wdg.setStyleSheet("background-color: transparent"))

    # Reset btn
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
        # name_item.setData(256, 12, progress)
        self.h_layout.addWidget(progress)

        timer = QTimer()
        self.reset_btn.pressed.connect(lambda: self.button_pressed(progress, timer))
        self.reset_btn.released.connect(lambda: self.button_released(progress, timer))
        timer.timeout.connect(lambda: self.button_event_check(progress, timer))

    def button_pressed(self, progress, timer_button):
        timer_button.start(15)
        progress.show()

    def button_released(self, progress, timer_button):
        timer_button.stop()
        progress.setValue(0)
        self.progress_counter = 1
        self.show_short_message("Reset Done", self.settingsTree.currentItem().data(256, 10))
        progress.hide()

    def button_event_check(self, progress, timer_button):
        if self.progress_counter == 100:
            timer_button.stop()
            self.apply_or_reset(True)
        progress.setValue(float(self.progress_counter))
        self.progress_counter += 1


def QSEnewinit(self, *__args):
    self.keySequenceChanged.connect(lambda: self.setStat(self))


def setStat(self):
    self.setWindowModified(False)
    self.setStyleSheet("background-color: transparent")

    settings_Widgets = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().settings_Widgets
    grid_row_count = list(settings_Widgets["Key Mapping"].keys())
    count = 0

    for i in grid_row_count:
        if self.keySequence().toString() == settings_Widgets["Key Mapping"][i].keySequence().toString():
            count += 1

    if count > 1:
        self.setStyleSheet("background-color: red")
        self.setWindowModified(True)
