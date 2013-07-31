# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import unittest
import ast
import misc
import table
import datatype


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
                            expression=ast.Identifier('plusInteger'),
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
                table.Constant(
                    datatype=datatype.SimpleDataType('int'),
                    value=1,
                ),
                table.Constant(
                    datatype=datatype.SimpleDataType('int'),
                    value=2,
                ),
            ],
            variable_list=[
                table.Variable(
                    datatype=datatype.SimpleDataType('int'),
                    name='tmp_0',
                ),
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
                    name='plusInteger',
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
                            expression=ast.Identifier('printInteger'),
                            argument_list=[
                                ast.Number(1),
                            ],
                        ),
                        ast.FunctionCall(
                            expression=ast.Identifier('printInteger'),
                            argument_list=[
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
                table.Constant(
                    datatype=datatype.SimpleDataType('int'),
                    value=1,
                ),
                table.Constant(
                    datatype=datatype.SimpleDataType('int'),
                    value=2,
                ),
            ],
            variable_list=[],
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
                    result_id=None,
                    name='printInteger',
                    argument_id_list=[
                        table.LinkToNumberConstant(id=0),
                    ],
                ),
                table.FunctionCallExpression(
                    result_id=None,
                    name='printInteger',
                    argument_id_list=[
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

    def test_if(self):
        ''' Conditional expression. '''
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='main',
                    interface=ast.FunctionInterface(
                        parameter_list=[],
                    ),
                    body=[
                        ast.If(
                            condition=ast.FunctionCall(
                                expression=ast.Identifier('isLessInteger'),
                                argument_list=[
                                    ast.Number(0),
                                    ast.Number(1),
                                ],
                            ),
                            branch_if=[
                                ast.FunctionCall(
                                    expression=ast.Identifier('printInteger'),
                                    argument_list=[
                                        ast.Number(666),
                                    ],
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
            constant_list=[
                table.Constant(
                    datatype=datatype.SimpleDataType('int'),
                    value=0,
                ),
                table.Constant(
                    datatype=datatype.SimpleDataType('int'),
                    value=1,
                ),
                table.Constant(
                    datatype=datatype.SimpleDataType('int'),
                    value=666,
                ),
            ],
            variable_list=[
                table.Variable(
                    datatype=datatype.SimpleDataType('int'),
                    name='tmp_0',
                ),
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
                    name='isLessInteger',
                    argument_id_list=[
                        table.LinkToNumberConstant(id=0),
                        table.LinkToNumberConstant(id=1),
                    ],
                ),
                table.FunctionCallExpression(
                    result_id=None,
                    name='printInteger',
                    argument_id_list=[
                        table.LinkToNumberConstant(id=2),
                    ],
                ),
            ],
        )
        expected_output = table.Table(
            declaration_list=[func],
            identifier_list={
                'main': ast.FunctionInterface(parameter_list=[]),
            },
            import_list=None,
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
                table.Constant(
                    datatype=datatype.SimpleDataType('int'),
                    value=0,
                )
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
