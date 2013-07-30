# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details

'''
Asbtract Syntax Tree
'''


class Module(object):
    def __init__(self, import_list=None, declaration_sequence=None):
        assert import_list is None or isinstance(import_list, list)
        assert (declaration_sequence is None or
                isinstance(declaration_sequence, list))
        self.import_list = import_list
        self.declaration_sequence = declaration_sequence


class TypeDeclaration(object):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype


class Identifier(object):
    def __init__(self, value):
        self.value = value


# TODO: value -> field_list ?
class TypeStruct(object):
    def __init__(self, value):
        self.value = value


class Field(object):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype


class ConstDeclaration(object):
    def __init__(self, name, datatype, expression):
        self.name = name
        self.datatype = datatype
        self.expression = expression


class Number(object):
    def __init__(self, value):
        self.value = value


class String():
    def __init__(self, value):
        self.value = value


class FunctionDeclaration(object):
    def __init__(self, name, interface, body):
        self.name = name
        self.interface = interface
        self.body = body


class FunctionInterface(object):
    def __init__(self, parameter_list, return_type=None):
        self.parameter_list = parameter_list
        self.return_type = return_type


class Parameter(object):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype


class FunctionCall(object):
    def __init__(self, expression, argument_list):
        self.expression = expression
        self.argument_list = argument_list


class VariableDeclaration(object):
    def __init__(
            self,
            name,
            expression=None,
            constructor_argument_list=None,
            datatype=None,
    ):
        self.name = name
        self.expression = expression
        self.constructor_argument_list = constructor_argument_list
        self.datatype = datatype


class If(object):
    def __init__(self, condition, branch_if, branch_else=None):
        self.condition = condition
        self.branch_if = branch_if
        self.branch_else = branch_else


class Return(object):
    def __init__(self, expression=None):
        self.expression = expression


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
