from examples.example_calculator.nodes_configuration import USERVARS


class UserData():
    def __init__(self):
        self.userVars = []
        self.varNames = []

    def AddVar(self, newVarRef: 'Node'):

        # Rename the Variable to an Unoccupied name
        self.autoVarRename(newVarRef)

        # Give new Var New Object ID
        newVarID = len(self.userVars)

        newVarRef.node_type = newVarID

        # Save new Var to list of vars with [Type, ID, Name, Value]
        varData = [newVarRef.name, newVarRef.node_value, newVarID]

        self.userVars.append(varData)

        return varData

    def LoadData(self):
        return self.userVars

    def autoVarRename(self, var: 'Node'):
        x = 0
        newName = var.name
        # does a variable already has this name ?
        while self.varNames.__contains__(newName):
            x += 1
            newName = f"{var.name}{x}"

        else:
            self.varNames.append(newName)
            var.name = newName
