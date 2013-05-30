# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import copy
import ast


class Variable(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Constant(object):
    def __init__(self, value, type):
        self.value = value
        self.type = type


class Function(object):
    def __init__(self, name, interface):
        self.name = name
        self.interface = interface
        self.block_list = []
        self.constant_list = []
        self.variable_list = []
        self.expression_list = []


class IfStatement(object):
    def __init__(self, expression_id, if_branch_id):
        self.expression_id = expression_id
        self.if_branch_id = if_branch_id


class VariableDeclarationStatement(object):
    def __init__(self, variable_id, expression_id):
        self.variable_id = variable_id
        self.expression_id = expression_id


class ReturnStatement(object):
    def __init__(self, expression_id):
        self.expression_id = expression_id


class FunctionCallStatement(object):
    def __init__(self, expression_id):
        self.expression_id = expression_id


class FunctionCallExpression(object):
    def __init__(self, name, argument_id_list, result_id):
        self.name = name
        self.argument_id_list = argument_id_list
        self.result_id = result_id


class LinkToNumberConstant(object):
    def __init__(self, id):
        self.id = id


class LinkToVariable(object):
    def __init__(self, id):
        self.id = id


class LinkToFunctionCall(object):
    def __init__(self, id):
        self.id = id


class Table(object):

    def __init__(self):
        self.declaration_list = []
        self.symbol_list = []
        self.import_list = None

    def _parse_number(self, number):
        assert isinstance(number, ast.Number)
        self.declaration_list[-1].constant_list.append(
            Constant(type='int', value=number.value))
        return LinkToNumberConstant(
            id=len(self.declaration_list[-1].constant_list) - 1)

    def _parse_function_call(self, function_call_node):
        assert isinstance(function_call_node, ast.FunctionCall)
        last_declaration = self.declaration_list[-1]
        varname = 'tmp_' + str(len(last_declaration.variable_list))
        # TODO: get type from some global symtable
        return_type = 'int'
        last_declaration.variable_list.append(
            Variable(name=varname, type=return_type))
        result_id = LinkToVariable(
            id=len(last_declaration.variable_list) - 1)
        argument_id_list = []
        for argument in function_call_node.argument_list:
            id = self._parse_expression(argument)
            argument_id_list.append(id)
        # TODO: parse function_call_node.expression!
        assert isinstance(function_call_node.expression, ast.Identifier)
        function_name = function_call_node.expression.value
        last_declaration.expression_list.append(
            FunctionCallExpression(
                name=function_name,
                argument_id_list=argument_id_list,
                result_id=result_id,
            )
        )
        return LinkToFunctionCall(
            id=len(last_declaration.expression_list) - 1)

    def _parse_expression(self, expression):
        if isinstance(expression, ast.FunctionCall):
            return self._parse_function_call(expression)
        elif isinstance(expression, ast.Number):
            return self._parse_number(expression)
        elif expression is None:
            return
        else:
            raise Exception('Not Implemented')

    def _parse_variable_declaration_statement(
            self, function, statement, block):
        expression_id = self._parse_expression(statement.expression)
        function.variable_list.append(
            Variable(
                name=statement.name,
                type=statement.type.value,
            )
        )
        block.append(
            VariableDeclarationStatement(
                variable_id=len(function.variable_list) - 1,
                expression_id=expression_id,
            )
        )

    def _parse_function_call_statement(self, function, statement, block):
        expression_id = self._parse_expression(statement)
        block.append(
            FunctionCallStatement(expression_id=expression_id))

    def _parse_if_statement(self, function, statement, block):
        expression_id = self._parse_expression(statement.condition)
        block_id = self._parse_block(function, statement.branch_if)
        block.append(
            IfStatement(
                expression_id=expression_id,
                if_branch_id=block_id,
            )
        )

    def _parse_return_statement(self, function, statement, block):
        expression_id = self._parse_expression(statement.expression)
        block.append(
            ReturnStatement(expression_id=expression_id),
        )

    def _parse_statement(self, function, statement, block):
        if isinstance(statement, ast.VariableDeclaration):
            self._parse_variable_declaration_statement(
                function, statement, block)
        elif isinstance(statement, ast.FunctionCall):
            self._parse_function_call_statement(function, statement, block)
        elif isinstance(statement, ast.If):
            self._parse_if_statement(function, statement, block)
        elif isinstance(statement, ast.Return):
            self._parse_return_statement(function, statement, block)
        else:
            raise Exception('Not Implemented')

    def _parse_block(self, function, declaration):
        function.block_list.append([])
        for statement in declaration:
            self._parse_statement(
                function, statement, function.block_list[-1])
        return len(function.block_list) - 1

    def _parse_function_declaration(self, declaration):
        function = Function(
            name=declaration.name,
            interface=declaration.interface,
        )
        self.declaration_list.append(function)
        self._parse_block(function, declaration.body)

    def generate_tables(self, ast_):
        self.import_list = copy.deepcopy(ast_.import_list)
        for declaration in ast_.declaration_sequence:
            if isinstance(declaration, ast.FunctionDeclaration):
                self._parse_function_declaration(declaration)
            elif isinstance(declaration, ast.TypeDeclaration):
                raise Exception('Not Implemented')
            else:
                raise Exception('Not Implemented')

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
