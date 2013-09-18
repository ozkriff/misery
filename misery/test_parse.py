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
    ''' Test parse.make_parser() func. '''

    # Standart module.
    # Usage:
    #   expected_ast = copy.deepcopy(self._std_module)
    #   <add specific detaild to expected_ast>
    _std_module = ast.Module(
        decl_list=[
            ast.FuncDecl(
                name='start',
                signature=ast.FuncSignature(par_list=[]),
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
            decl_list=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_empty_import(self):
        ''' Parse empty import stmt. '''
        input_string = 'import {}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            import_list=[],
            decl_list=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_import(self):
        ''' Parse import stmt. '''
        input_string = 'import {module1}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            import_list=['module1'],
            decl_list=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_import_2(self):
        ''' Parse import stmt with two modules. '''
        input_string = 'import {module1 module2}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            import_list=['module1', 'module2'],
            decl_list=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_struct_type_decl(self):
        ''' Parse struct type decl. '''
        input_string = (
            'MyStruct := struct {\n'
            '  field1: Int\n'
            '  field2: Float\n'
            '}\n'
        )
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            decl_list=[
                ast.StructDecl(
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

    def test_const_decl(self):
        ''' Parse constant decl. '''
        input_string = 'const importantIdent:Int := 10'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            decl_list=[
                ast.ConstDecl(
                    name='importantIdent',
                    datatype=datatype.SimpleDataType('Int'),
                    expr=ast.Number(10),
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func(self):
        ''' Parse minimal fnction decl. '''
        input_string = 'testfunc2 := func() {}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='testfunc2',
                    signature=ast.FuncSignature(par_list=[]),
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_return_value(self):
        ''' Parse func that returns Int. '''
        input_string = 'testfunc2 := func () -> Int {}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='testfunc2',
                    signature=ast.FuncSignature(
                        par_list=[],
                        return_type=datatype.SimpleDataType('Int'),
                    ),
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_parameter(self):
        ''' Parse func that takes one parameter. '''
        input_string = 'testfunc := func (par:ParType) {}'
        real_ast = self._parse(input_string)
        signature = ast.FuncSignature(
            par_list=[
                ast.Parameter(
                    name='par',
                    datatype=datatype.SimpleDataType('ParType')
                )
            ],
        )
        expected_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='testfunc',
                    signature=signature,
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_2_parameters(self):
        ''' Parse func that takes two parameters. '''
        input_string = 'testfunc := func (par1:ParType par2:ParType) {}'
        real_ast = self._parse(input_string)
        signature = ast.FuncSignature(
            par_list=[
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
            decl_list=[
                ast.FuncDecl(
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
        expected_ast.decl_list[0].body = [[], []]
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_call(self):
        ''' Parse simple func call. '''
        input_string = 'start := func () { fname2() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        funccall = ast.FuncCall(
            expr=ast.Ident('fname2'),
            arg_list=[],
        )
        expected_ast.decl_list[0].body.append(funccall)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_decl_without_initialization(self):
        ''' Parse var decl stmt. '''
        input_string = 'start := func () { testVar := Int() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VarDecl(
            name='testVar',
            expr=ast.FuncCall(
                expr=ast.Ident('Int'),
                arg_list=[],
            )
        )
        expected_ast.decl_list[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_decl_with_type_and_initialization(self):
        ''' Parse var decl stmt with initiaization. '''
        input_string = 'start := func () { testVar := Int(666) }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VarDecl(
            name='testVar',
            expr=ast.FuncCall(
                expr=ast.Ident('Int'),
                arg_list=[
                    ast.Number(666),
                ],
            ),
        )
        expected_ast.decl_list[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_decl_with_initialization(self):
        ''' Parse var decl stmt with
            initiaization and without explicit  type.
        '''
        input_string = 'start := func () { testVar := 666 }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VarDecl(
            name='testVar',
            expr=ast.Number(666),
        )
        expected_ast.decl_list[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_decl_with_ctor(self):
        ''' Parse var decl stmt with constructor call. '''
        input_string = 'start := func () { p := Parser() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VarDecl(
            name='p',
            expr=ast.FuncCall(
                expr=ast.Ident('Parser'),
                arg_list=[],
            ),
        )
        expected_ast.decl_list[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_decl_with_init_2(self):
        ''' Parse var decl stmt with
            complex initiaization.
        '''
        input_string = 'start := func () { v2 := plus(1 2) }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.VarDecl(
            name='v2',
            expr=ast.FuncCall(
                expr=ast.Ident('plus'),
                arg_list=[ast.Number(1), ast.Number(2)],
            ),
        )
        expected_ast.decl_list[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_decl_with_ctor_and_arguments(self):
        ''' Parse var decl stmt with
            constructor call with arguments.
        '''
        input_string = 'start := func () { p := Parser(lexer 1) }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.decl_list[0].body.append(
            ast.VarDecl(
                name='p',
                expr=ast.FuncCall(
                    expr=ast.Ident('Parser'),
                    arg_list=[
                        ast.Ident('lexer'),
                        ast.Number(1),
                    ],
                ),
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_if(self):
        ''' Parse if stmt. '''
        input_string = 'start := func () { if 1 {} }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.decl_list[0].body.append(
            ast.If(
                condition=ast.Number(1),
                branch_if=[],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_if_else(self):
        ''' Parse if-else stmt. '''
        input_string = 'start := func () { if 1 {} else {} }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.decl_list[0].body.append(
            ast.If(
                condition=ast.Number(1),
                branch_if=[],
                branch_else=[],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_nested_func_call_1(self):
        ''' Parse nested func call. '''
        input_string = 'start := func () { a()() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.decl_list[0].body.append(
            ast.FuncCall(
                expr=ast.FuncCall(
                    expr=ast.Ident('a'),
                    arg_list=[],
                ),
                arg_list=[],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_return_1(self):
        ''' Parse return stmt with integer. '''
        input_string = 'start := func () { return 1 }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.decl_list[0].body.append(
            ast.Return(expr=ast.Number(1)),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_return_2(self):
        ''' Parse return stmt without any value. '''
        input_string = 'start := func () { return }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.decl_list[0].body.append(
            ast.Return(expr=None),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_return_3(self):
        ''' Parse return stmt with func call. '''
        input_string = 'start := func () { return x() }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.decl_list[0].body.append(
            ast.Return(
                expr=ast.FuncCall(
                    expr=ast.Ident('x'),
                    arg_list=[],
                ),
            ),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_generic_func_1(self):
        ''' First test of generic funcs. '''
        input_string = 'testFunc := func <Int> () {}'
        real_ast = self._parse(input_string)
        expected_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='testFunc',
                    signature=ast.FuncSignature(
                        par_list=[],
                        generic_par_list=["Int"],
                    ),
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_string(self):
        ''' Parse anythong with string. '''
        input_string = 'start := func () { return "hi" }'
        real_ast = self._parse(input_string)
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.decl_list[0].body.append(
            ast.Return(
                expr=ast.String('hi')),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_lex_error(self):
        ''' Check lexer error reporting. '''
        input_string = 'start := &'
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
    ''' Test parse.find_column() func. '''

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
