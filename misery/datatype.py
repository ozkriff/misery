# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


'''
Data types.
'''


import copy
from misery import (
    ast,
    misc,
)


class SimpleDataType(object):
    def __init__(self, name):
        self.name = name


def find_var_datatype(func_decl, var_name):
    for parameter in func_decl.signature.par_list:
        if parameter.name == var_name:
            return parameter.datatype
    for local_var_name in func_decl.vars.keys():
        if local_var_name == var_name:
            return func_decl.vars[local_var_name]
    raise Exception('Bad var name: \'' + var_name + '\'')


def get_expr_datatype(ident_list, func_decl, expr):
    if isinstance(expr, ast.Number):
        return SimpleDataType('Int')
    elif isinstance(expr, ast.String):
        return SimpleDataType('String')
    elif isinstance(expr, ast.Ident):
        return find_var_datatype(func_decl, expr.name)
    elif isinstance(expr, ast.FuncCall):
        return get_func_call_expr_datatype(
            func_decl,
            ident_list,
            expr,
        )
    else:
        raise Exception('Bad type: ' + str(type(expr)))


def get_func_call_expr_datatype(func_decl, ident_list, func_call_expr):
    ''' Get datatype of function call expr. '''
    func_name = func_call_expr.called_expr.name  # shortcut
    if func_name not in ident_list:
        raise Exception('no func: \'' + func_name + '\'')
    return find_func_signature(
        ident_list,
        func_decl,
        func_call_expr,
    ).return_type


def find_func_signature(ident_list, func_decl, func_call_expr):
    expr = func_call_expr  # shortcut
    assert isinstance(expr.called_expr, ast.Ident)
    func_name = expr.called_expr.name
    signature_list = ident_list[func_name]
    if not signature_list:
        raise Exception('Can not find any signatures')
    signature_list = misc.tolist(signature_list)
    for signature in signature_list:
        par_count = len(signature.par_list)
        arg_count = len(expr.arg_list)
        if par_count == 0 and arg_count == 0:
            return signature
        if par_count != arg_count:
            continue
        for arg, par in zip(expr.arg_list, signature.par_list):
            if isinstance(arg, ast.FuncCall):
                arg_type = find_func_signature(
                    ident_list,
                    func_decl,
                    arg,
                ).return_type
            else:
                arg_type = get_expr_datatype(ident_list, func_decl, arg)
            if arg_type.name == par.datatype.name:
                return signature
    raise Exception('Can not find matching signature')


# TODO: split statement processing phases
def _mark_out_datatypes(ast_):
    ''' Mark out 'datatype' fields to ast nodes. '''

    func_decl = None

    def scan_stmt_vars(stmt):

        def scan_expr_vars(expr):
            fd = func_decl  # shortcut
            if isinstance(expr, ast.FuncCall):
                for arg in expr.arg_list:
                    scan_expr_vars(arg)
                assert isinstance(expr.called_expr, ast.Ident)
                called_func_name = expr.called_expr.name
                return_type = find_func_signature(
                    ast_.ident_list,
                    func_decl,
                    expr,
                ).return_type
                if return_type:
                    var_name = 'tmp_' + str(len(fd.tmp_vars))
                    fd.tmp_vars[var_name] = return_type
                    expr.binded_var_name = var_name
            elif isinstance(expr, (ast.Number, ast.String)):
                var_name = 'const_' + str(len(fd.constants))
                fd.constants[var_name] = copy.deepcopy(expr)
                expr.binded_var_name = var_name
            elif isinstance(expr, ast.Ident):
                pass  # ok
            else:
                raise Exception('Bad expr type: ' + str(type(expr)))

        if isinstance(stmt, ast.FuncCall):
            scan_expr_vars(stmt)
        elif isinstance(stmt, ast.VarDecl):
            datatype_ = copy.deepcopy(stmt.datatype)
            func_decl.vars[stmt.name] = datatype_
            if stmt.allocate_memory_on_stack:
                var_name = 'tmp_' + str(len(func_decl.tmp_vars))
                func_decl.tmp_vars[var_name] = copy.deepcopy(stmt.datatype)
                stmt.binded_var_name = var_name
            scan_expr_vars(stmt.rvalue_expr)
        elif isinstance(stmt, ast.Return):
            scan_expr_vars(stmt.expr)
        elif isinstance(stmt, ast.Assign):
            scan_expr_vars(stmt.rvalue_expr)
        elif isinstance(stmt, ast.If):
            scan_expr_vars(stmt.condition)
            mark_out_block(stmt.branch_if)
            if stmt.branch_else:
                mark_out_block(stmt.branch_else)
        elif isinstance(stmt, ast.For):
            scan_expr_vars(stmt.condition)
            mark_out_block(stmt.branch)
        else:
            raise Exception('Bad stmt type: ' + str(type(stmt)))

    def mark_out_var_decl_stmt(var_decl_stmt):
        var_decl_stmt.datatype = get_expr_datatype(
            ast_.ident_list,
            func_decl,
            var_decl_stmt.rvalue_expr,
        )

    def mark_out_assign_stmt(assign_stmt):
        assign_stmt.datatype = get_expr_datatype(
            ast_.ident_list,
            func_decl,
            assign_stmt.rvalue_expr,
        )

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

    def mark_out_block(block):
        for stmt in block:
            mark_out_stmt(stmt)
            scan_stmt_vars(stmt)

    for decl in ast_.decl_list:
        if isinstance(decl, ast.FuncDecl):
            func_decl = decl
            mark_out_block(decl.body)
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
