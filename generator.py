# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import ast
import misc
import textwrap


class Generator(object):

    prefix = '''
        #include <stdio.h>

        typedef int Int;
        typedef char* String;

        void printInteger(Int n) {
          printf("INTEGER: %d\n", n);
        }

        void printString(String s) {
          printf("STRING: %s\n", s);
        }

        void isLessInteger(Int* __result, Int a, Int b) {
          *__result = (a < b);
        }

        void isGreaterInteger(Int* __result, Int a, Int b) {
          *__result = (a < b);
        }

        void isEqualInteger(Int* __result, Int a, Int b) {
          *__result = (a == b);
        }

        void minusInteger(Int* __result, Int a, Int b) {
          *__result = (a - b);
        }

        void plusInteger(Int* __result, Int a, Int b) {
          *__result = (a + b);
        }

        void multiplyInteger(Int* __result, Int a, Int b) {
          *__result = (a * b);
        }

    '''

    postfix = '''
        Int main(void) {
          start();
          return 0;
        }

    '''

    def __init__(self, ast_):
        self._ast = ast_
        self._indent_level = 0
        self._function_declaration = None

    def _indent(self):
        return self._indent_level * '  '

    def _increnent_indent(self):
        self._indent_level += 1

    def _decrenent_indent(self):
        self._indent_level -= 1

    def _generate_function_parameters(self, parameter_list):
        out = ''
        is_first = True
        for parameter in parameter_list:
            if is_first:
                is_first = False
            else:
                out += ', '
            out += parameter.datatype.name + ' ' + parameter.name
        return out

    def _generate_function_header(self, name, interface):
        out = ''
        out += 'void ' + name + '('
        if interface.return_type:
            out += interface.return_type.name + '* __result'
        if len(interface.parameter_list) != 0:
            if interface.return_type:
                out += ', '
            out += self._generate_function_parameters(interface.parameter_list)
        elif not interface.return_type:
            out += 'void'
        out += ')'
        return out

    def _generate_expression_dependencies(self, function_call_expression):
        out = ''
        for argument in function_call_expression.argument_list:
            if isinstance(argument, ast.FunctionCall):
                out += self._generate_expression(argument)
        return out

    def _generate_argument(self, argument):
        out = ''
        if isinstance(argument, ast.Number):
            out += str(argument.value)
        elif isinstance(argument, ast.String):
            out += '\"' + str(argument.value) + '\"'
        elif isinstance(argument, ast.Identifier):
            # TODO: check if this is correct identifier
            out += argument.name
        elif isinstance(argument, ast.FunctionCall):
            out += argument.tmp_var
        else:
            raise Exception('Wrong argument type: ' + str(type(argument)))
        return out

    def _generate_function_call_expression_arguments(
        self,
        function_call_expression,
    ):
        out = ''
        is_first = True
        assert isinstance(function_call_expression.expression, ast.Identifier)
        called_func_name = function_call_expression.expression.name
        identifier_list = self._ast.identifier_list
        if identifier_list[called_func_name].return_type is not None:
            out += '&' + function_call_expression.tmp_var
            is_first = False
        for argument in function_call_expression.argument_list:
            if is_first:
                is_first = False
            else:
                out += ', '
            out += self._generate_argument(argument)
        return out

    def _generate_function_call_expression(self, function_call_expression):
        out = ''
        # TODO: implement other expressions
        assert isinstance(function_call_expression.expression, ast.Identifier)
        called_func_name = function_call_expression.expression.name
        out += self._generate_expression_dependencies(
            function_call_expression=function_call_expression,
        )
        out += self._indent()
        # is constructor\initializer? TODO: remove from here, do earlier
        if called_func_name[0].istitle():
            out += called_func_name + '_init'
        else:
            out += called_func_name
        out += '('
        out += self._generate_function_call_expression_arguments(
            function_call_expression,
        )
        out += ');\n'
        return out

    def _generate_expression(self, expression):
        ''' Generate evaluation code. '''
        out = ''
        if isinstance(expression, ast.FunctionCall):
            out += self._generate_function_call_expression(expression)
        else:
            raise Exception('Bad expression type: ' + str(type(expression)))
        return out

    def _generate_assign_statement(self, assign_statement):
        out = ''
        rvalue_expression = assign_statement.expression
        if isinstance(rvalue_expression, ast.Number):
            out += self._indent()
            out += assign_statement.name
            out += ' = '
            out += str(rvalue_expression.value)
            out += ';\n'
        elif isinstance(rvalue_expression, ast.String):
            out += self._indent()
            out += assign_statement.name
            out += ' = '
            out += '\"' + str(rvalue_expression.value) + '\"'
            out += ';\n'
        elif isinstance(rvalue_expression, ast.FunctionCall):
            out += self._generate_expression(rvalue_expression)
            out += self._indent()
            out += assign_statement.name
            out += ' = '
            out += assign_statement.expression.tmp_var
            out += ';\n'
        else:
            raise Exception(
                'Bad expression type: ' + str(type(rvalue_expression)),
            )
        return out

    def _generate_function_call_statement(self, statement):
        out = ''
        out += self._generate_expression(statement)
        return out

    def _generate_if_statement(self, statement):
        out = ''
        assert isinstance(statement.condition, ast.FunctionCall)
        out += self._generate_expression(statement.condition)
        out += self._indent() + 'if ('
        variable_name = statement.condition.tmp_var
        out += variable_name
        out += ') {\n'
        self._increnent_indent()
        out += self._generate_block(block=statement.branch_if)
        self._decrenent_indent()
        out += self._indent() + '}'
        if statement.branch_else:
            out += ' else {\n'
            self._increnent_indent()
            out += self._generate_block(block=statement.branch_else)
            self._decrenent_indent()
            out += self._indent() + '}'
        out += '\n'
        return out

    def _generate_for_statement(self, statement):
        out = ''
        assert isinstance(statement.condition, ast.FunctionCall)
        out += self._indent() + 'while (1) {\n'
        self._increnent_indent()
        out += self._generate_expression(statement.condition)
        variable_name = statement.condition.tmp_var
        out += self._indent() + 'if (' + '!' + variable_name + ') {\n'
        self._increnent_indent()
        out += self._indent() + 'break;\n'
        self._decrenent_indent()
        out += self._indent() + '}'
        out += '\n'
        out += self._generate_block(block=statement.branch)
        self._decrenent_indent()
        out += self._indent() + '}'
        out += '\n'
        return out

    def _generate_return_statement(self, statement):
        out = ''
        if isinstance(statement.expression, ast.FunctionCall):
            out += self._generate_expression(statement.expression)
        out += self._indent() + '*__result = '
        out += self._generate_argument(argument=statement.expression)
        out += ';\n'
        out += self._indent() + 'return;\n'
        return out

    def _generate_statement(self, statement):
        out = ''
        if isinstance(statement, ast.FunctionCall):
            out += self._generate_function_call_statement(statement)
        elif isinstance(statement, ast.VariableDeclaration):
            out += self._generate_assign_statement(statement)
        elif isinstance(statement, ast.Assign):
            out += self._generate_assign_statement(statement)
        elif isinstance(statement, ast.If):
            out += self._generate_if_statement(statement)
        elif isinstance(statement, ast.For):
            out += self._generate_for_statement(statement)
        elif isinstance(statement, ast.Return):
            out += self._generate_return_statement(statement)
        else:
            raise Exception('Bad statement type: ' + str(type(statement)))
        return out

    def _generate_block(self, block):
        out = ''
        for statement in block:
            out += self._generate_statement(statement)
        return out

    def _scan_expression(self, expression):
        vars = self._function_declaration.vars
        if isinstance(expression, ast.FunctionCall):
            for argument in expression.argument_list:
                if isinstance(argument, ast.FunctionCall):
                    self._scan_expression(argument)
            assert isinstance(expression.expression, ast.Identifier)
            called_func_name = expression.expression.name
            identifier_list = self._ast.identifier_list
            return_type = identifier_list[called_func_name].return_type
            if return_type is not None:
                var_name = 'tmp_' + str(len(vars))
                vars[var_name] = return_type
                expression.tmp_var = var_name
        elif isinstance(expression, ast.VariableDeclaration):
            vars[expression.name] = expression.datatype
            self._scan_expression(expression.expression)
        elif isinstance(expression, (ast.Number, ast.String, ast.Identifier)):
            pass  # ok
        else:
            raise Exception('Bad expression type: ' + str(type(expression)))

    # TODO: rename method, do in separate pass (like datatype)
    def _scan_vars(self, block):
        for statement in block:
            if isinstance(statement, ast.FunctionCall):
                self._scan_expression(statement)
            elif isinstance(statement, ast.VariableDeclaration):
                self._scan_expression(statement)
            elif isinstance(statement, ast.Return):
                self._scan_expression(statement.expression)
            elif isinstance(statement, ast.Assign):
                self._scan_expression(statement.expression)
            elif isinstance(statement, ast.If):
                self._scan_expression(statement.condition)
                self._scan_vars(statement.branch_if)
                if statement.branch_else:
                    self._scan_vars(statement.branch_else)
            elif isinstance(statement, ast.For):
                self._scan_expression(statement.condition)
                self._scan_vars(statement.branch)
            else:
                raise Exception('Bad statement type: ' + str(type(statement)))

    def _generate_local_variables(self):
        out = ''
        # TODO: sort! # TODO: python3
        for name, type in self._function_declaration.vars.iteritems():
            out += self._indent()
            out += type.name
            out += ' '
            out += name
            out += ';' + '\n'
        return out

    def _generate_function(self, function_declaration):
        self._function_declaration = function_declaration
        out = ''
        out += self._generate_function_header(
            name=function_declaration.name,
            interface=function_declaration.interface,
        )
        out += ' {\n'
        self._increnent_indent()
        self._scan_vars(function_declaration.body)
        out += self._generate_local_variables()
        out += '\n'
        out += self._generate_block(function_declaration.body)
        self._decrenent_indent()
        out += '}\n'
        return out

    def _generate_struct(self, struct_declaration):
        name = struct_declaration.name  # shortcut
        out = ''
        out += 'struct ' + name + ' {\n'
        self._increnent_indent()
        for field in struct_declaration.field_list:
            out += self._indent()
            out += field.datatype.name + ' ' + field.name + ';\n'
        self._decrenent_indent()
        out += '};\n'
        out += '\n'
        out += 'void ' + name + '_init(' + name + '* __result' + ') {\n'
        out += '  /* todo */\n'
        out += '}\n'
        return out

    def _generate_forward_declarations(self):
        out = ''
        for declaration in self._ast.declaration_sequence:
            if isinstance(declaration, ast.FunctionDeclaration):
                out += self._generate_function_header(
                    name=declaration.name,
                    interface=declaration.interface,
                )
                out += ';\n'
            elif isinstance(declaration, ast.StructDeclaration):
                out += 'typedef struct '
                out += declaration.name
                out += ' '
                out += declaration.name
                out += ';\n'
            else:
                raise Exception('Bad type: ' + str(type(declaration)))
        return out

    def _generate_imports(self):
        if self._ast.import_list is None:
            return ''
        out = ''
        out += '\n'
        for import_node in self._ast.import_list:
            out += '// import: ' + import_node + '\n'
        return out

    def _generate_declaration(self, declaration):
        out = ''
        if isinstance(declaration, ast.FunctionDeclaration):
            out += self._generate_function(declaration)
        elif isinstance(declaration, ast.StructDeclaration):
            out += self._generate_struct(declaration)
        else:
            raise Exception('Bad declaration type: ' + str(type(declaration)))
        return out

    def _generate_declarations(self):
        out = ''
        for declaration in self._ast.declaration_sequence:
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

    def generate_full(self):
        out = ''
        out += textwrap.dedent(Generator.prefix)
        out += self.generate()
        out += textwrap.dedent(Generator.postfix)
        return out

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
