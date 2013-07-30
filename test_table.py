# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import unittest
import ast
import misc
import table


class TestTable(unittest.TestCase):
    ''' Test 'Table' class. '''

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
        table_ = table.Table.from_ast(ast_)
        real_output = table_

        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
            constant_list=[
                table.Constant(datatype='int', value=1),
                table.Constant(datatype='int', value=2),
            ],
            variable_list=[
                table.Variable(datatype='int', name='tmp_0'),
            ],
            block_list=[
                [
                    table.FunctionCallStatement(
                        expression_id=table.LinkToFunctionCall(id=0)),
                ]
            ],
            expression_list=[
                table.FunctionCallExpression(
                    result_id=table.LinkToVariable(id=0),
                    name='plus',
                    argument_id_list=[
                        table.LinkToNumberConstant(id=0),
                        table.LinkToNumberConstant(id=1),
                    ],
                ),
            ],
        )
        expected_output = table.Table(
            declaration_list=[func],
            identifier_list={
                'main': ast.FunctionInterface(parameter_list=[]),
            },
            import_list=[],
        )

        misc.assert_is_part_of(self, expected_output, real_output)

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
        table_ = table.Table.from_ast(ast_)
        real_output = table_

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
                    table.FunctionCallStatement(
                        expression_id=table.LinkToFunctionCall(id=0)),
                    table.FunctionCallStatement(
                        expression_id=table.LinkToFunctionCall(id=1)),
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
            ],
        )
        expected_output = table.Table(
            declaration_list=[func],
            identifier_list={
                'main': ast.FunctionInterface(parameter_list=[]),
            },
            import_list=[],
        )

        misc.assert_is_part_of(self, expected_output, real_output)

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
        table_ = table.Table.from_ast(ast_)
        real_output = table_

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
            ],
        )
        expected_output = table.Table(
            declaration_list=[func],
            identifier_list={
                'main': ast.FunctionInterface(parameter_list=[]),
            },
            import_list=[],
        )

        misc.assert_is_part_of(self, expected_output, real_output)

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
        table_ = table.Table.from_ast(ast_)
        real_output = table_

        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
            constant_list=[],
            variable_list=[],
            block_list=[
                [
                    table.ReturnStatement(
                        expression_id=None,
                    ),
                ],
            ],
            expression_list=[],
        )
        expected_output = table.Table(
            declaration_list=[func],
            identifier_list={
                'main': ast.FunctionInterface(parameter_list=[]),
            },
            import_list=[],
        )

        misc.assert_is_part_of(self, expected_output, real_output)

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
        table_ = table.Table.from_ast(ast_)
        real_output = table_

        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
            constant_list=[
                table.Constant(datatype="int", value=0)
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
        expected_output = table.Table(
            declaration_list=[func],
            identifier_list={
                'main': ast.FunctionInterface(parameter_list=[]),
            },
            import_list=[],
        )

        misc.assert_is_part_of(self, expected_output, real_output)


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
