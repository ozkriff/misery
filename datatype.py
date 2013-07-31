# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


'''
Data types.
'''


import misc
import ast


class SimpleDataType(object):
    def __init__(self, name):
        self.name = name


def mark_out_datatypes(ast_):
    ''' Mark out 'datatype' fields to ast nodes. '''

    function = None

    def get_function_call_expression_datatype(block, function_call_expression):
        # TODO: find this function and get real type
        return SimpleDataType('int')

    def get_expression_datatype(block, expression):
        if isinstance(expression, ast.Number):
            return SimpleDataType('int')
        elif isinstance(expression, ast.FunctionCall):
            return get_function_call_expression_datatype(block, expression)
        else:
            raise Exception('Not Implemented: ' + str(type(expression)))

    def mark_out_variable_declaration_statement(
            block, variable_declaration_statement):
        datatype = get_expression_datatype(
            block, variable_declaration_statement.expression)
        variable_declaration_statement.datatype = datatype

    def mark_out_statement(block, statement):
        ''' block - current parsed block
            statement - current parsed statement in this block
        '''
        ignored_statement_type_tuple = (
            ast.FunctionCall,
            ast.Return,
            ast.If,
        )
        if isinstance(statement, ast.VariableDeclaration):
            mark_out_variable_declaration_statement(block, statement)
        elif isinstance(statement, ignored_statement_type_tuple):
            pass  # do nothing for this statements
        else:
            raise Exception('Not Implemented: ' + str(type(statement)))

    def mark_out_function_declaration(function_declaration):
        function = function_declaration
        block = function_declaration.body
        for statement in block:
            mark_out_statement(block, statement)

    for declaration in ast_.declaration_sequence:
        if isinstance(declaration, ast.FunctionDeclaration):
            mark_out_function_declaration(declaration)
        else:
            raise Exception('Not Implemented: ' + str(type(declaration)))


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
