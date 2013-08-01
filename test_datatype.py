# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'datatype' module. '''


from unittest import TestCase
from misc import assert_is_part_of
import ast
from datatype import mark_out_datatypes, SimpleDataType


class TestMarkOutDatatypes(TestCase):

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
        real_output = mark_out_datatypes(input_ast)
        assert_is_part_of(self, expected_output, real_output)

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
                            datatype=SimpleDataType('Int'),
                        ),
                    ],
                )
            ]
        )
        real_output = mark_out_datatypes(input_ast)
        assert_is_part_of(self, expected_output, real_output)

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
                            datatype=SimpleDataType('Int'),
                        ),
                    ],
                )
            ]
        )
        real_output = mark_out_datatypes(input_ast)
        assert_is_part_of(self, expected_output, real_output)


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
