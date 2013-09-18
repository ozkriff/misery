# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


'''
Data types.
'''


import copy
from misery import (
    ast,
)


class SimpleDataType(object):
    def __init__(self, name):
        self.name = name


def _mark_out_datatypes(ast_):
    ''' Mark out 'datatype' fields to ast nodes. '''

    def get_func_call_expr_datatype(func_call_expr):
        func_name = func_call_expr.called_expr.name
        if func_name not in ast_.ident_list:
            raise Exception('no func: \'' + func_name + '\'')
        return ast_.ident_list[func_name].return_type

    def get_expr_datatype(expr):
        if isinstance(expr, ast.Number):
            return SimpleDataType('Int')
        if isinstance(expr, ast.String):
            return SimpleDataType('String')
        elif isinstance(expr, ast.FuncCall):
            return get_func_call_expr_datatype(expr)
        else:
            raise Exception('Bad type: ' + str(type(expr)))

    def mark_out_var_decl_stmt(
        var_decl_stmt,
    ):
        datatype = get_expr_datatype(
            var_decl_stmt.rvalue_expr,
        )
        var_decl_stmt.datatype = datatype

    def mark_out_assign_stmt(assign_stmt):
        datatype = get_expr_datatype(assign_stmt.rvalue_expr)
        assign_stmt.datatype = datatype

    def mark_out_stmt(stmt):
        ''' stmt - current parsed stmt in current parsed block
        '''
        ignored_stmt_type_tuple = (
            ast.FuncCall,
            ast.Return,
            ast.If,
            ast.For,
        )
        if isinstance(stmt, ast.VarDecl):
            mark_out_var_decl_stmt(stmt)
        elif isinstance(stmt, ast.Assign):
            mark_out_assign_stmt(stmt)
        elif isinstance(stmt, ignored_stmt_type_tuple):
            pass  # do nothing for this stmts
        else:
            raise Exception('Bad type: ' + str(type(stmt)))

    def mark_out_func_decl(func_decl):
        block = func_decl.body
        for stmt in block:
            mark_out_stmt(stmt)

    for decl in ast_.decl_list:
        if isinstance(decl, ast.FuncDecl):
            mark_out_func_decl(decl)
        elif isinstance(decl, ast.StructDecl):
            pass
        else:
            raise Exception('Bad type: ' + str(type(decl)))


def mark_out_datatypes(ast_):
    ''' Mark out 'datatype' fields to ast nodes. '''
    copied_ast_ = copy.deepcopy(ast_)
    _mark_out_datatypes(copied_ast_)
    return copied_ast_


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
