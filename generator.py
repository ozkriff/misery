# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import table


class Generator:

    def __init__(self):
        self.indent_level = 0

    def _indent(self):
        return self.indent_level * '  '

    def _increnent_indent(self):
        self.indent_level += 1

    def _decrenent_indent(self):
        self.indent_level -= 1

    def _generate_function_parameters(self, parameter_list):
        out = ''
        is_first = True
        for parameter in parameter_list:
            if is_first:
                is_first = False
            else:
                out += ', '
            out += parameter.type.value + ' ' + parameter.name
        return out

    def _generate_function_header(self, name, interface):
        out = ''
        return_type = 'void'
        if interface.return_type:
            return_type = interface.return_type.value
        function_parameters = self._generate_function_parameters(
            interface.parameter_list)
        out += return_type + ' ' + name + '(' + function_parameters + ')'
        return out

    def _generate_expression(self, function, expression):
        out = ''
        assert isinstance(expression, table.FunctionCallExpression)
        for argument in expression.argument_id_list:
            if isinstance(argument, table.LinkToFunctionCall):
                last_declaration = self.table.declaration_list[-1]
                out += self._indent()
                out += self._generate_expression(
                    function, last_declaration.expression_list[argument.id])
                out += ';' + '\n'
        out += expression.name + '('
        # out var. passed by pointer
        out += '&' + function.variable_list[expression.result_id.id].name
        for argument in expression.argument_id_list:
            out += ', '
            if isinstance(argument, table.LinkToNumberConstant):
                out += str(function.constant_list[argument.id].value)
            elif isinstance(argument, table.LinkToFunctionCall):
                result_id = function.expression_list[argument.id].result_id.id
                out += str(function.variable_list[result_id].name)
            else:
                # out += str(argument.__class__)
                raise Exception("Not Implemented")
        out += ')'
        return out

    def _generate_variable_declaration_statement(self, function, statement):
        out = ''
        expression = function.expression_list[statement.expression_id.id]
        out += self._indent()
        out += self._generate_expression(function, expression)
        out += ';' + '\n'
        expression_id = statement.expression_id.id
        result_id = function.expression_list[expression_id].result_id.id
        out += self._indent()
        out += function.variable_list[statement.variable_id].name
        out += ' = ' + function.variable_list[result_id].name + ';\n'
        return out

    def _generate_function_call_statement(self, function, statement):
        out = ''
        expression = function.expression_list[statement.expression_id.id]
        out += self._indent()
        out += self._generate_expression(function, expression)
        out += ';' + '\n'
        return out

    def _generate_if_statement(self, function, statement):
        out = ''

        expression = function.expression_list[statement.expression_id.id]
        cond = self._generate_expression(function, expression)

        out += self._indent() + 'if (' + cond + ') {' + '\n'

        block = function.block_list[statement.if_branch_id]
        self._increnent_indent()
        out += self._generate_block(function, block)
        self._decrenent_indent()

        out += self._indent() + '}' + '\n'
        return out

    def _generate_return_statement(self, function, statement):
        out = ''
        out += self._indent() + 'return '
        out += '0' # TODO: expression?
        out += ';' + '\n'
        return out

    def _generate_statement(self, function, statement):
        out = ''
        if isinstance(statement, table.VariableDeclarationStatement):
            out += self._generate_variable_declaration_statement(
                function, statement)
        elif isinstance(statement, table.FunctionCallStatement):
            out += self._generate_function_call_statement(function, statement)
        elif isinstance(statement, table.IfStatement):
            out += self._generate_if_statement(function, statement)
        elif isinstance(statement, table.ReturnStatement):
            out += self._generate_return_statement(function, statement)
        else:
            raise Exception("Not Implemented")
        return out

    def _generate_block(self, function, block):
        out = ''
        for statement in block:
            out += self._generate_statement(function, statement)
        return out

    def _generate_function(self, function):
        out = ''
        out += self._generate_function_header(function.name, function.interface)
        out += ' {\n'
        self._increnent_indent()
        for variable in function.variable_list:
            out += self._indent()
            out += variable.type + ' ' + variable.name
            out += ';' + '\n'
        out += '\n'
        out += self._generate_block(function, function.block_list[0])
        self._decrenent_indent()
        out += '}\n'
        return out

    def generate(self):
        out = ''
        if self.table.import_list is not None:
            for import_node in self.table.import_list:
                out += '// import: ' + import_node + '\n'
        out += '\n'
        for declaration in self.table.declaration_list:
            if isinstance(declaration, table.Function):
                out += self._generate_function_header(
                    declaration.name, declaration.interface)
                out += ';\n'
        out += '\n'
        for declaration in self.table.declaration_list:
            assert isinstance(declaration, table.Function)
            out += self._generate_function(declaration)
            out += '\n'
        return out

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
