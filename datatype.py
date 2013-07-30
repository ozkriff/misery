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


def set_datatype_marks(ast_):

    function = None

    def _x_function_call_expression(block, function_call_expression):
        return SimpleDataType('int')  # TODO: get real type

    def _x_expression(block, expression):
        if isinstance(expression, ast.Number):
            return SimpleDataType('int')
        elif isinstance(expression, ast.FunctionCall):
            return _x_function_call_expression(block, expression)
        else:
            raise Exception('Not Implemented')

    def _x_variable_declaration_statement(
            block,
            variable_declaration_statement,
    ):
        datatype = _x_expression(
            block,
            variable_declaration_statement.expression,
        )
        variable_declaration_statement.datatype = datatype

    def _x_statement(block, statement):
        ''' block - current parsed block
            statement - current parsed statement in this block
        '''
        # print '>>> _x_statement: statement: ', pretty_print(statement)
        if isinstance(statement, ast.VariableDeclaration):
            _x_variable_declaration_statement(block, statement)
        else:
            raise Exception('Not Implemented')

    def _x_function_declaration(function_declaration):
        # print '>>> _x_function_declaration: function_declaration: ',
        # pretty_print(function_declaration)
        function = function_declaration
        block = function_declaration.body
        for statement in block:
            _x_statement(block, statement)

    for declaration in ast_.declaration_sequence:
        if isinstance(declaration, ast.FunctionDeclaration):
            _x_function_declaration(declaration)
        else:
            raise Exception('Not Implemented')


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
