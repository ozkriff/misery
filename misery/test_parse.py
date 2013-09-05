# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test parse module. '''


import unittest
import copy
from misery import (
    ast,
    datatype,
    misc,
    parse,
)


class TestParser(unittest.TestCase):
    ''' Test parse.make_parser() function. '''

    # Standart module.
    # Usage:
    #   expected_ast = copy.deepcopy(self._std_module)
    #   <add specific detaild to expected_ast>
    _std_module = ast.Module(
        declaration_sequence=[
            ast.FunctionDeclaration(
                name='start',
                signature=ast.FunctionSignature(parameter_list=[]),
                body=[],
            )
        ]
    )

    def _parse(self, input_string):
        real_ast = parse.make_parser().parse(
            input_string,
            lexer=parse.make_lexer())
        return real_ast

    def test_empty_module(self):
        ''' Parse empty string. '''
        input_string = ''
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            declaration_sequence=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_empty_import(self):
        ''' Parse empty import statement. '''
        input_string = 'import {}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            import_list=[],
            declaration_sequence=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_import(self):
        ''' Parse import statement. '''
        input_string = 'import {module1}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            import_list=['module1'],
            declaration_sequence=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_import_2(self):
        ''' Parse import statement with two modules. '''
        input_string = 'import {module1 module2}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            import_list=['module1', 'module2'],
            declaration_sequence=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_struct_type_declaration(self):
        ''' Parse struct type declaration. '''
        input_string = (
            'MyStruct := struct {\n'
            '  field1: Int\n'
            '  field2: Float\n'
            '}\n'
        )
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            declaration_sequence=[
                ast.StructDeclaration(
                    name='MyStruct',
                    field_list=[
                        ast.Field(
                            name='field1',
                            datatype=datatype.SimpleDataType('Int'),
                        ),
                        ast.Field(
                            name='field2',
                            datatype=datatype.SimpleDataType('Float'),
                        )
                    ]
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_const_declaration(self):
        ''' Parse constant declaration. '''
        input_string = 'const importantIdentifier:Int := 10'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            declaration_sequence=[
                ast.ConstDeclaration(
                    name='importantIdentifier',
                    datatype=datatype.SimpleDataType('Int'),
                    expression=ast.Number(10),
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func(self):
        ''' Parse minimal fnction declaration. '''
        input_string = 'testfunc2 := func() {}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='testfunc2',
                    signature=ast.FunctionSignature(parameter_list=[]),
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_return_value(self):
        ''' Parse function that returns Int. '''
        input_string = 'testfunc2 := func () -> Int {}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='testfunc2',
                    signature=ast.FunctionSignature(
                        parameter_list=[],
                        return_type=datatype.SimpleDataType('Int'),
                    ),
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_parameter(self):
        ''' Parse function that takes one parameter. '''
        input_string = 'testfunc := func (par:ParType) {}'
        real_ast = self._parse(input_string)
        signature = ast.FunctionSignature(
            parameter_list=[
                ast.Parameter(
                    name='par',
                    datatype=datatype.SimpleDataType('ParType')
                )
            ],
        )
        expected_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='testfunc',
                    signature=signature,
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_2_parameters(self):
        ''' Parse function that takes two parameters. '''
        input_string = 'testfunc := func (par1:ParType par2:ParType) {}'
        real_ast = self._parse(input_string)
        signature = ast.FunctionSignature(
            parameter_list=[
                ast.Parameter(
                    name='par1',
                    datatype=datatype.SimpleDataType('ParType'),
                ),
                ast.Parameter(
                    name='par2',
                    datatype=datatype.SimpleDataType('ParType'),
                )
            ]
        )
        expected_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='testfunc',
                    signature=signature,
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_func_body_2_empty_blocks(self):
        ''' Parse fnction with empty blocks. '''
        input_string = 'start := func () { {} {} }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body = [[], []]
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_call(self):
        ''' Parse simple function call. '''
        input_string = 'start := func () { fname2() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        funccall = ast.FunctionCall(
            expression=ast.Identifier('fname2'),
            argument_list=[],
        )
        expected_ast.declaration_sequence[0].body.append(funccall)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_without_initialization(self):
        ''' Parse variable declaration statement. '''
        input_string = 'start := func () { testVar := Int() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VariableDeclaration(
            name='testVar',
            expression=ast.FunctionCall(
                expression=ast.Identifier('Int'),
                argument_list=[],
            )
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_type_and_initialization(self):
        ''' Parse variable declaration statement with initiaization. '''
        input_string = 'start := func () { testVar := Int(666) }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VariableDeclaration(
            name='testVar',
            expression=ast.FunctionCall(
                expression=ast.Identifier('Int'),
                argument_list=[
                    ast.Number(666),
                ],
            ),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_initialization(self):
        ''' Parse variable declaration statement with
            initiaization and without explicit  type.
        '''
        input_string = 'start := func () { testVar := 666 }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VariableDeclaration(
            name='testVar',
            expression=ast.Number(666),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_ctor(self):
        ''' Parse variable declaration statement with constructor call. '''
        input_string = 'start := func () { p := Parser() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VariableDeclaration(
            name='p',
            expression=ast.FunctionCall(
                expression=ast.Identifier('Parser'),
                argument_list=[],
            ),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_init_2(self):
        ''' Parse variable declaration statement with
            complex initiaization.
        '''
        input_string = 'start := func () { v2 := plus(1 2) }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VariableDeclaration(
            name='v2',
            expression=ast.FunctionCall(
                expression=ast.Identifier('plus'),
                argument_list=[ast.Number(1), ast.Number(2)],
            ),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_ctor_and_arguments(self):
        ''' Parse variable declaration statement with
            constructor call with arguments.
        '''
        input_string = 'start := func () { p := Parser(lexer 1) }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.VariableDeclaration(
                name='p',
                expression=ast.FunctionCall(
                    expression=ast.Identifier('Parser'),
                    argument_list=[
                        ast.Identifier('lexer'),
                        ast.Number(1),
                    ],
                ),
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_if(self):
        ''' Parse if statement. '''
        input_string = 'start := func () { if 1 {} }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.If(
                condition=ast.Number(1),
                branch_if=[],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_if_else(self):
        ''' Parse if-else statement. '''
        input_string = 'start := func () { if 1 {} else {} }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.If(
                condition=ast.Number(1),
                branch_if=[],
                branch_else=[],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_nested_func_call_1(self):
        ''' Parse nested function call. '''
        input_string = 'start := func () { a()() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.FunctionCall(
                expression=ast.FunctionCall(
                    expression=ast.Identifier('a'),
                    argument_list=[],
                ),
                argument_list=[],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_return_1(self):
        ''' Parse return statement with integer. '''
        input_string = 'start := func () { return 1 }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.Return(expression=ast.Number(1)),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_return_2(self):
        ''' Parse return statement without any value. '''
        input_string = 'start := func () { return }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.Return(expression=None),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_return_3(self):
        ''' Parse return statement with function call. '''
        input_string = 'start := func () { return x() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.Return(
                expression=ast.FunctionCall(
                    expression=ast.Identifier('x'),
                    argument_list=[],
                ),
            ),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_string(self):
        ''' Parse anythong with string. '''
        input_string = 'start := func () { return "hi" }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.Return(
                expression=ast.String('hi')),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_qualified_identifier_1(self):
        ''' Parse qualified identifier. '''
        input_string = 'start := func () { a.b() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.FunctionCall(
                expression=ast.QualifiedIdentifier(identifier_list=['a', 'b']),
                argument_list=[],
            ),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_qualified_identifier_2(self):
        ''' Parse longer qualified identifier. '''
        input_string = 'start := func () { a.b.c() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.FunctionCall(
                expression=ast.QualifiedIdentifier(
                    identifier_list=['a', 'b', 'c'],
                ),
                argument_list=[],
            ),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_lex_error(self):
        ''' Check lexer error reporting. '''
        input_string = 'start := <'
        self.assertRaisesRegexp(
            Exception,
            'Lexer error: Illegal character',
            self._parse,
            input_string,
        )

    def test_parse_error(self):
        ''' Check parser error reporting. '''
        input_string = 'start := func 666 () {}'
        self.assertRaisesRegexp(
            Exception,
            'Parser error: unexpected token',
            self._parse,
            input_string,
        )


class TestFindColumn(unittest.TestCase):
    ''' Test parse.find_column() function. '''

    def test_one_line(self):
        ''' Call find_column with one-line string. '''
        input_data = '1 2 3\n'
        pos = 3
        real_column = parse.find_column(input_data, pos)
        expected_column = 3
        misc.assert_equal(self, expected_column, real_column)

    def test_two_lines(self):
        ''' Call find_column with two-line string. '''
        input_data = (
            '1 2 3\n'
            '4 5 6\n'
        )
        pos = 8
        real_column = parse.find_column(input_data, pos)
        expected_column = 2
        misc.assert_equal(self, expected_column, real_column)

    def test_empty_string(self):
        ''' Call find_column with empty string. '''
        input_data = ''
        pos = 0
        real_column = parse.find_column(input_data, pos)
        expected_column = 0
        misc.assert_equal(self, expected_column, real_column)


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab: