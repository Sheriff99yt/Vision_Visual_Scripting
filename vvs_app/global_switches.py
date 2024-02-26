import json
import os

from utils import loadStylesheets


class GlobalSwitches:
    def __init__(self, master):
        self.master_ref = master
        self.Settings_Directory = f"{self.master_ref.files_widget.default_system_dir}/Preferences"
        self.Settings_File = self.Settings_Directory + f"/Settings.json"

        self.themes = {"Dark": "qss/nodeeditor-night.qss", "Light": "qss/nodeeditor-light.qss"}

        self.themes_colors = {"Nodes": ["Text", "Background", "Outline", "", ""],
                              "Dark": ["#ffffff", "#282828", "#282828", "#828282", "#ffffff"],
                              "Light": ["#1f1f1f", "#828282", "#565656", "#282828", "#1f1f1f"]}

        self.Default_switches_Dict = {"Appearance":
                                          {
                                              "Theme": ["Dark", "Light"],
                                              "Font Size": 16,
                                              "Grid Size": 30
                                          },
                                      "System":
                                          {
                                              "AutoSave Steps": 30,
                                              "AutoSave Folder MaxSize": 500.0,
                                              "Always Save Before Closing": True,
                                              "Save New Project Folder On Close": False
                                          },
                                      "Key Mapping":
                                          {
                                              "New Graph": "Ctrl+N",
                                              "Open": "Ctrl+O",
                                              "Set Project Location": "Ctrl+Shift+O",
                                              "Save": "Ctrl+S",
                                              "Save As": "Ctrl+Shift+S",
                                              "Exit": "Ctrl+Q",

                                              "Undo": "Ctrl+Z",
                                              "Redo": "Ctrl+Shift+Z",
                                              "Select All": "Ctrl+A",
                                              "Cut": "Ctrl+X",
                                              "Copy": "Ctrl+C",
                                              "Paste": "Ctrl+V",
                                              "Delete": "Del",

                                              "Close": "Q",
                                              "Close All": "Shift+Q",
                                              "Tile": "T",
                                              "Next": "Shift+Tab",
                                              "Previous": "Ctrl+Shift+Tab",

                                              "Settings Window": "S",
                                              "Node Editor Window": "N",
                                              "Node Designer Window": "D",
                                              "Library Window": "L"
                                          }
                                      }

        if os.path.isfile(self.Settings_File):
            # Read data from file
            self.switches_Dict = json.load(open(self.Settings_File))
        else:
            if os.path.exists(self.Settings_Directory) is False:
                os.makedirs(self.Settings_Directory)

            self.switches_Dict = self.Default_switches_Dict

            self.save_settings_to_file()
        self.icons_dict = []
        self.fill_icons_dict()

    def save_settings_to_file(self, data=None, file_path=None):
        """Serializes/Saves Data Into filePath

        :param data :Is The Data Needed To Be Saved
        :param file_path :Full Path Of The File That Data Will Be Saved in
        """
        if data == None and file_path == None:
            data = self.switches_Dict
            file_path = self.Settings_File

        json.dump(data, open(file_path, 'w'))

    def update_font_size(self, size:str = ""):
        if size == "":
            size = self.switches_Dict["Appearance"]["Font Size"]

        s, z = "{font:", "}"
        self.master_ref.setStyleSheet(f"QWidget {s}{size}px{z}")
        if self.master_ref.settingsWidget:
            self.master_ref.settingsWidget.setStyleSheet(f"QWidget {s}{size}px{z}")

    def change_theme(self, theme:str = ""):
        if theme == "":
            theme = self.switches_Dict["Appearance"]["Theme"][0]

        self.master_ref.qss_theme = self.themes[theme]
        self.master_ref.stylesheet_filename = os.path.join(os.path.dirname(__file__), self.master_ref.qss_theme)

        loadStylesheets(
            os.path.join(os.path.dirname(__file__), self.master_ref.qss_theme), self.master_ref.stylesheet_filename)

    def fill_icons_dict(self):
        for icon in os.listdir(f"""vvs_app/icons/{self.switches_Dict["Appearance"]["Theme"][0]}"""):
            self.icons_dict.append(icon)
            pass

    def get_icon(self, icon):
        return f"""vvs_app/icons/{self.switches_Dict["Appearance"]["Theme"][0]}/{icon}"""
