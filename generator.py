# -*- coding: utf-8 -*-


import table


class Generator:

    indent = '  '

    def generate_function_parameters(self, parameter_list):
        out = ''
        is_first = True
        for parameter in parameter_list:
            if is_first:
                is_first = False
            else:
                out += ', '
            out += parameter.type.value + ' ' + parameter.name
        return out

    def generate_function_header(self, name, interface):
        out = ''
        return_type = 'void'
        if interface.return_type:
            return_type = interface.return_type.value
        function_parameters = self.generate_function_parameters(
            interface.parameter_list)
        out += return_type + ' ' + name + '(' + function_parameters + ')'
        return out

    def generate_expression(self, function, expression):
        out = ''
        assert isinstance(expression, table.FunctionCallExpression)
        for argument in expression.argument_id_list:
            if isinstance(argument, table.LinkToFunctionCall):
                last_declaration = self.table.declaration_list[-1]
                out += self.generate_expression(
                    last_declaration.expression_list[argument.id])
        out += self.indent + expression.name + '('
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
                out += str(argument.__class__)
        out += ');'
        out += '\n'
        return out

    def generate_variable_declaration_statement(self, function, statement):
        out = ''
        expression = function.expression_list[statement.expression_id.id]
        out += self.generate_expression(function, expression)
        expression_id = statement.expression_id.id
        result_id = function.expression_list[expression_id].result_id.id
        out += self.indent + function.variable_list[statement.variable_id].name
        out += ' = ' + function.variable_list[result_id].name + ';\n'
        return out

    def generate_function_call_statement(self, function, statement):
        out = ''
        expression = function.expression_list[statement.expression_id.id]
        out += self.generate_expression(function, expression)
        return out

    def generate_statement(self, function, statement):
        out = ''
        if isinstance(statement, table.VariableDeclarationStatement):
            out += self.generate_variable_declaration_statement(
                function, statement)
        elif isinstance(statement, table.FunctionCallStatement):
            out += self.generate_function_call_statement(function, statement)
        else:
            assert False
        return out

    def generate_function(self, function):
        out = ''
        out += self.generate_function_header(function.name, function.interface)
        out += ' {\n'
        for variable in function.variable_list:
            out += self.indent
            out += variable.type + ' ' + variable.name
            out += ';' + '\n'
        out += '\n'
        for statement in function.statement_list:
            out += self.generate_statement(function, statement)
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
                out += self.generate_function_header(
                    declaration.name, declaration.interface)
                out += ';\n'
        out += '\n'
        for declaration in self.table.declaration_list:
            assert isinstance(declaration, table.Function)
            out += self.generate_function(declaration)
            out += '\n'
        return out

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
