# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


from misery import (
    ast,
    datatype,
)


def identifier_table(ast_):
    ''' Build simple identifier table. '''

    def standart_functions():
        datatype_int = datatype.SimpleDataType('Int')
        datatype_string = datatype.SimpleDataType('String')
        identifier_list = {}
        std_signature = ast.FunctionSignature(
            return_type=datatype.SimpleDataType('Int'),
            parameter_list=[
                ast.Parameter(name='a', datatype=datatype_int),
                ast.Parameter(name='b', datatype=datatype_int),
            ],
        )
        identifier_list['printString'] = ast.FunctionSignature(
            parameter_list=[
                ast.Parameter(name='s', datatype=datatype_string),
            ],
        )
        identifier_list['printInt'] = ast.FunctionSignature(
            parameter_list=[
                ast.Parameter(name='n', datatype=datatype_int),
            ],
        )
        identifier_list['isEqualInt'] = std_signature
        identifier_list['isLessInt'] = std_signature
        identifier_list['isGreaterInt'] = std_signature
        identifier_list['minusInt'] = std_signature
        identifier_list['plusInt'] = std_signature
        identifier_list['multiplyInt'] = std_signature
        return identifier_list

    identifier_list = {}
    for declaration in ast_.declaration_sequence:
        if isinstance(declaration, ast.FunctionDeclaration):
            identifier_list[declaration.name] = declaration.signature
    for declaration in ast_.declaration_sequence:
        if isinstance(declaration, ast.StructDeclaration):
            # create constructor
            identifier_list[declaration.name] = ast.FunctionSignature(
                return_type=datatype.SimpleDataType(declaration.name),
                parameter_list=[],
            )
    identifier_list.update(standart_functions())
    return identifier_list


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
