
class UserData():
    def __init__(self):
        self.userVars = []


    def SaveVar(self, var: 'Node'):
        # store Name, Type and Value in a Dic
        self.userVars.append([var.name, var.node_ID, var.outputs[0].socketValue])


    def LoadData(self):
        return self.userVars
