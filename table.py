# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import copy
import ast
import datatype


class Variable(object):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype


class Constant(object):
    def __init__(self, value, datatype):
        self.value = value
        self.datatype = datatype


class Function(object):
    def __init__(
            self,
            name,
            interface,
            block_list,
            constant_list,
            variable_list,
            expression_list):
        self.name = name
        self.interface = interface
        self.block_list = block_list
        self.constant_list = constant_list
        self.variable_list = variable_list
        self.expression_list = expression_list


class IfStatement(object):
    def __init__(self, expression_id, if_branch_id, else_branch_id=None):
        self.expression_id = expression_id
        self.if_branch_id = if_branch_id
        self.else_branch_id = else_branch_id


class ForStatement(object):
    def __init__(self, expression_id, branch_id):
        self.expression_id = expression_id
        self.branch_id = branch_id


class VariableDeclarationStatement(object):
    def __init__(self, variable_id, expression_id):
        self.variable_id = variable_id
        self.expression_id = expression_id


class AssignStatement(object):
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


class LinkToStringConstant(object):
    def __init__(self, id):
        self.id = id


class LinkToVariable(object):
    def __init__(self, id):
        self.id = id


class LinkToParameter(object):
    def __init__(self, name):
        self.name = name


class LinkToFunctionCall(object):
    def __init__(self, id):
        self.id = id


class Table(object):

    def __init__(
            self,
            declaration_list,
            identifier_list,
            import_list):
        self.declaration_list = declaration_list
        self.identifier_list = identifier_list
        self.import_list = import_list

    def _parse_number(self, number):
        assert isinstance(number, ast.Number)
        self.declaration_list[-1].constant_list.append(
            Constant(
                datatype=datatype.SimpleDataType('Int'),
                value=number.value,
            ),
        )
        return LinkToNumberConstant(
            id=len(self.declaration_list[-1].constant_list) - 1)

    def _parse_string(self, string):
        assert isinstance(string, ast.String)
        last_declaration = self.declaration_list[-1]
        last_declaration.constant_list.append(
            Constant(
                datatype=datatype.SimpleDataType('String'),
                value=string.value,
            ),
        )
        return LinkToStringConstant(
            id=len(last_declaration.constant_list) - 1
        )

    def _parse_identifier(self, identidier_node):
        assert isinstance(identidier_node, ast.Identifier)
        # TODO: find this identifier
        return LinkToParameter(name=identidier_node.name)

    def _parse_function_call(self, function_call_node):
        assert isinstance(function_call_node, ast.FunctionCall)
        function_name = function_call_node.expression.name
        last_declaration = self.declaration_list[-1]
        varname = 'tmp_' + str(len(last_declaration.variable_list))
        if function_name not in self.identifier_list:
            raise Exception('no function: \'' + function_name + '\'')
        return_type = self.identifier_list[function_name].return_type
        result_id = None
        if return_type is not None:
            last_declaration.variable_list.append(
                Variable(name=varname, datatype=return_type))
            result_id = LinkToVariable(
                id=len(last_declaration.variable_list) - 1)
        argument_id_list = []
        for argument in function_call_node.argument_list:
            id = self._parse_expression(argument)
            argument_id_list.append(id)
        # TODO: parse function_call_node.expression!
        assert isinstance(function_call_node.expression, ast.Identifier)
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
        elif isinstance(expression, ast.String):
            return self._parse_string(expression)
        elif isinstance(expression, ast.Identifier):
            return self._parse_identifier(expression)
        elif expression is None:
            return
        else:
            raise Exception('Not Implemented')

    def _parse_variable_declaration_statement(
            self, function, statement, block):
        assert(statement.datatype is not None)
        expression_id = self._parse_expression(statement.expression)
        function.variable_list.append(
            Variable(
                name=statement.name,
                datatype=statement.datatype,
            )
        )
        block.append(
            VariableDeclarationStatement(
                variable_id=len(function.variable_list) - 1,
                expression_id=expression_id,
            )
        )

    def _find_variable_id_by_name(self, function, variable_name):
        for id, variable in enumerate(function.variable_list):
            if variable.name == variable_name:
                return id
        raise Exception('bad variable name: ' + str(variable_name))

    def _parse_assign_statement(self, function, statement, block):
        variable_id = self._find_variable_id_by_name(function, statement.name)
        expression_id = self._parse_expression(statement.expression)
        block.append(
            AssignStatement(
                variable_id=variable_id,
                expression_id=expression_id,
            )
        )

    def _parse_function_call_statement(self, function, statement, block):
        expression_id = self._parse_expression(statement)
        block.append(
            FunctionCallStatement(expression_id=expression_id))

    def _parse_if_statement(self, function, statement, block):
        expression_id = self._parse_expression(statement.condition)
        if_block_id = self._parse_block(function, statement.branch_if)
        else_block_id = None  # optional branch
        if statement.branch_else:
            else_block_id = self._parse_block(function, statement.branch_else)
        block.append(
            IfStatement(
                expression_id=expression_id,
                if_branch_id=if_block_id,
                else_branch_id=else_block_id,
            )
        )

    def _parse_for_statement(self, function, statement, block):
        expression_id = self._parse_expression(statement.condition)
        block_id = self._parse_block(function, statement.branch)
        block.append(
            ForStatement(
                expression_id=expression_id,
                branch_id=block_id,
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
        elif isinstance(statement, ast.Assign):
            self._parse_assign_statement(function, statement, block)
        elif isinstance(statement, ast.FunctionCall):
            self._parse_function_call_statement(function, statement, block)
        elif isinstance(statement, ast.If):
            self._parse_if_statement(function, statement, block)
        elif isinstance(statement, ast.For):
            self._parse_for_statement(function, statement, block)
        elif isinstance(statement, ast.Return):
            self._parse_return_statement(function, statement, block)
        else:
            raise Exception('Not Implemented')

    def _parse_block(self, function, declaration):
        function.block_list.append([])
        b = function.block_list[-1]
        for statement in declaration:
            self._parse_statement(
                function, statement, b)
        return len(function.block_list) - 1

    def _parse_function_declaration(self, declaration):
        function = Function(
            name=declaration.name,
            interface=declaration.interface,
            constant_list=[],
            variable_list=[],
            block_list=[],
            expression_list=[],
        )
        self.declaration_list.append(function)
        self._parse_block(function, declaration.body)

    @classmethod
    def from_ast(cls, ast_):
        new_table = Table(
            declaration_list=[],
            identifier_list=IdentifierTable(ast_).identifier_list,
            import_list=copy.deepcopy(ast_.import_list),
        )
        # fill declaration_list...
        for declaration in ast_.declaration_sequence:
            if isinstance(declaration, ast.FunctionDeclaration):
                new_table._parse_function_declaration(declaration)
            elif isinstance(declaration, ast.TypeDeclaration):
                raise Exception('Not Implemented')
            else:
                raise Exception('Not Implemented')
        return new_table


# TODO: Move to some other file (closer to AST)
class IdentifierTable(object):

    def append_standart_functions(self, identifier_list):
        std_interface = ast.FunctionInterface(
            return_type=datatype.SimpleDataType('Int'),
            parameter_list=[
                ast.Parameter(
                    name='a',
                    datatype=datatype.SimpleDataType('Int'),
                ),
                ast.Parameter(
                    name='b',
                    datatype=datatype.SimpleDataType('Int'),
                ),
            ],
        )
        identifier_list['printString'] = ast.FunctionInterface(
            parameter_list=[
                ast.Parameter(
                    name='s',
                    datatype=datatype.SimpleDataType('String'),
                ),
            ],
        )
        identifier_list['printInteger'] = ast.FunctionInterface(
            parameter_list=[
                ast.Parameter(
                    name='n',
                    datatype=datatype.SimpleDataType('Int'),
                ),
            ],
        )
        identifier_list['isEqualInteger'] = std_interface
        identifier_list['isLessInteger'] = std_interface
        identifier_list['isGreaterInteger'] = std_interface
        identifier_list['minusInteger'] = std_interface
        identifier_list['plusInteger'] = std_interface
        identifier_list['multiplyInteger'] = std_interface

    def __init__(self, ast_):
        identifier_list = {}
        for declaration in ast_.declaration_sequence:
            if isinstance(declaration, ast.FunctionDeclaration):
                identifier_list[declaration.name] = declaration.interface
        self.append_standart_functions(identifier_list)
        self.identifier_list = identifier_list

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
