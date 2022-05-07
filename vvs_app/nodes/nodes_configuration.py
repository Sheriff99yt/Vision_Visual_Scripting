LISTBOX_MIMETYPE = "application/x-item"

EVENT = 0
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
FUN_USER_INPUT = 12
FUN_RAW_CODE = 13
FUN_INPUT = 14
FUN_OUTPUT = 15
FUN_FOR_EACH_LOOP = 16
######################

VAR_FLOAT = 20
VAR_INTEGER = 21
VAR_BOOLEAN = 22
VAR_STRING = 23
VAR_LIST = 24

######################

FUNCTIONS = {}
MATH_OPERATORS = {}
LOGIC_OPERATORS = {}
NUMPY = {}

######################

VARIABLES = {}
EVENTS = {}

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


def get_node_by_type(node_type):
    NODES = {**FUNCTIONS, **VARIABLES, **EVENTS}
    if node_type not in NODES:
        raise NodeTypeNotRegistered("node_type '%d' is not registered" % node_type)
    else:
        return NODES[node_type]

######################


##############################################################################################################
##############################################################################################################

# User Variables setup


######################

# User Events setup


##############################################################################################################
##############################################################################################################


# This comment was originally here before it was removed for better init performance and moved
# import all nodes and register them
# from vvs_app.nodes import *
