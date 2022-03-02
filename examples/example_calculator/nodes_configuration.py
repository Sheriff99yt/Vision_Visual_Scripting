LISTBOX_MIMETYPE = "application/x-item"

FUN_INPUT = 1
FUN_OUTPUT = 2
FUN_ADD = 3
FUN_SUB = 4
FUN_MUL = 5
FUN_DIV = 6
FUN_IF = 7
FUN_FOR_LOOP = 8
FUN_EXECUTION_EVENT = 9
FUN_PRINT = 10
FUN_EVENT = 11

####################

VAR_FLOAT = 12
VAR_INTEGER = 13
VAR_BOOLEAN = 14
VAR_STRING = 15

######################

FUNCTIONS = {}
VARIABLES = {}


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class OpCodeNotRegistered(ConfException):
    pass


# Functions

def register_node_now(node_ID, class_reference, Fun):
    if Fun is True:
        if node_ID in FUNCTIONS:
            raise InvalidNodeRegistration(
                "Duplicate node registration of '%s'. There is already %s" % (node_ID, FUNCTIONS[node_ID]))
        else:
            FUNCTIONS[node_ID] = class_reference
    else:
        if node_ID in VARIABLES:
            raise InvalidNodeRegistration(
                "Duplicate node registration of '%s'. There is already %s" % (node_ID, VARIABLES[node_ID]))
        else:
            VARIABLES[node_ID] = class_reference


def register_node(node_ID, Fun=True):
    def decorator(original_class):
        register_node_now(node_ID, original_class, Fun)
        return original_class

    return decorator


def get_class_from_nodesID(node_ID):
    NODES = {**FUNCTIONS, **VARIABLES}
    if node_ID not in NODES:
        raise OpCodeNotRegistered("node_ID '%d' is not registered" % node_ID)
    else:
        return NODES[node_ID]


# import all nodes and register them
from examples.example_calculator.nodes import *
