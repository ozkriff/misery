# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test my_parser module. '''


import unittest
import ast
import misc
import copy
import my_parser


class TestParser(unittest.TestCase):
    ''' Test my_parser.make_parser() function. '''

    # TODO: Rename
    _std_module = ast.NodeModule(
        declaration_sequence=[
            ast.NodeFunctionDeclaration(
                name='fname',
                interface=ast.NodeFunctionInterface(parameter_list=[]),
                body=[],
            )
        ]
    )

    def test_empty_module(self):
        ''' Parse empty string. '''
        input_string = ''
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_empty_import(self):
        ''' Parse empty import statement. '''
        input_string = 'import{}'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            import_list=[],
            declaration_sequence=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_import(self):
        ''' Parse import statement. '''
        input_string = 'import{module1}'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            import_list=['module1'],
            declaration_sequence=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_import_2(self):
        ''' Parse import statement with two modules. '''
        input_string = 'import{module1 module2}'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            import_list=['module1', 'module2'],
            declaration_sequence=[],
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_type_declaration(self):
        ''' Parse type simple declaration. '''
        input_string = 'type MyInteger Integer'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeTypeDeclaration(
                    name='MyInteger',
                    type=ast.NodeIdentifier('Integer'),
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_struct_type_declaration(self):
        ''' Some test :) '''
        input_string = '''
            type MyStruct struct {
                field1 Int
                field2 Float
            }
        '''
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeTypeDeclaration(
                    name='MyStruct',
                    type=ast.NodeTypeStruct(
                        value=[
                            ast.NodeField(
                                name='field1',
                                type=ast.NodeIdentifier('Int'),
                            ),
                            ast.NodeField(
                                name='field2',
                                type=ast.NodeIdentifier('Float'),
                            )
                        ]
                    )
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_type_alias(self):
        ''' Some test :) '''
        input_string = 'type MyInteger Integer'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeTypeDeclaration(
                    name='MyInteger',
                    type=ast.NodeIdentifier('Integer'),
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_const_declaration(self):
        ''' Some test :) '''
        input_string = 'const importantIdentifier Integer = 10'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeConstDeclaration(
                    name='importantIdentifier',
                    type=ast.NodeIdentifier('Integer'),
                    expression=ast.NodeNumber(10),
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func(self):
        ''' Some test :) '''
        input_string = 'func testfunc2() {}'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='testfunc2',
                    interface=ast.NodeFunctionInterface(parameter_list=[]),
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_return_value(self):
        ''' Some test :) '''
        input_string = 'func testfunc2() -> Integer {}'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='testfunc2',
                    interface=ast.NodeFunctionInterface(
                        parameter_list=[],
                        return_type=ast.NodeIdentifier('Integer'),
                    ),
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_parameter(self):
        ''' Some test :) '''
        input_string = 'func testfunc(par ParType) {}'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        interface = ast.NodeFunctionInterface(
            parameter_list=[
                ast.NodeFormalParameter(
                    name='par',
                    type=ast.NodeIdentifier('ParType')
                )
            ],
        )
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='testfunc',
                    interface=interface,
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_2_parameters(self):
        ''' Some test :) '''
        input_string = 'func testfunc(par1 ParType, par2 ParType) {}'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        interface = ast.NodeFunctionInterface(
            parameter_list=[
                ast.NodeFormalParameter(
                    name='par1',
                    type=ast.NodeIdentifier('ParType'),
                ),
                ast.NodeFormalParameter(
                    name='par2',
                    type=ast.NodeIdentifier('ParType'),
                )
            ]
        )
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='testfunc',
                    interface=interface,
                    body=[],
                )
            ]
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_func_body_2_empty_blocks(self):
        ''' Some test :) '''
        input_string = 'func fname() { {} {} }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body = [[], []]
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_func_call(self):
        ''' Some test :) '''
        input_string = 'func fname() { fname2() }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        funccall = ast.NodeFunctionCall(
            expression=ast.NodeIdentifier('fname2'),
            argument_list=[],
        )
        expected_ast.declaration_sequence[0].body.append(funccall)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_without_initialization(self):
        ''' Some test :) '''
        input_string = 'func fname() { var testVar Integer }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.NodeVariableDeclaration(
            name='testVar',
            type=ast.NodeIdentifier('Integer'),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_type_and_initialization(self):
        ''' Some test :) '''
        input_string = 'func fname() { var testVar Integer = 666 }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.NodeVariableDeclaration(
            name='testVar',
            type=ast.NodeIdentifier('Integer'),
            expression=ast.NodeNumber(666),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_initialization(self):
        ''' Some test :) '''
        input_string = 'func fname() { var testVar = 666 }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.NodeVariableDeclaration(
            name='testVar',
            expression=ast.NodeNumber(666),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_ctor(self):
        ''' Some test :) '''
        input_string = 'func fname() { var p Parser() }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.NodeVariableDeclaration(
            name='p',
            type=ast.NodeIdentifier('Parser'),
            constructor_argument_list=[],
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_init_2(self):
        ''' Some test :) '''
        input_string = 'func fname() { var v2 Int = plus(1, 2) }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.NodeVariableDeclaration(
            name='v2',
            expression=ast.NodeFunctionCall(
                expression=ast.NodeIdentifier('plus'),
                argument_list=[ast.NodeNumber(1), ast.NodeNumber(2)],
            ),
            type=ast.NodeIdentifier('Int'),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_ctor_and_arguments(self):
        ''' Some test :) '''
        input_string = 'func fname() { var p Parser(lexer, 1) }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeVariableDeclaration(
                name='p',
                type=ast.NodeIdentifier('Parser'),
                constructor_argument_list=[
                    ast.NodeIdentifier('lexer'),
                    ast.NodeNumber(1),
                ],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_if(self):
        ''' Some test :) '''
        input_string = 'func fname() { if 1 {} }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeIf(
                condition=ast.NodeNumber(1),
                branch_if=[],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_if_else(self):
        ''' Some test :) '''
        input_string = 'func fname() { if 1 {} else {} }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeIf(
                condition=ast.NodeNumber(1),
                branch_if=[],
                branch_else=[],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_nested_func_call_1(self):
        ''' Some test :) '''
        input_string = 'func fname() { a()() }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeFunctionCall(
                expression=ast.NodeFunctionCall(
                    expression=ast.NodeIdentifier('a'),
                    argument_list=[],
                ),
                argument_list=[],
            )
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_return_1(self):
        ''' Some test :) '''
        input_string = 'func fname() { return 1 }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeReturn(expression=ast.NodeNumber(1)),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_return_2(self):
        ''' Some test :) '''
        input_string = 'func fname() { return }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeReturn(expression=None),
        )
        misc.assert_equal(self, expected_ast, real_ast)

    def test_simple_return_3(self):
        ''' Some test :) '''
        input_string = 'func fname() { return x() }'
        real_ast = my_parser.make_parser().parse(
            input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeReturn(
                expression=ast.NodeFunctionCall(
                    expression=ast.NodeIdentifier('x'),
                    argument_list=[],
                ),
            ),
        )
        misc.assert_equal(self, expected_ast, real_ast)


# TODO: Why +1?
class TestFindColumn(unittest.TestCase):
    ''' Test my_parser.find_column() function. '''

    def test_simple(self):
        ''' Basic test. '''
        input_data = '1 2 3\n'
        pos = 3
        real_column = my_parser.find_column(input_data, pos)
        expected_column = 4
        misc.assert_equal(self, expected_column, real_column)

    def test_simple_multiline(self):
        ''' Basic test. '''
        input_data = (
            '1 2 3\n'
            '4 5 6\n'
        )
        pos = 8
        real_column = my_parser.find_column(input_data, pos)
        expected_column = 4
        misc.assert_equal(self, expected_column, real_column)

    def test_no_newline(self):
        ''' Basic test. '''
        input_data = ''
        pos = 0
        real_column = my_parser.find_column(input_data, pos)
        expected_column = 1
        misc.assert_equal(self, expected_column, real_column)


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
