import json
import os

class GlobalSwitches():
    def __init__(self):
        self.MasterRef = None
        self.Settings_Directory = f"C:/Users/{os.getlogin()}/Documents/VVS"
        self.Settings_File = self.Settings_Directory + f"/Settings.json"

        self.Default_switches_Dict = {"autoSaveSteps": 30,
                                      "AutoSave Folder Max Size": 5,

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

        if os.path.isfile(self.Settings_File):
            # Read data from file
            self.switches_Dict = json.load(open(self.Settings_File))
        else:
            if os.path.exists(self.Settings_Directory) is False:
                os.makedirs(self.Settings_Directory)

            self.switches_Dict = self.Default_switches_Dict

            print(self.switches_Dict)

            self.saveSettingsToFile(self.switches_Dict, self.Settings_File)

    def change_Switches(self, newValue, resetList:list, CounterReset):
        """Changes The Values Of The Switches in the GlobalSwitches.switches_Dict

        - Note: The Function Also Resets The Current Graph's Edits_Counter depending on the Value of CounterReset

        - Note: The Function Also Resets Given List Of settings to Default Value if newValue is a Dict

        :param newValue: The New Value if a single Value and a Collection of Values in a Dict if a Dict is Given
        :param resetList: The Index Of the Value That Will Change
        :param CounterReset: Determines whether to Reset The Edits_Counter Of The Current Graph or not
        """
        if resetList:
            for i in resetList:
                self.switches_Dict[i] = newValue[i] if type(newValue) is dict else newValue

        self.saveSettingsToFile(self.switches_Dict, self.Settings_File)
        self.MasterRef.settingsWidget.currentSettingsWidget.fill()

        CurrentNodeEditor = self.MasterRef.CurrentNodeEditor()
        if CounterReset is True and CurrentNodeEditor is not None:
            CurrentNodeEditor.scene.history.Edits_Counter = 0


    def saveSettingsToFile(self, Data, filePath):
        """Serializes/Saves Data Into filePath

        :param Data :Is The Data Needed To Be Saved
        :param filePath :Full Path Of The File That Data Will Be Saved in
        """
        json.dump(Data, open(filePath, 'w'))
