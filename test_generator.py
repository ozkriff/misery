# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'generator' module. '''


import unittest
import ast
import misc
import generator
import table


class TestGenerator(unittest.TestCase):
    ''' Test 'Generator' class. '''

    def test_nested_func_calls(self):
        ''' Generate nested function calls. '''
        ast_ = ast.Module(
            import_list=[],
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='main',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.FunctionCall(
                            expression=ast.Identifier('a'),
                            argument_list=[
                                ast.FunctionCall(
                                    expression=ast.Identifier('b'),
                                    argument_list=[]
                                ),
                            ]
                        ),
                    ]
                )
            ]
        )
        gen = generator.Generator(
            table=table.Table.from_ast(ast_),
        )
        real_output = gen.generate()
        expected_output = (
            '\n'
            'void main(void);\n'
            '\n'
            'void main(void) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '\n'
            '  b(&tmp_1);\n'
            '  a(&tmp_0, tmp_1);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_2(self):
        ''' Generate some simple code. '''
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='f1',
                    interface=ast.FunctionInterface(
                        parameter_list=[
                            ast.Parameter(
                                name='a',
                                datatype=ast.Identifier('int')
                            ),
                            ast.Parameter(
                                name='b',
                                datatype=ast.Identifier('int')
                            ),
                        ],
                        return_type=ast.Identifier('int'),
                    ),
                    body=[]
                ),
            ]
        )
        gen = generator.Generator(
            table=table.Table.from_ast(ast_),
        )
        # print('\n' + my_pretty_print(gen))
        real_output = gen.generate()
        expected_output = (
            '\n'
            'void f1(int* __result, int a, int b);\n'
            '\n'
            'void f1(int* __result, int a, int b) {\n'
            '\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_if(self):
        ''' Test if. '''
        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
            constant_list=[],
            variable_list=[
                table.Variable(datatype='int', name='tmp_0'),
                table.Variable(datatype='int', name='tmp_1'),
            ],
            block_list=[
                [
                    table.IfStatement(
                        expression_id=table.LinkToFunctionCall(id=0),
                        if_branch_id=1,
                    ),
                ],
                [
                    table.FunctionCallStatement(
                        expression_id=table.LinkToFunctionCall(id=1)),
                    table.FunctionCallStatement(
                        expression_id=table.LinkToFunctionCall(id=2)),
                ],
            ],
            expression_list=[
                table.FunctionCallExpression(
                    result_id=table.LinkToVariable(id=0),
                    name='f1',
                    argument_id_list=[],
                ),
                table.FunctionCallExpression(
                    result_id=table.LinkToVariable(id=1),
                    name='f2',
                    argument_id_list=[],
                ),
                table.FunctionCallExpression(
                    result_id=table.LinkToVariable(id=1),
                    name='f3',
                    argument_id_list=[],
                ),
            ]
        )
        table_ = table.Table(
            declaration_list=[func],
            identifier_list=[],
            import_list=[],
        )

        gen = generator.Generator(table=table_)
        real_output = gen.generate()
        expected_output = (
            '\n'
            'void main(void);\n'
            '\n'
            'void main(void) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '\n'
            '  f1(&tmp_0);\n'
            '  if (tmp_0) {\n'
            '    f2(&tmp_1);\n'
            '    f3(&tmp_1);\n'
            '  }\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_return_integer_constant(self):
        ''' Test returning integer constant. '''
        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
            constant_list=[
                table.Constant(datatype="int", value=1),
            ],
            variable_list=[],
            block_list=[
                [
                    table.ReturnStatement(
                        expression_id=table.LinkToNumberConstant(id=0),
                    ),
                ],
            ],
            expression_list=[],
        )
        table_ = table.Table(
            declaration_list=[func],
            identifier_list=[],
            import_list=[],
        )

        gen = generator.Generator(table=table_)
        real_output = gen.generate()
        expected_output = (
            '\n'
            'void main(void);\n'
            '\n'
            'void main(void) {\n'
            '\n'
            '  *__result = 1;\n'
            '  return;\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_return_function_call_result(self):
        ''' Test returning function call result. '''
        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
            constant_list=[],
            variable_list=[
                table.Variable(datatype='int', name='tmp_0'),
            ],
            block_list=[
                [
                    table.ReturnStatement(
                        expression_id=table.LinkToFunctionCall(id=0)),
                ],
            ],
            expression_list=[
                table.FunctionCallExpression(
                    result_id=table.LinkToVariable(id=0),
                    name='f',
                    argument_id_list=[],
                ),
            ],
        )
        table_ = table.Table(
            declaration_list=[func],
            identifier_list=[],
            import_list=[],
        )

        gen = generator.Generator(table=table_)
        real_output = gen.generate()
        expected_output = (
            '\n'
            'void main(void);\n'
            '\n'
            'void main(void) {\n'
            '  int tmp_0;\n'
            '\n'
            '  f(&tmp_0);\n'
            '  *__result = tmp_0;\n'
            '  return;\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
