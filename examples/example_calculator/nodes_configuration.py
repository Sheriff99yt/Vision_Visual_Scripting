LISTBOX_MIMETYPE = "application/x-item"

FUN_EVENT = 0
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

####################

VAR_FLOAT = 11
VAR_INTEGER = 12
VAR_BOOLEAN = 13
VAR_STRING = 14

######################

FUNCTIONS = {}
VARIABLES = {}


class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass

# Functions

def register_node_now(node_ID, class_reference):
    if node_ID in FUNCTIONS or node_ID in VARIABLES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" % (node_ID, FUNCTIONS[node_ID]))

    elif node_ID in FUNCTIONS: VARIABLES[node_ID] = class_reference
    else: FUNCTIONS[node_ID] = class_reference


def register_node(node_ID):
    def decorator(original_class):
        register_node_now(node_ID, original_class)
        return original_class
    return decorator

def get_class_from_nodesID(node_ID):
    NODES = {**FUNCTIONS, **VARIABLES}
    if node_ID not in NODES:
        raise OpCodeNotRegistered("OpCode '%d' is not registered" % node_ID)
    return NODES[node_ID]




# Variables
# import all nodes and register them
from examples.example_calculator.nodes import *