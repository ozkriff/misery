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
        std_signature = ast.FuncSignature(
            return_type=datatype.SimpleDataType('Int'),
            par_list=[
                ast.Parameter(name='a', datatype=datatype_int),
                ast.Parameter(name='b', datatype=datatype_int),
            ],
        )
        ident_list = {
            # Int constructor
            'Int': ast.FuncSignature(
                return_type=datatype_int,
                par_list=[
                    ast.Parameter(name='n', datatype=datatype_int),
                ],
            ),
            'printNewLine': ast.FuncSignature(),
            'print': [
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
            ],
            'isEqual': std_signature,
            'isLess': std_signature,
            'isGreater': std_signature,
            'minus': std_signature,
            'plus': std_signature,
            'multiply': std_signature,
        }
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
