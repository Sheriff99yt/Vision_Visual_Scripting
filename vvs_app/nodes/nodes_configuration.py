LISTBOX_MIMETYPE = "application/x-item"

# FUN_INPUT = "NOT IMPLEMENTED"
# FUN_OUTPUT = "NOT IMPLEMENTED"

# class NodeType:
#     def __init__(self, value, category, sub_category):
#         self.value = value
#         self.category = category
#         self.sub_category = sub_category
#
# Functions = "Functions"
#
# Qustions = "Qustions"
# FUN_IF = NodeType(1, Functions, Qustions)
# FUN_GREATER_THAN = NodeType(5, Functions, Qustions)
# FUN_LESS_THAN = NodeType(6, Functions, Qustions)
# FUN_Equal = NodeType(4, Functions, Qustions)
#
# Outputers = "Outputers"
# FUN_PRINT = NodeType(4, Functions, Outputers)
#
# Iterators = "Iterators"
# FUN_FOR_EACH_LOOP = NodeType(16, Functions, Iterators)
# FUN_FOR_LOOP = NodeType(2, Functions, Iterators)
# FUN_WHILE_LOOP = NotImplemented
#
# Logic = "Logic"
# FUN_AND = NodeType(7, Functions, Logic)
# FUN_OR = NotImplemented
#
# UserInput = "UserInput"
# FUN_RAW_CODE = NodeType(13, UserInput, None)
# FUN_USER_INPUT = NodeType(12, UserInput, None)
#
# MathOperations = "MathOperations"
# FUN_ADD = NodeType(8, MathOperations, None)
# FUN_SUB = NodeType(9, MathOperations, None)
# FUN_MUL = NodeType(10, MathOperations, None)
# FUN_DIV = NodeType(11, MathOperations, None)
#
# ######################
#
# Events = "Events"
# EVENT = NodeType(0, Events, None)
#
# Variables = "Variables"
# VAR_FLOAT = NodeType(20, Variables, None)
# VAR_INTEGER = NodeType(21, Variables, None)
# VAR_BOOLEAN = NodeType(22, Variables, None)
# VAR_STRING = NodeType(23, Variables, None)
# VAR_LIST = NodeType(24, Variables, None)

FUN_IF = 1
FUN_Equal = 4
FUN_GREATER_THAN = 5
FUN_LESS_THAN = 6
FUN_AND = 7
FUN_FOR_LOOP = 2
FUN_FOR_EACH_LOOP = 16

FUN_ADD = 8
FUN_SUB = 9
FUN_MUL = 10
FUN_DIV = 11

FUN_RAW_CODE = 13
FUN_PRINT = 3
FUN_USER_INPUT = 12
FUN_INPUT = NotImplemented
FUN_OUTPUT = NotImplemented

######################
EVENT = 0

VAR_FLOAT = 20
VAR_INTEGER = 21
VAR_BOOLEAN = 22
VAR_STRING = 23
VAR_LIST = 24

######################

Logic = []
Math = []
Process = []

FUN_LIST = [FUN_IF, FUN_Equal, FUN_GREATER_THAN, FUN_LESS_THAN, FUN_AND, FUN_FOR_LOOP, FUN_FOR_EACH_LOOP, FUN_ADD, FUN_SUB,
     FUN_MUL, FUN_DIV, FUN_RAW_CODE, FUN_PRINT, FUN_USER_INPUT, FUN_INPUT, FUN_OUTPUT, EVENT, VAR_FLOAT, VAR_INTEGER,
     VAR_BOOLEAN, VAR_STRING, VAR_LIST]

FUNCTIONS = {}
VARIABLES = {}
EVENTS = {}

######################


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
    print(FUNCTIONS)
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
