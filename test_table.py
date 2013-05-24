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
        func.statement_list = [
            table.FunctionCallStatement(
                expression_id=table.LinkToFunctionCall(id=0)),
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

    def test_if(self):
        ''' Test IF. '''
        ast_ = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='main',
                    interface=ast.NodeFunctionInterface(parameter_list=[]),
                    body=[
                        ast.NodeIf(
                            condition=ast.NodeNumber(1),
                            branch_if=[
                            ],
                        ),
                    ]
                )
            ]
        )
        table.Table().generate_tables(ast_)
        # print('\n' + my_pretty_print(t))
        # g = Generator()
        # g.table = t
        # real_output = g.generate()
        # expected_output = (
        #     '\n'
        #     'void main();\n'
        #     '\n'
        #     'void main() {\n'
        #     '  int tmp_0;\n'
        #     '\n'
        #     '  plus(&tmp_0, 1, 2);\n'
        #     '}\n'
        #     '\n'
        # )
        # misc.assert_equal(self, expected_output, real_output)

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
