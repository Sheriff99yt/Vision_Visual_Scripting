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
            class_reference.isFun = Fun
            FUNCTIONS[node_ID] = class_reference

    else:
        if node_ID in VARIABLES:
            raise InvalidNodeRegistration(
                "Duplicate node registration of '%s'. There is already %s" % (node_ID, VARIABLES[node_ID]))
        else:
            class_reference.isFun = Fun
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
