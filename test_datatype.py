# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'datatype' module. '''


import unittest
import misc
import ast
import datatype


class TestMarkOutDatatypes(unittest.TestCase):

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
        real_output = datatype.mark_out_datatypes(input_ast)
        misc.assert_equal(self, expected_output, real_output)

    def test_copy(self):
        input_ast = ast.Module(
            declaration_sequence=[],
        )
        real_output = datatype.mark_out_datatypes(input_ast)
        # change original data
        input_ast.declaration_sequence.append('hi')
        self.assertEquals(len(real_output.declaration_sequence), 0)

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
                            datatype=datatype.SimpleDataType('Int'),
                        ),
                    ],
                )
            ]
        )
        real_output = datatype.mark_out_datatypes(input_ast)
        misc.assert_equal(self, expected_output, real_output)

    def test_integer_variable_declaration_with_plus_integer(self):
        int_data_type = datatype.SimpleDataType('Int'),
        std_identifier_list = {
            'plusInteger': ast.FunctionInterface(
                return_type=datatype.SimpleDataType('Int'),
                parameter_list=[
                    ast.Parameter(name='a', datatype=int_data_type),
                    ast.Parameter(name='b', datatype=int_data_type),
                ],
            ),
        }
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
        input_ast.identifier_list = std_identifier_list
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
                            datatype=datatype.SimpleDataType('Int'),
                        ),
                    ],
                )
            ]
        )
        expected_output.identifier_list = std_identifier_list
        real_output = datatype.mark_out_datatypes(input_ast)
        misc.assert_equal(self, expected_output, real_output)

    def test_bad_func_error(self):
        input_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            name='testVar',
                            expression=ast.FunctionCall(
                                expression=ast.Identifier('badFuncName'),
                                argument_list=[],
                            ),
                        ),
                    ],
                )
            ]
        )
        input_ast.identifier_list = {}
        self.assertRaisesRegexp(
            Exception,
            'no function: \'badFuncName\'',
            datatype.mark_out_datatypes,
            input_ast,
        )

    def test_bad_expression_type_error(self):
        class BadExpressionClass(object):
            pass
        input_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            name='testVar',
                            expression=BadExpressionClass(),
                        ),
                    ],
                )
            ]
        )
        self.assertRaisesRegexp(
            Exception,
            'Bad type:.*BadExpressionClass',
            datatype.mark_out_datatypes,
            input_ast,
        )

    def test_bad_statement_type_error(self):
        class BadStatementClass(object):
            pass
        input_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        BadStatementClass(),
                    ],
                )
            ]
        )
        self.assertRaisesRegexp(
            Exception,
            'Bad type:.*BadStatementClass',
            datatype.mark_out_datatypes,
            input_ast,
        )

    def test_bad_declaration_type_error(self):
        class BadDeclarationClass(object):
            pass
        input_ast = ast.Module(
            declaration_sequence=[
                BadDeclarationClass(),
            ]
        )
        self.assertRaisesRegexp(
            Exception,
            'Bad type:.*BadDeclarationClass',
            datatype.mark_out_datatypes,
            input_ast,
        )


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
