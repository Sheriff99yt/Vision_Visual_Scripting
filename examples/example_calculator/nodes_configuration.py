LISTBOX_MIMETYPE = "application/x-item"

FUN_INPUT = 25
FUN_OUTPUT = 26
FUN_ADD = 20
FUN_SUB = 21
FUN_MUL = 23
FUN_DIV = 24
FUN_IF = 2
FUN_FOR_LOOP = 3
FUN_PRINT = 4
FUN_EVENT = 1
FUN_GREATER_THAN = 17
FUN_LESS_THAN = 18
FUN_Equal = 16
FUN_AND = 19
######################

VAR_FLOAT = 12
VAR_INTEGER = 13
VAR_BOOLEAN = 14
VAR_STRING = 15

######################

FUNCTIONS = {}
VARIABLES = {}
######################

USERVARS = {}

######################


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class InvalidUserVarRegistration(ConfException):
    pass


class OpCodeNotRegistered(ConfException):
    pass


######################
# Nodes setup

def set_node_ID(node_type, Fun=True):
    def decorator(original_class):
        set_node_ID_now(node_type, original_class, Fun)
        return original_class
    return decorator

def set_node_ID_now(node_type, class_reference, Fun):
    if Fun is True:
        if node_type in FUNCTIONS:
            raise InvalidNodeRegistration(
                "Duplicate node registration of '%s'. There is already %s" % (node_type, FUNCTIONS[node_type]))
        else:
            class_reference.isFun = Fun
            FUNCTIONS[node_type] = class_reference

    else:
        if node_type in VARIABLES:
            raise InvalidNodeRegistration(
                "Duplicate node registration of '%s'. There is already %s" % (node_type, VARIABLES[node_type]))
        else:
            class_reference.isFun = Fun
            VARIABLES[node_type] = class_reference

def get_node_by_ID(node_type):
    NODES = {**FUNCTIONS, **VARIABLES}
    if node_type not in NODES:
        raise OpCodeNotRegistered("node_type '%d' is not registered" % node_type)
    else:
        return NODES[node_type]

######################

# User Variables setup


def set_user_var_ID_now(var_ID, class_reference):
    if var_ID in USERVARS:
        raise InvalidNodeRegistration(
            "Duplicate node registration of '%s'. There is already %s" % (var_ID, USERVARS[var_ID]))
    else:
        USERVARS[var_ID] = class_reference

def get_var_by_ID(var_ID):
    if var_ID not in USERVARS:
        raise OpCodeNotRegistered("node_type '%d' is not registered" % var_ID)
    else:
        return USERVARS[var_ID]

######################



# This comment was originally here before it was removed for better init performance and moved
    # import all nodes and register them
    # from examples.example_calculator.nodes import *
