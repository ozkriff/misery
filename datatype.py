# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


'''
Data types.
'''


import ast
import copy


class SimpleDataType(object):
    def __init__(self, name, is_pointer=False):
        self.name = name
        self.is_pointer = is_pointer


def _mark_out_datatypes(ast_):
    ''' Mark out 'datatype' fields to ast nodes. '''

    # function = None

    def get_function_call_expression_datatype(block, function_call_expression):
        function_name = function_call_expression.expression.name
        if function_name not in ast_.identifier_list:
            raise Exception('no function: \'' + function_name + '\'')
        return ast_.identifier_list[function_name].return_type

    def get_expression_datatype(block, expression):
        if isinstance(expression, ast.Number):
            return SimpleDataType('Int')
        if isinstance(expression, ast.String):
            return SimpleDataType('String')
        elif isinstance(expression, ast.FunctionCall):
            return get_function_call_expression_datatype(block, expression)
        else:
            raise Exception('Bad type: ' + str(type(expression)))

    def mark_out_variable_declaration_statement(
        block,
        variable_declaration_statement,
    ):
        datatype = get_expression_datatype(
            block, variable_declaration_statement.expression)
        variable_declaration_statement.datatype = datatype

    def mark_out_assign_statement(block, assign_statement):
        datatype = get_expression_datatype(block, assign_statement.expression)
        assign_statement.datatype = datatype

    def mark_out_statement(block, statement):
        ''' block - current parsed block
            statement - current parsed statement in this block
        '''
        ignored_statement_type_tuple = (
            ast.FunctionCall,
            ast.Return,
            ast.If,
            ast.For,
        )
        if isinstance(statement, ast.VariableDeclaration):
            mark_out_variable_declaration_statement(block, statement)
        elif isinstance(statement, ast.Assign):
            mark_out_assign_statement(block, statement)
        elif isinstance(statement, ignored_statement_type_tuple):
            pass  # do nothing for this statements
        else:
            raise Exception('Bad type: ' + str(type(statement)))

    def mark_out_function_declaration(function_declaration):
        function = function_declaration
        block = function_declaration.body
        for statement in block:
            mark_out_statement(block, statement)

    for declaration in ast_.declaration_sequence:
        if isinstance(declaration, ast.FunctionDeclaration):
            mark_out_function_declaration(declaration)
        elif isinstance(declaration, ast.StructDeclaration):
            pass
        else:
            raise Exception('Bad type: ' + str(type(declaration)))


def mark_out_datatypes(ast_):
    ''' Mark out 'datatype' fields to ast nodes. '''
    copied_ast_ = copy.deepcopy(ast_)
    _mark_out_datatypes(copied_ast_)
    return copied_ast_


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
