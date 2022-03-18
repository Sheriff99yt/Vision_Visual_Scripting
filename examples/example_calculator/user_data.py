class UserData():
    def __init__(self):
        self.userVars = []
        self.userEvents = []
        self.VarEventNames = []

    def AddVar(self, newVarRef: 'Node'):

        # Rename the Variable to an Unoccupied name
        self.autoNodeRename(newVarRef)

        # Give new Var New Object ID
        newVarID = len(self.userVars)

        # Save new Var to list of vars with [Type, ID, Name, Value]
        varData = [newVarRef.name, newVarRef.node_Value, newVarID, newVarRef.node_type]


        self.userVars.append(varData)
        return varData

    def AddEvent(self, newEventRef: 'Node'):

        # Rename the Variable to an Unoccupied name
        self.autoNodeRename(newEventRef)

        # Give new Var New Object ID
        newEventID = len(self.userEvents)

        # Save new Var to list of vars with [Type, ID, Name, Value]
        eventData = [newEventRef.name, newEventRef.node_Value, newEventID, newEventRef.node_type]

        self.userEvents.append(eventData)

        return eventData

    def LoadData(self):
        return self.userVars

    def userRename(self, oldName, tryName: str):
        if self.VarEventNames.__contains__(tryName):
            return None
        else:
            self.VarEventNames.remove(oldName)
            self.VarEventNames.append(tryName)
            return tryName

    def autoNodeRename(self, node: 'Node'):
        x = 0
        newName = node.name
        # does a variable already has this name ?
        while self.VarEventNames.__contains__(newName):
            x += 1
            newName = f"{node.name}{x}"

        else:
            self.VarEventNames.append(newName)
            node.name = newName
