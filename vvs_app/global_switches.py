import json
import os


class GlobalSwitches:
    def __init__(self):
        self.MasterRef = None
        self.Settings_Directory = f"C:/Users/{os.getlogin()}/Documents/VVS"
        self.Settings_File = self.Settings_Directory + f"/Settings.json"

        self.Default_switches_Dict = {"AutoSave Trigger": 30,
                                      "AutoSave Folder MaxSize": 5.0,

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

            self.save_settings_to_file(self.switches_Dict, self.Settings_File)

    # def change_switches(self, new_value, reset_list:list, counter_reset):
    #     """Changes The Values Of The Switches in the GlobalSwitches.switches_Dict
    #
    #     - Note: The Function Also Resets The Current Graph's Edits_Counter depending on the Value of CounterReset
    #
    #     - Note: The Function Also Resets Given List Of settings to Default Value if newValue is a Dict
    #
    #     :param new_value: The New Value if a single Value and a Collection of Values in a Dict if a Dict is Given
    #     :param reset_list: The Index Of the Value That Will Change
    #     :param counter_reset: Determines whether to Reset The Edits_Counter Of The Current Graph or not
    #     """
    #     if reset_list:
    #         for i in reset_list:
    #             self.switches_Dict[i] = new_value[i] if type(new_value) is dict else new_value
    #
    #             self.MasterRef.settingsWidget.fill(self.MasterRef.settingsWidget.settingsTree.currentItem().data(5, 6))
    #
    #             if reset_list == self.MasterRef.settingsWidget.Key_Mapping_settings_list:
    #                 self.MasterRef.settingsWidget.shortcutEdit(self.MasterRef.actions_list[i], i)
    #
    #     self.save_settings_to_file(self.switches_Dict, self.Settings_File)
    #     current_node_editor = self.MasterRef.CurrentNodeEditor()
    #     if counter_reset is True and current_node_editor is not None:
    #         current_node_editor.scene.history.Edits_Counter = 0
    def save_settings_to_file(self, data, file_path):
        """Serializes/Saves Data Into filePath

        :param data :Is The Data Needed To Be Saved
        :param file_path :Full Path Of The File That Data Will Be Saved in
        """
        json.dump(data, open(file_path, 'w'))

