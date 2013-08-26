# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'generator' module. '''


import unittest
import ast
import misc
import generator
import textwrap
import datatype


def check_translation(test_case, input_ast, expected_output):
    ''' Small helper function. '''
    marked_out_ast = datatype.mark_out_datatypes(input_ast)
    generator_ = generator.Generator(marked_out_ast)
    real_output = generator_.generate()
    misc.assert_equal(test_case, textwrap.dedent(expected_output), real_output)


class TestGenerator(unittest.TestCase):

    def test_1(self):
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                declaration_sequence=[
                    ast.FunctionDeclaration(
                        name='start',
                        interface=ast.FunctionInterface(parameter_list=[]),
                        body=[
                            ast.FunctionCall(
                                expression=ast.Identifier('printInteger'),
                                argument_list=[ast.Number(1)],
                            ),
                        ]
                    )
                ]
            ),
            expected_output='''
                void start(void);

                void start(void) {

                  printInteger(1);
                }

            ''',
        )

    def test_2(self):
        body = [
            ast.FunctionCall(
                expression=ast.Identifier('printInteger'),
                argument_list=[
                    ast.FunctionCall(
                        expression=ast.Identifier('plusInteger'),
                        argument_list=[ast.Number(1), ast.Number(2)],
                    ),
                ],
            ),
        ]
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                declaration_sequence=[
                    ast.FunctionDeclaration(
                        name='start',
                        interface=ast.FunctionInterface(parameter_list=[]),
                        body=body,
                    )
                ]
            ),
            expected_output='''
                void start(void);

                void start(void) {
                  Int tmp_0;

                  plusInteger(&tmp_0, 1, 2);
                  printInteger(tmp_0);
                }

            ''',
        )

    def test_3(self):
        body = [
            ast.FunctionCall(
                expression=ast.Identifier('printInteger'),
                argument_list=[
                    ast.FunctionCall(
                        expression=ast.Identifier('plusInteger'),
                        argument_list=[
                            ast.Number(1),
                            ast.FunctionCall(
                                expression=ast.Identifier('plusInteger'),
                                argument_list=[
                                    ast.Number(2),
                                    ast.Number(3),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                declaration_sequence=[
                    ast.FunctionDeclaration(
                        name='start',
                        interface=ast.FunctionInterface(parameter_list=[]),
                        body=body,
                    )
                ]
            ),
            expected_output='''
                void start(void);

                void start(void) {
                  Int tmp_1;
                  Int tmp_0;

                  plusInteger(&tmp_0, 2, 3);
                  plusInteger(&tmp_1, 1, tmp_0);
                  printInteger(tmp_1);
                }

            ''',
        )


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
