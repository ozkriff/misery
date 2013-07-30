# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'datatype' module. '''


import unittest
import misc
import ast
import datatype


class TestSetTypeMarks(unittest.TestCase):

    def test_simple_function_declaration(self):
        input_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[],
                )
            ]
        )
        expected_output = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[],
                )
            ]
        )
        datatype.set_datatype_marks(input_ast)
        real_output = input_ast
        misc.assert_equal(self, expected_output, real_output)

    def test_simple_integer_variable_declaration(self):
        input_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            name='testVar',
                            expression=ast.Number(666),
                        ),
                    ],
                )
            ]
        )
        expected_output = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            name='testVar',
                            expression=ast.Number(666),
                            datatype=datatype.SimpleDataType('int'),
                        ),
                    ],
                )
            ]
        )
        datatype.set_datatype_marks(input_ast)
        real_output = input_ast
        misc.assert_equal(self, expected_output, real_output)

    def test_integer_variable_declaration_with_plus_integer(self):
        input_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            name='testVar',
                            expression=ast.FunctionCall(
                                expression=ast.Identifier('plusInteger'),
                                argument_list=[
                                    ast.Number(1),
                                    ast.Number(2),
                                ],
                            ),
                        ),
                    ],
                )
            ]
        )
        expected_output = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            name='testVar',
                            expression=ast.FunctionCall(
                                expression=ast.Identifier('plusInteger'),
                                argument_list=[
                                    ast.Number(1),
                                    ast.Number(2),
                                ],
                            ),
                            datatype=datatype.SimpleDataType('int'),
                        ),
                    ],
                )
            ]
        )
        datatype.set_datatype_marks(input_ast)
        real_output = input_ast
        misc.assert_equal(self, expected_output, real_output)


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
