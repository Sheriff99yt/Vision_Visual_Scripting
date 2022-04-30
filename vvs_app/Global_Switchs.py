import json
import os

class GlobalSwitches():
    def __init__(self):

        self.Settings_Directory = f"C:/Users/{os.getlogin()}/Documents/VVS"
        self.Settings_File = self.Settings_Directory + f"/Settings.json"

        if os.path.isfile(self.Settings_File):
            # Read data from file
            self.switches_List = json.load(open(self.Settings_File))
        else:
            if os.path.exists(self.Settings_Directory) is False:
                os.makedirs(self.Settings_Directory)

            self.switches_List = {"autoSaveSteps": 30,
                            "autoSaveCounter": 0,
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

                                  "Settings Window": "Ctrl+Shift+S"}
            self.saveSettingsToFile(self.switches_List, self.Settings_File)

    def change_Switches(self, newValue, Text):
        self.switches_List[Text] = newValue
        self.saveSettingsToFile(self.switches_List, self.Settings_File)

    def saveSettingsToFile(self, Data, filePath):
        # Serialize data into file
        json.dump(Data, open(filePath, 'w'))