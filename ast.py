# -*- coding: utf-8 -*-

"""
Asbtract Syntax Tree
"""


class BaseNode(object):

    def __eq__(self, other):
        if isinstance(other, BaseNode):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self == other


class NodeModule(BaseNode):
    def __init__(self, import_list=None, declaration_sequence=None):
        assert import_list is None or isinstance(import_list, list)
        assert (declaration_sequence is None or
                isinstance(declaration_sequence, list))
        self.import_list = import_list
        self.declaration_sequence = declaration_sequence


class NodeTypeDeclaration(BaseNode):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class NodeIdentifier(BaseNode):
    def __init__(self, value):
        self.value = value


# TODO: value -> field_list ?
class NodeTypeStruct(BaseNode):
    def __init__(self, value):
        self.value = value


class NodeField(BaseNode):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class NodeConstDeclaration(BaseNode):
    def __init__(self, name, type, expression):
        self.name = name
        self.type = type
        self.expression = expression


class NodeNumber(BaseNode):
    def __init__(self, value):
        self.value = value


class NodeString(BaseNode):
    def __init__(self, value):
        self.value = value


class NodeFunctionDeclaration(BaseNode):
    def __init__(self, name, interface, body):
        self.name = name
        self.interface = interface
        self.body = body


class NodeFunctionInterface(BaseNode):
    def __init__(self, parameter_list=[], return_type=None):
        self.parameter_list = parameter_list
        self.return_type = return_type


class NodeFormalParameter(BaseNode):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class NodeFunctionCall(BaseNode):
    def __init__(self, expression, argument_list=[]):
        self.expression = expression
        self.argument_list = argument_list


class NodeVariableDeclaration(BaseNode):
    def __init__(
            self,
            name,
            type=None,
            expression=None,
            constructor_argument_list=None):
        self.name = name
        self.type = type
        self.expression = expression
        self.constructor_argument_list = constructor_argument_list


class NodeIf(BaseNode):
    def __init__(self, condition, branch_if, branch_else=None):
        self.condition = condition
        self.branch_if = branch_if
        self.branch_else = branch_else


class NodeReturn(BaseNode):
    def __init__(self, expression=None):
        self.expression = expression

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
