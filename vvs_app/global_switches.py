import json
import os


class GlobalSwitches:
    def __init__(self, master):
        self.master_ref = master
        self.Settings_Directory = f"{self.master_ref.files_widget.default_system_dir}/Preferences"
        self.Settings_File = self.Settings_Directory + f"/Settings.json"

        self.Default_switches_Dict = {"AutoSave Steps": 30,
                                      "AutoSave Folder MaxSize": 500,
                                      "Always Save Before Closing": True,
                                      "Save Unsaved Files to Project Folder": False,

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

