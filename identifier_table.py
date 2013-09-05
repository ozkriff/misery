# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import ast
import datatype


def identifier_table(ast_):
    ''' Build simple identifier table. '''

    def standart_functions():
        datatype_int = datatype.SimpleDataType('Int')
        datatype_string = datatype.SimpleDataType('String')
        identifier_list = {}
        std_interface = ast.FunctionInterface(
            return_type=datatype.SimpleDataType('Int'),
            parameter_list=[
                ast.Parameter(name='a', datatype=datatype_int),
                ast.Parameter(name='b', datatype=datatype_int),
            ],
        )
        identifier_list['printString'] = ast.FunctionInterface(
            parameter_list=[
                ast.Parameter(name='s', datatype=datatype_string),
            ],
        )
        identifier_list['printInt'] = ast.FunctionInterface(
            parameter_list=[
                ast.Parameter(name='n', datatype=datatype_int),
            ],
        )
        identifier_list['isEqualInt'] = std_interface
        identifier_list['isLessInt'] = std_interface
        identifier_list['isGreaterInt'] = std_interface
        identifier_list['minusInt'] = std_interface
        identifier_list['plusInt'] = std_interface
        identifier_list['multiplyInt'] = std_interface
        return identifier_list

    identifier_list = {}
    for declaration in ast_.declaration_sequence:
        if isinstance(declaration, ast.FunctionDeclaration):
            identifier_list[declaration.name] = declaration.interface
    for declaration in ast_.declaration_sequence:
        if isinstance(declaration, ast.StructDeclaration):
            # create constructor
            identifier_list[declaration.name] = ast.FunctionInterface(
                return_type=datatype.SimpleDataType(declaration.name),
                parameter_list=[],
            )
    identifier_list.update(standart_functions())
    return identifier_list


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
