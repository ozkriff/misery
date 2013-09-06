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
        self.identifier_list = None


class Identifier(object):
    def __init__(self, name):
        self.name = name


class Field(object):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype


class ConstDeclaration(object):
    def __init__(self, name, datatype, expression):
        self.name = name
        self.datatype = datatype
        self.expression = expression


class StructDeclaration(object):
    def __init__(self, name, field_list):
        self.name = name
        self.field_list = field_list


class Number(object):
    def __init__(self, value):
        self.value = value
        self.binded_variable_name = None


class String(object):
    def __init__(self, value):
        self.value = value
        self.binded_variable_name = None


class FunctionDeclaration(object):
    def __init__(self, name, signature, body):
        self.name = name
        self.signature = signature
        self.body = body
        # TODO: move to ast.Block ...
        self.vars = {}
        self.tmp_vars = {}
        self.constants = {}


class FunctionSignature(object):
    def __init__(self, parameter_list, return_type=None):
        self.parameter_list = parameter_list
        self.return_type = return_type


class Parameter(object):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype


class FunctionCall(object):
    def __init__(self, expression, argument_list):
        self.expression = expression  # TODO: rename - called_expression?
        self.argument_list = argument_list
        self.binded_variable_name = None


class VariableDeclaration(object):
    def __init__(
        self,
        name,
        expression=None,
        datatype=None,
        allocate_memory_on_stack=False,
    ):
        self.name = name
        self.expression = expression  # TODO: rename
        self.datatype = datatype
        self.allocate_memory_on_stack = allocate_memory_on_stack


class Assign(object):
    def __init__(
        self,
        name,
        expression=None,
        datatype=None,
    ):
        self.name = name
        self.expression = expression
        self.datatype = datatype


class If(object):
    def __init__(self, condition, branch_if, branch_else=None):
        self.condition = condition
        self.branch_if = branch_if
        self.branch_else = branch_else


class For(object):
    def __init__(self, condition, branch):
        self.condition = condition
        self.branch = branch


class Return(object):
    def __init__(self, expression=None):
        self.expression = expression


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
