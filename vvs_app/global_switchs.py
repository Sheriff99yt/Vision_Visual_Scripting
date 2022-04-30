class GlobalSwitches():
    def __init__(self):
        # AutoSave
        self.autoSaveSteps = 30
        self.autoSaveCounter = 0

        self.varlist = ["New Graph", "Ctrl+N",
                        "Open", "Ctrl+O",
                        "Set Project Location", "Ctrl+Shift+O",
                        "Save", "Ctrl+S",
                        "Save As", "Ctrl+Shift+S",
                        "Exit", "Ctrl+Q",

                        "Undo", "Ctrl+Z",
                        "Redo", "Ctrl+Shift+Z",
                        "Cut", "Ctrl+X",
                        "Copy", "Ctrl+C",
                        "Paste", "Ctrl+V",
                        "Delete", "Del"]

    def change_autoSaveSteps(self, newValue):
        self.autoSaveSteps = newValue
        self.autoSaveCounter = 0

    def change_Switches(self, newValue, Text):
        self.varlist[self.varlist.index(Text)+1] = newValue
