LISTBOX_MIMETYPE = "application/x-item"

FUN_EVENT = 0
FUN_IF = 1
FUN_FOR_LOOP = 2
FUN_PRINT = 3
FUN_Equal = 4
FUN_GREATER_THAN = 5
FUN_LESS_THAN = 6
FUN_AND = 7
FUN_ADD = 8
FUN_SUB = 9
FUN_MUL = 10
FUN_DIV = 11
FUN_INPUT = 12
FUN_OUTPUT = 13

######################

VAR_FLOAT = 20
VAR_INTEGER = 21
VAR_BOOLEAN = 22
VAR_STRING = 23

######################

FUNCTIONS = {}
VARIABLES = {}

######################

USERVARS = {}
USEREVENTS = {}

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
            "Duplicate Variable registration of '%s'. There is already %s" % (var_ID, USERVARS[var_ID]))
    else:
        USERVARS[var_ID] = class_reference

def get_var_by_ID(var_ID):
    if var_ID not in USERVARS:
        raise OpCodeNotRegistered("node_type '%d' is not registered" % var_ID)
    else:
        return USERVARS[var_ID]

######################

# User Events setup

def set_user_event_ID_now(event_ID, class_reference):
    if event_ID in USEREVENTS:
        raise InvalidNodeRegistration(
            "Duplicate Event registration of '%s'. There is already %s" % (event_ID, USEREVENTS[event_ID]))
    else:
        USEREVENTS[event_ID] = class_reference


def get_event_by_ID(event_ID):
    if event_ID not in USEREVENTS:
        raise OpCodeNotRegistered("Event '%d' is not registered" % event_ID)
    else:
        return USEREVENTS[event_ID]

######################



# This comment was originally here before it was removed for better init performance and moved
    # import all nodes and register them
    # from examples.example_calculator.nodes import *
