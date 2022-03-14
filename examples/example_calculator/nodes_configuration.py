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
EVENTS = {}

######################

USERVARS = {}
USEREVENTS = {}

######################


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class NodeTypeNotRegistered(ConfException):
    pass


######################
# Nodes setup

def set_function_ID(node_type):
    def decorator(original_class):
        set_function_ID_now(node_type, original_class)
        return original_class

    return decorator


def set_var_ID(node_type):
    def decorator(original_class):
        set_var_ID_now(node_type, original_class)
        return original_class

    return decorator


def set_event_ID(node_type):
    def decorator(original_class):
        set_event_ID_now(node_type, original_class)
        return original_class

    return decorator


def set_function_ID_now(node_type, class_reference):
    if node_type in FUNCTIONS:
        raise InvalidNodeRegistration(
            "Duplicate node registration of '%s'. There is already %s" % (node_type, FUNCTIONS[node_type]))
    else:
        FUNCTIONS[node_type] = class_reference


def set_var_ID_now(node_type, class_reference):
    if node_type in VARIABLES:
        raise InvalidNodeRegistration(
            "Duplicate node registration of '%s'. There is already %s" % (node_type, VARIABLES[node_type]))
    else:
        VARIABLES[node_type] = class_reference


def set_event_ID_now(node_type, class_reference):
    if node_type in EVENTS:
        raise InvalidNodeRegistration(
            "Duplicate node registration of '%s'. There is already %s" % (node_type, EVENTS[node_type]))
    else:
        EVENTS[node_type] = class_reference


def get_node_by_ID(node_type):
    NODES = {**FUNCTIONS, **VARIABLES, **EVENTS}
    if node_type not in NODES:
        raise NodeTypeNotRegistered("node_type '%d' is not registered" % node_type)
    else:
        return NODES[node_type]


######################


##############################################################################################################
##############################################################################################################

# User Variables setup


def set_user_var_ID_now(var_ID, class_reference):
    if var_ID in USERVARS:
        raise InvalidNodeRegistration(
            "Duplicate Variable registration of '%s'. There is already %s" % (var_ID, USERVARS[var_ID]))
    else:
        USERVARS[var_ID] = class_reference


def get_user_var_by_ID(var_ID):
    if var_ID not in USERVARS:
        raise NodeTypeNotRegistered("node_type '%d' is not registered" % var_ID)
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


def get_user_event_by_ID(event_ID):
    if event_ID not in USEREVENTS:
        raise NodeTypeNotRegistered("Event '%d' is not registered" % event_ID)
    else:
        return USEREVENTS[event_ID]

##############################################################################################################
##############################################################################################################


# This comment was originally here before it was removed for better init performance and moved
# import all nodes and register them
# from examples.example_calculator.nodes import *
