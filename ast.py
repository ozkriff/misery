# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details

'''
Asbtract Syntax Tree
'''


import datatype


class Module(object):
    def __init__(self, import_list=None, declaration_sequence=None):
        assert import_list is None or isinstance(import_list, list)
        assert (declaration_sequence is None or
                isinstance(declaration_sequence, list))
        self.import_list = import_list
        self.declaration_sequence = declaration_sequence


class Identifier(object):
    def __init__(self, name):
        self.name = name


class QualifiedIdentifier(object):
    def __init__(self, identifier_list):
        self.identifier_list = identifier_list


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


class String(object):
    def __init__(self, value):
        self.value = value


class FunctionDeclaration(object):
    def __init__(self, name, interface, body):
        self.name = name
        self.interface = interface
        self.body = body
        self.vars = {}  # TODO: move to ast.Block


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
        self.expression = expression  # TODO: rename - called_expression?
        self.argument_list = argument_list
        self.tmp_var = None  # TODO: rename? - binded_variable_name


class VariableDeclaration(object):
    def __init__(
        self,
        name,
        expression=None,
        datatype=None,
    ):
        self.name = name
        self.expression = expression  # TODO: rename
        self.datatype = datatype


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


def identifier_table(ast_):
    ''' Build simple identifier table. '''

    def standart_functions():
        identifier_list = {}
        std_interface = FunctionInterface(
            return_type=datatype.SimpleDataType('Int'),
            parameter_list=[
                Parameter(
                    name='a',
                    datatype=datatype.SimpleDataType('Int'),
                ),
                Parameter(
                    name='b',
                    datatype=datatype.SimpleDataType('Int'),
                ),
            ],
        )
        identifier_list['printString'] = FunctionInterface(
            parameter_list=[
                Parameter(
                    name='s',
                    datatype=datatype.SimpleDataType('String'),
                ),
            ],
        )
        identifier_list['printInteger'] = FunctionInterface(
            parameter_list=[
                Parameter(
                    name='n',
                    datatype=datatype.SimpleDataType('Int'),
                ),
            ],
        )
        identifier_list['isEqualInteger'] = std_interface
        identifier_list['isLessInteger'] = std_interface
        identifier_list['isGreaterInteger'] = std_interface
        identifier_list['minusInteger'] = std_interface
        identifier_list['plusInteger'] = std_interface
        identifier_list['multiplyInteger'] = std_interface
        return identifier_list

    identifier_list = {}
    for declaration in ast_.declaration_sequence:
        if isinstance(declaration, FunctionDeclaration):
            identifier_list[declaration.name] = declaration.interface
    for declaration in ast_.declaration_sequence:
        if isinstance(declaration, StructDeclaration):
            # create constructor
            identifier_list[declaration.name] = FunctionInterface(
                return_type=datatype.SimpleDataType(declaration.name),
                parameter_list=[],
            )
    identifier_list.update(standart_functions())
    return identifier_list


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
