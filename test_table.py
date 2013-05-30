# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import unittest
import ast
import misc
import table


class TestTable(unittest.TestCase):
    ''' Test 'Table' class. '''

    def test_1(self):
        ''' Just generate some tables. '''
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='f1',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            expression=ast.Number(1),
                            name='a',
                            type=ast.Identifier('int'),
                        ),
                    ]
                ),
            ]
        )
        table.Table().generate_tables(ast_)
        # expected_tables = []
        # misc.assert_equal(self, expected_tables, real_tables)
        # print('\n' + my_pretty_print(t))

    def test_generate_function_call(self):
        ''' Generate table with simple function call. '''
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='main',
                    interface=ast.FunctionInterface(
                        parameter_list=[]),
                    body=[
                        ast.FunctionCall(
                            expression=ast.Identifier('plus'),
                            argument_list=[
                                ast.Number(1),
                                ast.Number(2),
                            ],
                        ),
                    ]
                )
            ]
        )
        table_ = table.Table()
        table_.generate_tables(ast_)
        real_output = table_

        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
        )
        func.constant_list = [
            table.Constant(type='int', value=1),
            table.Constant(type='int', value=2),
        ]
        func.variable_list = [
            table.Variable(type='int', name='tmp_0'),
        ]
        func.block_list = [
            [
                table.FunctionCallStatement(
                    expression_id=table.LinkToFunctionCall(id=0)),
            ]
        ]
        func.expression_list = [
            table.FunctionCallExpression(
                result_id=table.LinkToVariable(id=0),
                name='plus',
                argument_id_list=[
                    table.LinkToNumberConstant(id=0),
                    table.LinkToNumberConstant(id=1),
                ],
            ),
        ]
        expected_output = table.Table()
        expected_output.declaration_list = [func]

        misc.assert_equal(self, expected_output, real_output)

    def test_blocks(self):
        ''' Generate table with simple function call. '''
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='main',
                    interface=ast.FunctionInterface(
                        parameter_list=[]),
                    body=[
                        ast.FunctionCall(
                            expression=ast.Identifier('f1'),
                            argument_list=[],
                        ),
                        ast.FunctionCall(
                            expression=ast.Identifier('f2'),
                            argument_list=[],
                        ),
                    ]
                )
            ]
        )
        table_ = table.Table()
        table_.generate_tables(ast_)
        real_output = table_

        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
        )
        func.constant_list = []
        func.variable_list = [
            table.Variable(type='int', name='tmp_0'),
            table.Variable(type='int', name='tmp_1'),
        ]
        func.block_list = [
            [
                table.FunctionCallStatement(
                    expression_id=table.LinkToFunctionCall(id=0)),
                table.FunctionCallStatement(
                    expression_id=table.LinkToFunctionCall(id=1)),
            ],
        ]
        func.expression_list = [
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
        ]
        expected_output = table.Table()
        expected_output.declaration_list = [func]

        misc.assert_equal(self, expected_output, real_output)

    def test_if(self):
        ''' Conditional expression. '''
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='main',
                    interface=ast.FunctionInterface(
                        parameter_list=[]),
                    body=[
                        ast.If(
                            condition=ast.FunctionCall(
                                expression=ast.Identifier('f1'),
                                argument_list=[],
                            ),
                            branch_if=[
                                ast.FunctionCall(
                                    expression=ast.Identifier('f2'),
                                    argument_list=[],
                                ),
                            ],
                        ),
                    ]
                )
            ]
        )
        table_ = table.Table()
        table_.generate_tables(ast_)
        real_output = table_

        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
        )
        func.constant_list = []
        func.variable_list = [
            table.Variable(type='int', name='tmp_0'),
            table.Variable(type='int', name='tmp_1'),
        ]
        func.block_list = [
            [
                table.IfStatement(
                    expression_id=table.LinkToFunctionCall(id=0),
                    if_branch_id=1,
                ),
            ],
            [
                table.FunctionCallStatement(
                    expression_id=table.LinkToFunctionCall(id=1)),
            ],
        ]
        func.expression_list = [
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
        ]
        expected_output = table.Table()
        expected_output.declaration_list = [func]

        misc.assert_equal(self, expected_output, real_output)

    def test_return_none(self):
        ''' Return from function. '''
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='main',
                    interface=ast.FunctionInterface(
                        parameter_list=[]),
                    body=[
                        ast.Return(expression=None),
                    ]
                )
            ]
        )
        table_ = table.Table()
        table_.generate_tables(ast_)
        real_output = table_

        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
        )
        func.constant_list = []
        func.variable_list = []
        func.block_list = [
            [
                table.ReturnStatement(
                    expression_id=None,
                ),
            ],
        ]
        func.expression_list = []
        expected_output = table.Table()
        expected_output.declaration_list = [func]

        misc.assert_equal(self, expected_output, real_output)

    def test_return_integer_constant(self):
        ''' Return integer constant from function. '''
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='main',
                    interface=ast.FunctionInterface(
                        parameter_list=[]),
                    body=[
                        ast.Return(expression=ast.Number(0)),
                    ]
                )
            ]
        )
        table_ = table.Table()
        table_.generate_tables(ast_)
        real_output = table_

        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
        )
        func.constant_list = [
            table.Constant(type="int", value=0)
        ]
        func.variable_list = []
        func.block_list = [
            [
                table.ReturnStatement(
                    expression_id=table.LinkToNumberConstant(id=0),
                ),
            ],
        ]
        func.expression_list = []
        expected_output = table.Table()
        expected_output.declaration_list = [func]

        misc.assert_equal(self, expected_output, real_output)

    def test_factorial(self):
        ''' Test table generation for simple factorial function. '''

        body = [
            ast.If(
                branch_if=[
                    ast.Return(expression=ast.Number(1)),
                ],
                condition=ast.FunctionCall(
                    expression=ast.Identifier('isEqualInteger'),
                    argument_list=[
                        ast.Identifier('n'),
                        ast.Number(0),
                    ],
                ),
            ),
            ast.Return(
                expression=ast.FunctionCall(
                    expression=ast.Identifier('multiplyInteger'),
                    argument_list=[
                        ast.FunctionCall(
                            expression=ast.Identifier('fac'),
                            argument_list=[
                                ast.FunctionCall(
                                    expression=ast.Identifier('minusInteger'),
                                    argument_list=[
                                        ast.Identifier('n'),
                                        ast.Number(1),
                                    ],
                                ),
                            ],
                        ),
                        ast.Identifier('n'),
                    ],
                ),
            ),
        ]
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='fac',
                    interface=ast.FunctionInterface(
                        return_type=ast.Identifier('int'),
                        parameter_list=[
                            ast.Parameter(
                                name='n',
                                type=ast.Identifier('int'),
                            ),
                        ],
                    ),
                    body=body,
                )
            ]
        )

        table_ = table.Table()
        table_.generate_tables(ast_)
        real_output = table_

        func = table.Function(
            name='fac',
            interface=ast.FunctionInterface(
                return_type=ast.Identifier('int'),
                parameter_list=[
                    ast.Parameter(
                        name='n',
                        type=ast.Identifier('int')
                    ),
                ],
            ),
        )
        func.constant_list = [
            table.Constant(type='int', value=0),
            table.Constant(type='int', value=1),
            table.Constant(type='int', value=1),
        ]
        func.variable_list = [
            table.Variable(name='tmp_0', type='int'),
            table.Variable(name='tmp_1', type='int'),
            table.Variable(name='tmp_2', type='int'),
            table.Variable(name='tmp_3', type='int'),
        ]
        func.block_list = [
            [
                table.IfStatement(
                    expression_id=table.LinkToFunctionCall(id=0),
                    if_branch_id=1,
                ),
            ],
            [
                table.ReturnStatement(
                    expression_id=table.LinkToNumberConstant(id=1),
                ),
                # TODO: next statement should be in previous block!
                table.ReturnStatement(
                    expression_id=table.LinkToFunctionCall(id=3),
                ),
            ],
        ]
        func.expression_list = [
            table.FunctionCallExpression(
                result_id=table.LinkToVariable(id=0),
                name='isEqualInteger',
                argument_id_list=[
                    table.LinkToParameter(name='n'),
                    table.LinkToNumberConstant(id=0),
                ],
            ),
            table.FunctionCallExpression(
                result_id=table.LinkToVariable(id=3),
                name='minusInteger',
                argument_id_list=[
                    table.LinkToParameter(name='n'),
                    table.LinkToNumberConstant(id=2),
                ],
            ),
            table.FunctionCallExpression(
                result_id=table.LinkToVariable(id=2),
                name='fac',
                argument_id_list=[
                    table.LinkToFunctionCall(id=1),
                ],
            ),
            table.FunctionCallExpression(
                result_id=table.LinkToVariable(id=1),
                name='multiplyInteger',
                argument_id_list=[
                    table.LinkToFunctionCall(id=2),
                    table.LinkToParameter(name='n'),
                ],
            ),
        ]
        expected_output = table.Table()
        expected_output.declaration_list = [func]

        misc.assert_equal(self, expected_output, real_output)


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
