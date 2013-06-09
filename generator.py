# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import table


class Generator(object):

    prefix = (
        '#include <stdio.h>\n'
        '\n'
        'void printInteger(int n) {\n'
        '  printf("INTEGER: %d\\n", n);\n'
        '}\n'
        '\n'
        'void isEqualInteger(int* __result, int a, int b) {\n'
        '  *__result = (a == b);\n'
        '}\n'
        '\n'
        'void minusInteger(int* __result, int a, int b) {\n'
        '  *__result = (a - b);\n'
        '}\n'
        '\n'
        'void multiplyInteger(int* __result, int a, int b) {\n'
        '  *__result = (a * b);\n'
        '}\n'
        '\n'
    )

    postfix = (
        '\n'
        'int main(void) {\n'
        '  int n;\n'
        '  fac(&n, 2);\n'
        '  printInteger(n);\n'
        '  fac(&n, 3);\n'
        '  printInteger(n);\n'
        '  fac(&n, 4);\n'
        '  printInteger(n);\n'
        '  fac(&n, 5);\n'
        '  printInteger(n);\n'
        '  return 0;\n'
        '}\n'
        '\n'
    )

    def __init__(self):
        self.indent_level = 0

    def _indent(self):
        return self.indent_level * '  '

    def _increnent_indent(self):
        self.indent_level += 1

    def _decrenent_indent(self):
        self.indent_level -= 1

    def _generate_function_parameters(self, parameter_list):
        if len(parameter_list) == 0:
            return 'void'
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
        out += 'void ' + name + '('
        if interface.return_type:
            out += interface.return_type.value + '* __result, '
        out += self._generate_function_parameters(interface.parameter_list)
        out += ')'
        return out

    def _generate_expression_dependancies(self, function, expression):
        out = ''
        for argument in expression.argument_id_list:
            if isinstance(argument, table.LinkToFunctionCall):
                last_declaration = self.table.declaration_list[-1]
                out += self._generate_expression(
                    function, last_declaration.expression_list[argument.id])
        return out

    def _generate_argument(self, function, argument):
        out = ''
        if isinstance(argument, table.LinkToNumberConstant):
            out += str(function.constant_list[argument.id].value)
        elif isinstance(argument, table.LinkToFunctionCall):
            result_id = function.expression_list[argument.id].result_id.id
            out += str(function.variable_list[result_id].name)
        elif isinstance(argument, table.LinkToVariable):
            out += function.variable_list[argument.id].name
        elif isinstance(argument, table.LinkToParameter):
            out += argument.name
        else:
            raise Exception("Wrong argument type: " + str(type(argument)))
        return out

    def _generate_function_call_expression_arguments(
            self, function, expression):
        out = ''
        # out var. passed by pointer
        # TODO: check in symtable if there are any return value
        out += '&' + function.variable_list[expression.result_id.id].name
        for argument in expression.argument_id_list:
            out += ', ' + self._generate_argument(function, argument)
        return out

    def _generate_function_call_expression(self, function, expression):
        out = ''
        out += self._generate_expression_dependancies(function, expression)
        out += self._indent()
        out += expression.name
        out += '('
        out += self._generate_function_call_expression_arguments(
            function, expression)
        out += ');\n'
        return out

    def _generate_expression(self, function, expression):
        ''' Generate evaluation code. '''
        out = ''
        if isinstance(expression, table.FunctionCallExpression):
            out += self._generate_function_call_expression(
                function, expression)
        else:
            raise Exception("Not Implemented")
        return out

    def _generate_variable_declaration_statement(self, function, statement):
        out = ''
        expression = function.expression_list[statement.expression_id.id]
        out += self._generate_expression(function, expression)
        expression_id = statement.expression_id.id
        result_id = function.expression_list[expression_id].result_id.id
        out += self._indent()
        out += function.variable_list[statement.variable_id].name
        out += ' = ' + function.variable_list[result_id].name + ';\n'
        return out

    def _generate_function_call_statement(self, function, statement):
        out = ''
        expression = function.expression_list[statement.expression_id.id]
        out += self._generate_expression(function, expression)
        return out

    def _generate_if_statement(self, function, statement):
        out = ''
        expression = function.expression_list[statement.expression_id.id]
        assert isinstance(expression, table.FunctionCallExpression)
        out += self._generate_expression(function, expression)
        out += self._indent() + 'if ('
        out += self._generate_argument(function, expression.result_id)
        out += ') {\n'
        block = function.block_list[statement.if_branch_id]
        self._increnent_indent()
        out += self._generate_block(function, block)
        self._decrenent_indent()
        out += self._indent() + '}' + '\n'
        return out

    def _generate_return_statement(self, function, statement):
        out = ''
        if isinstance(statement.expression_id, table.LinkToFunctionCall):
            expression = function.expression_list[statement.expression_id.id]
            out += self._generate_expression(function, expression)
        out += self._indent() + '*__result = '
        out += self._generate_argument(function, statement.expression_id)
        out += ';\n'
        out += self._indent() + 'return;\n'
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

    def _generate_local_variables(self, function):
        out = ''
        for variable in function.variable_list:
            out += self._indent()
            out += variable.type + ' ' + variable.name
            out += ';' + '\n'
        return out

    def _generate_function(self, function):
        out = ''
        out += self._generate_function_header(
            function.name, function.interface)
        out += ' {\n'
        self._increnent_indent()
        out += self._generate_local_variables(function)
        out += '\n'
        out += self._generate_block(function, function.block_list[0])
        self._decrenent_indent()
        out += '}\n'
        return out

    def _generate_forward_declarations(self):
        out = ''
        for declaration in self.table.declaration_list:
            if isinstance(declaration, table.Function):
                out += self._generate_function_header(
                    declaration.name, declaration.interface)
                out += ';\n'
        return out

    def _generate_imports(self):
        if self.table.import_list is None:
            return ''
        out = ''
        for import_node in self.table.import_list:
            out += '// import: ' + import_node + '\n'
        return out

    def _generate_declaration(self, declaration):
        out = ''
        if isinstance(declaration, table.Function):
            out += self._generate_function(declaration)
        else:
            raise Exception("Not Implemented")
        return out

    def _generate_declarations(self):
        out = ''
        for declaration in self.table.declaration_list:
            out += self._generate_declaration(declaration)
            out += '\n'
        return out

    def generate(self):
        out = ''
        out += self._generate_imports()
        out += '\n'
        out += self._generate_forward_declarations()
        out += '\n'
        out += self._generate_declarations()
        return out

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
