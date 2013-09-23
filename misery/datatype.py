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


# TODO: split statement processing phases
def _mark_out_datatypes(ast_):
    ''' Mark out 'datatype' fields to ast nodes. '''

    def scan_stmt_vars(ast_, func_decl, stmt):

        def scan_expr_vars(func_decl, expr):
            fd = func_decl  # shortcut
            if isinstance(expr, ast.FuncCall):
                for argument in expr.arg_list:
                    scan_expr_vars(fd, argument)
                assert isinstance(expr.called_expr, ast.Ident)
                called_func_name = expr.called_expr.name
                ident_list = ast_.ident_list
                return_type = ident_list[called_func_name].return_type
                if return_type is not None:
                    var_name = 'tmp_' + str(len(fd.tmp_vars))
                    fd.tmp_vars[var_name] = return_type
                    expr.binded_var_name = var_name
            elif isinstance(expr, ast.Number):
                var_name = 'const_' + str(len(fd.constants))
                fd.constants[var_name] = copy.deepcopy(expr)
                expr.binded_var_name = var_name
            elif isinstance(expr, ast.String):
                var_name = 'const_' + str(len(fd.constants))
                fd.constants[var_name] = copy.deepcopy(expr)
                expr.binded_var_name = var_name
            elif isinstance(expr, ast.Ident):
                pass  # ok
            else:
                raise Exception('Bad expr type: ' + str(type(expr)))

        fd = func_decl  # shortcut
        if isinstance(stmt, ast.FuncCall):
            scan_expr_vars(fd, stmt)
        elif isinstance(stmt, ast.VarDecl):
            datatype_ = copy.deepcopy(stmt.datatype)
            fd.vars[stmt.name] = datatype_
            if stmt.allocate_memory_on_stack:
                var_name = 'tmp_' + str(len(fd.tmp_vars))
                fd.tmp_vars[var_name] = copy.deepcopy(stmt.datatype)
                stmt.binded_var_name = var_name
            scan_expr_vars(fd, stmt.rvalue_expr)
        elif isinstance(stmt, ast.Return):
            scan_expr_vars(fd, stmt.expr)
        elif isinstance(stmt, ast.Assign):
            scan_expr_vars(fd, stmt.rvalue_expr)
        elif isinstance(stmt, ast.If):
            scan_expr_vars(fd, stmt.condition)
            mark_out_block(fd, stmt.branch_if)
            if stmt.branch_else:
                mark_out_block(fd, stmt.branch_else)
        elif isinstance(stmt, ast.For):
            scan_expr_vars(fd, stmt.condition)
            mark_out_block(fd, stmt.branch)
        else:
            raise Exception('Bad stmt type: ' + str(type(stmt)))

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
        elif isinstance(expr, ast.Ident):
            return SimpleDataType('Int')  # TODO: get actual type
        else:
            raise Exception('Bad type: ' + str(type(expr)))

    def mark_out_var_decl_stmt(var_decl_stmt):
        datatype = get_expr_datatype(var_decl_stmt.rvalue_expr)
        var_decl_stmt.datatype = datatype

    def mark_out_assign_stmt(assign_stmt):
        datatype = get_expr_datatype(assign_stmt.rvalue_expr)
        assign_stmt.datatype = datatype

    def mark_out_stmt(stmt):
        ''' stmt - current parsed stmt in current parsed block '''
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

    def mark_out_block(func_decl, block):
        for stmt in block:
            mark_out_stmt(stmt)
            scan_stmt_vars(ast_, func_decl, stmt)

    for decl in ast_.decl_list:
        if isinstance(decl, ast.FuncDecl):
            mark_out_block(decl, decl.body)
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
