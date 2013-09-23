# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


from misery import (
    ast,
    datatype,
    misc,
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
        ident_list['print'] = [
            ast.FuncSignature(
                par_list=[
                    ast.Parameter(name='s', datatype=datatype_string),
                ],
            ),
            ast.FuncSignature(
                par_list=[
                    ast.Parameter(name='n', datatype=datatype_int),
                ],
            ),
        ]
        ident_list['isEqual'] = std_signature
        ident_list['isLess'] = std_signature
        ident_list['isGreater'] = std_signature
        ident_list['minus'] = std_signature
        ident_list['plus'] = std_signature
        ident_list['multiply'] = std_signature
        return ident_list

    def create_constructor_func(struct_decl):
        return ast.FuncSignature(
            return_type=datatype.SimpleDataType(struct_decl.name),
        )

    ident_list = {}
    for decl in ast_.decl_list:
        if isinstance(decl, ast.FuncDecl):
            if decl.name in ident_list:
                ident_list[decl.name] = misc.tolist(ident_list[decl.name])
                ident_list[decl.name].append(decl.signature)
            else:
                ident_list[decl.name] = [
                    decl.signature,
                ]
        elif isinstance(decl, ast.StructDecl):
            ident_list[decl.name] = create_constructor_func(decl)
    ident_list.update(standart_funcs())
    return ident_list


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
