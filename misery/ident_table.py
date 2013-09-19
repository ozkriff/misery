# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


from misery import (
    ast,
    datatype,
)


def ident_table(ast_):
    ''' Build simple ident table. '''

    def standart_funcs():
        datatype_int = datatype.SimpleDataType('Int')
        datatype_string = datatype.SimpleDataType('String')
        ident_list = {}
        std_signature = ast.FuncSignature(
            return_type=datatype.SimpleDataType('Int'),
            par_list=[
                ast.Parameter(name='a', datatype=datatype_int),
                ast.Parameter(name='b', datatype=datatype_int),
            ],
        )
        # Int constructor
        ident_list['Int'] = ast.FuncSignature(
            return_type=datatype_int,
            par_list=[
                ast.Parameter(name='n', datatype=datatype_int),
            ],
        )
        ident_list['printNewLine'] = ast.FuncSignature()
        ident_list['printString'] = ast.FuncSignature(
            par_list=[
                ast.Parameter(name='s', datatype=datatype_string),
            ],
        )
        ident_list['printInt'] = ast.FuncSignature(
            par_list=[
                ast.Parameter(name='n', datatype=datatype_int),
            ],
        )
        ident_list['isEqualInt'] = std_signature
        ident_list['isLessInt'] = std_signature
        ident_list['isGreaterInt'] = std_signature
        ident_list['minusInt'] = std_signature
        ident_list['plusInt'] = std_signature
        ident_list['multiplyInt'] = std_signature
        return ident_list

    ident_list = {}
    for decl in ast_.decl_list:
        if isinstance(decl, ast.FuncDecl):
            ident_list[decl.name] = decl.signature
    for decl in ast_.decl_list:
        if isinstance(decl, ast.StructDecl):
            # create constructor
            ident_list[decl.name] = ast.FuncSignature(
                return_type=datatype.SimpleDataType(decl.name),
            )
    ident_list.update(standart_funcs())
    return ident_list


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
