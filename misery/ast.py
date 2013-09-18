# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details

'''
Asbtract Syntax Tree
'''


class Module(object):
    def __init__(self, import_list=None, decl_seq=None):
        assert import_list is None or isinstance(import_list, list)
        assert (decl_seq is None or
                isinstance(decl_seq, list))
        self.import_list = import_list
        self.decl_seq = decl_seq
        self.ident_list = None


class Ident(object):
    def __init__(self, name):
        self.name = name


class Field(object):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype


class ConstDecl(object):
    def __init__(self, name, datatype, expr):
        self.name = name
        self.datatype = datatype
        self.expr = expr


class StructDecl(object):
    def __init__(self, name, field_list):
        self.name = name
        self.field_list = field_list


class Number(object):
    def __init__(self, value):
        self.value = value
        self.binded_var_name = None


class String(object):
    def __init__(self, value):
        self.value = value
        self.binded_var_name = None


class FuncDecl(object):
    def __init__(self, name, signature, body):
        self.name = name
        self.signature = signature
        self.body = body
        # TODO: move to ast.Block ...
        self.vars = {}
        self.tmp_vars = {}
        self.constants = {}


class FuncSignature(object):
    def __init__(
        self,
        par_list,
        generic_par_list=None,
        return_type=None,
    ):
        self.par_list = par_list
        if generic_par_list:
            self.generic_par_list = generic_par_list
        else:
            self.generic_par_list = []
        self.return_type = return_type


class Parameter(object):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype


class FuncCall(object):
    def __init__(self, expr, arg_list):
        self.called_expr = expr
        self.arg_list = arg_list
        self.binded_var_name = None


class VarDecl(object):
    def __init__(
        self,
        name,
        expr=None,
        datatype=None,
        allocate_memory_on_stack=False,
    ):
        self.name = name
        self.rvalue_expr = expr
        self.datatype = datatype
        self.allocate_memory_on_stack = allocate_memory_on_stack


class Assign(object):
    def __init__(
        self,
        name,
        expr=None,
        datatype=None,
    ):
        self.name = name
        self.rvalue_expr = expr
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
    def __init__(self, expr=None):
        self.expr = expr


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
