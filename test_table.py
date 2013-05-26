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
        ast_ = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='f1',
                    interface=ast.NodeFunctionInterface(parameter_list=[]),
                    body=[
                        ast.NodeVariableDeclaration(
                            expression=ast.NodeNumber(1),
                            name='a',
                            type=ast.NodeIdentifier('int'),
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
        ast_ = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='main',
                    interface=ast.NodeFunctionInterface(
                        parameter_list=[]),
                    body=[
                        ast.NodeFunctionCall(
                            expression=ast.NodeIdentifier('plus'),
                            argument_list=[
                                ast.NodeNumber(1),
                                ast.NodeNumber(2),
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
            interface=ast.NodeFunctionInterface(
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
        ast_ = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='main',
                    interface=ast.NodeFunctionInterface(
                        parameter_list=[]),
                    body=[
                        ast.NodeFunctionCall(
                            expression=ast.NodeIdentifier('f1'),
                            argument_list=[],
                        ),
                        ast.NodeFunctionCall(
                            expression=ast.NodeIdentifier('f2'),
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
            interface=ast.NodeFunctionInterface(
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
        ast_ = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='main',
                    interface=ast.NodeFunctionInterface(
                        parameter_list=[]),
                    body=[
                        ast.NodeIf(
                            condition=ast.NodeFunctionCall(
                                expression=ast.NodeIdentifier('f1'),
                                argument_list=[],
                            ),
                            branch_if=[
                                ast.NodeFunctionCall(
                                    expression=ast.NodeIdentifier('f2'),
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
            interface=ast.NodeFunctionInterface(
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

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
