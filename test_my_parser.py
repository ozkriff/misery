# -*- coding: utf-8 -*-

import unittest
import ast
import misc
import copy
import my_parser

class TestParser(unittest.TestCase):

    # TODO: Rename
    _std_module = ast.NodeModule(
        declaration_sequence=[
            ast.NodeFunctionDeclaration(
                name='fname',
                interface=ast.NodeFunctionInterface(),
                body=[],
            )
        ]
    )

    def test_empty_module(self):
        input_string = ''
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[],
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_empty_import(self):
        input_string = 'import{}'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            import_list=[],
            declaration_sequence=[],
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_import(self):
        input_string = 'import{module1}'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            import_list=['module1'],
            declaration_sequence=[],
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_import_2(self):
        input_string = 'import{module1 module2}'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            import_list=['module1', 'module2'],
            declaration_sequence=[],
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_type_declaration(self):
        input_string = 'type MyInteger Integer'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeTypeDeclaration(
                    name='MyInteger',
                    type=ast.NodeIdentifier('Integer'),
                )
            ]
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_struct_type_declaration(self):
        input_string = '''
            type MyStruct struct {
                field1 Int
                field2 Float
            }
        '''
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
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
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_type_alias(self):
        input_string = 'type MyInteger Integer'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeTypeDeclaration(
                    name='MyInteger',
                    type=ast.NodeIdentifier('Integer'),
                )
            ]
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_const_declaration(self):
        input_string = 'const importantIdentifier Integer = 10'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeConstDeclaration(
                    name='importantIdentifier',
                    type=ast.NodeIdentifier('Integer'),
                    expression=ast.NodeNumber(10),
                )
            ]
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_func(self):
        input_string = 'func testfunc2() {}'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='testfunc2',
                    interface=ast.NodeFunctionInterface(),
                    body=[],
                )
            ]
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_return_value(self):
        input_string = 'func testfunc2() -> Integer {}'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='testfunc2',
                    interface=ast.NodeFunctionInterface(
                        return_type=ast.NodeIdentifier('Integer'),
                    ),
                    body=[],
                )
            ]
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_parameter(self):
        input_string = 'func testfunc(par ParType) {}'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
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
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_func_with_2_parameters(self):
        input_string = 'func testfunc(par1 ParType, par2 ParType) {}'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
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
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_func_body_2_empty_blocks(self):
        input_string = 'func fname() { {} {} }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body = [[], []]
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_func_call(self):
        input_string = 'func fname() { fname2() }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        funccall = ast.NodeFunctionCall(
            expression=ast.NodeIdentifier('fname2'),
            argument_list=[],
        )
        expected_ast.declaration_sequence[0].body.append(funccall)
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_without_initialization(self):
        input_string = 'func fname() { var testVar Integer }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.NodeVariableDeclaration(
            name='testVar',
            type=ast.NodeIdentifier('Integer'),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_type_and_initialization(self):
        input_string = 'func fname() { var testVar Integer = 666 }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.NodeVariableDeclaration(
            name='testVar',
            type=ast.NodeIdentifier('Integer'),
            expression=ast.NodeNumber(666),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_initialization(self):
        input_string = 'func fname() { var testVar = 666 }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.NodeVariableDeclaration(
            name='testVar',
            expression=ast.NodeNumber(666),
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_ctor(self):
        input_string = 'func fname() { var p Parser() }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        var = ast.NodeVariableDeclaration(
            name='p',
            type=ast.NodeIdentifier('Parser'),
            constructor_argument_list=[],
        )
        expected_ast.declaration_sequence[0].body.append(var)
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_init_2(self):
        input_string = 'func fname() { var v2 Int = plus(1, 2) }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
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
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_var_declaration_with_ctor_and_arguments(self):
        input_string = 'func fname() { var p Parser(lexer, 1) }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
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
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_if(self):
        input_string = 'func fname() { if 1 {} }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeIf(
                condition=ast.NodeNumber(1),
                branch_if=[],
            )
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_if_else(self):
        input_string = 'func fname() { if 1 {} else {} }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeIf(
                condition=ast.NodeNumber(1),
                branch_if=[],
                branch_else=[],
            )
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_nested_func_call_1(self):
        input_string = 'func fname() { a()() }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
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
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_return_1(self):
        input_string = 'func fname() { return 1 }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeReturn(expression=ast.NodeNumber(1)),
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_return_2(self):
        input_string = 'func fname() { return }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeReturn(expression=None),
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

    def test_simple_return_3(self):
        input_string = 'func fname() { return x() }'
        real_ast = my_parser.make_parser().parse(input_string, lexer=my_parser.make_lexer())
        expected_ast = copy.deepcopy(self._std_module)
        expected_ast.declaration_sequence[0].body.append(
            ast.NodeReturn(
                expression=ast.NodeFunctionCall(
                    expression=ast.NodeIdentifier('x'),
                ),
            ),
        )
        misc.my_assert_equal(self, expected_ast, real_ast)

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
