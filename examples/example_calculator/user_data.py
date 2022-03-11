from examples.example_calculator.nodes_configuration import USERVARS


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

        newVarRef.node_type = newVarID

        # Save new Var to list of vars with [Type, ID, Name, Value]
        varData = [newVarRef.name, newVarRef.node_value, newVarID]

        self.userVars.append(varData)

        return varData

    def AddEvent(self, newEventRef: 'Node'):

        # Rename the Variable to an Unoccupied name
        self.autoNodeRename(newEventRef)

        # Give new Var New Object ID
        newEventID = len(self.userEvents)

        newEventRef.node_type = newEventID

        # Save new Var to list of vars with [Type, ID, Name, Value]
        eventData = [newEventRef.name, newEventRef.node_value, newEventID]

        self.userEvents.append(eventData)

        return eventData

    def LoadData(self):
        return self.userVars

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
