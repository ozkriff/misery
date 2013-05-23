# -*- coding: utf-8 -*-


import copy
import ast


class Variable:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Constant:
    def __init__(self, value, type):
        self.value = value
        self.type = type


class Function:
    def __init__(self, name, interface):
        self.name = name
        self.interface = interface
        self.statement_list = []
        self.constant_list = []
        self.variable_list = []
        self.expression_list = []


# TODO: ...
class IfStatement:
    def __init__(self, expression_id, if_branch_id):
        self.expression_id = expression_id
        self.if_branch_id = if_branch_id


class VariableDeclarationStatement:
    def __init__(self, variable_id, expression_id):
        self.variable_id = variable_id
        self.expression_id = expression_id


class FunctionCallStatement:
    def __init__(self, expression_id):
        self.expression_id = expression_id


class FunctionCallExpression:
    def __init__(self, name, argument_id_list, result_id):
        self.name = name
        self.argument_id_list = argument_id_list
        self.result_id = result_id


class LinkToNumberConstant:
    def __init__(self, id):
        self.id = id


class LinkToVariable:
    def __init__(self, id):
        self.id = id


class LinkToFunctionCall:
    def __init__(self, id):
        self.id = id


class Table:

    def __init__(self):
        self.declaration_list = []
        self.symbol_list = []
        self.import_list = None

    def parse_number(self, number):
        assert isinstance(number, ast.NodeNumber)
        self.declaration_list[-1].constant_list.append(
            Constant(type='int', value=number.value))
        return LinkToNumberConstant(
            id=len(self.declaration_list[-1].constant_list) - 1)

    def parse_function_call(self, function_call_node):
        assert isinstance(function_call_node, ast.NodeFunctionCall)
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
            id = self.parse_expression(argument)
            argument_id_list.append(id)
        # TODO: parse function_call_node.expression!
        assert isinstance(function_call_node.expression, ast.NodeIdentifier)
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

    def parse_expression(self, expression):
        if isinstance(expression, ast.NodeFunctionCall):
            return self.parse_function_call(expression)
        elif isinstance(expression, ast.NodeNumber):
            return self.parse_number(expression)
        else:
            assert False

    def parse_variable_declaration_statement(self, function, statement):
        expression_id = self.parse_expression(statement.expression)
        function.variable_list.append(
            Variable(
                name=statement.name,
                type=statement.type.value,
            )
        )
        function.statement_list.append(
            VariableDeclarationStatement(
                variable_id=len(function.variable_list) - 1,
                expression_id=expression_id,
            )
        )

    def parse_function_call_statement(self, function, statement):
        expression_id = self.parse_expression(statement)
        function.statement_list.append(
            FunctionCallStatement(expression_id=expression_id))

    def parse_if_statement(self, function, statement):
        # expression_id = self.parse_expression(statement.expression)
        # function.variable_list.append(
        #     Variable(
        #         name=statement.name,
        #         type=statement.type.value,
        #     )
        # )
        function.statement_list.append(
            IfStatement(
                expression_id=None,
                if_branch_id=None,
            )
        )

    def parse_statement(self, function, statement):
        '''
        Translates AST Node to Table Node.

        function -- current functions`s table
        statement -- statement to parse
        '''
        if isinstance(statement, ast.NodeVariableDeclaration):
            self.parse_variable_declaration_statement(function, statement)
        elif isinstance(statement, ast.NodeFunctionCall):
            self.parse_function_call_statement(function, statement)
        elif isinstance(statement, ast.NodeIf):
            self.parse_if_statement(function, statement)
        else:
            assert False  # TODO: ...

    def parse_function_declaration(self, declaration):
        function = Function(
            name=declaration.name,
            interface=declaration.interface,
        )
        self.declaration_list.append(function)
        for statement in declaration.body:
            self.parse_statement(function, statement)

    def generate_tables(self, ast_):
        self.import_list = copy.deepcopy(ast_.import_list)
        for declaration in ast_.declaration_sequence:
            if isinstance(declaration, ast.NodeFunctionDeclaration):
                self.parse_function_declaration(declaration)
            elif isinstance(declaration, ast.NodeTypeDeclaration):
                assert False  # TODO
            else:
                assert False

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
