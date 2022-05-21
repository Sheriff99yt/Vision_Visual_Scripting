import json
import os

from nodeeditor.utils import loadStylesheets


class GlobalSwitches:
    def __init__(self, master):
        self.master_ref = master
        self.Settings_Directory = f"{self.master_ref.files_widget.default_system_dir}/Preferences"
        self.Settings_File = self.Settings_Directory + f"/Settings.json"
        self.themes = {"Night": "qss/nodeeditor-night.qss", "Light": "qss/nodeeditor-light.qss"}

        self.Default_switches_Dict = {"AutoSave Steps": 30,
                                      "AutoSave Folder MaxSize": 500,
                                      "Always Save Before Closing": True,
                                      "Save New Project Folder On Close": False,

                                      "Theme": ["Night", "Light"],
                                      "Font Size": 16,

                                      "New Graph": "Ctrl+N",
                                      "Open": "Ctrl+O",
                                      "Set Project Location": "Ctrl+Shift+O",
                                      "Save": "Ctrl+S",
                                      "Save As": "Ctrl+Shift+S",
                                      "Exit": "Ctrl+Q",

                                      "Undo": "Ctrl+Z",
                                      "Redo": "Ctrl+Shift+Z",
                                      "Cut": "Ctrl+X",
                                      "Copy": "Ctrl+C",
                                      "Paste": "Ctrl+V",
                                      "Delete": "Del",

                                      "Settings Window": "Ctrl+Shift+S",
                                      "Select All": "Ctrl+A"
                                      }

        if os.path.isfile(self.Settings_File):
            # Read data from file
            self.switches_Dict = json.load(open(self.Settings_File))
        else:
            if os.path.exists(self.Settings_Directory) is False:
                os.makedirs(self.Settings_Directory)

            self.switches_Dict = self.Default_switches_Dict

            self.save_settings_to_file(self.switches_Dict, self.Settings_File)

    def save_settings_to_file(self, data, file_path):
        """Serializes/Saves Data Into filePath

        :param data :Is The Data Needed To Be Saved
        :param file_path :Full Path Of The File That Data Will Be Saved in
        """
        json.dump(data, open(file_path, 'w'))

    def update_font_size(self, size):
        s, z = "{font:", "}"
        self.master_ref.setStyleSheet(f"QWidget {s}{size}px{z}")
        if self.master_ref.settingsWidget:
            self.master_ref.settingsWidget.setStyleSheet(f"QWidget {s}{size}px{z}")

    def change_theme(self, theme):
        self.master_ref.qss_theme = self.themes[theme]
        self.master_ref.stylesheet_filename = os.path.join(os.path.dirname(__file__), self.master_ref.qss_theme)

        loadStylesheets(
            os.path.join(os.path.dirname(__file__), self.master_ref.qss_theme), self.master_ref.stylesheet_filename)
