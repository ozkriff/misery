# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'generator' module. '''


import unittest
import ast
import misc
import generator
import textwrap
import datatype
import identifier_table


def check_translation(test_case, input_ast, expected_output):
    ''' Small helper function. '''
    input_ast.identifier_list = identifier_table.identifier_table(input_ast)
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
                                expression=ast.Identifier('printInt'),
                                argument_list=[ast.Number(1)],
                            ),
                        ]
                    )
                ]
            ),
            expected_output='''
                void start(void);

                void start(void) {
                  Int const_0;

                  const_0 = 1;

                  printInt(&const_0);
                }

            ''',
        )

    def test_2(self):
        body = [
            ast.FunctionCall(
                expression=ast.Identifier('printInt'),
                argument_list=[
                    ast.FunctionCall(
                        expression=ast.Identifier('plusInt'),
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
                  Int const_1;
                  Int const_0;

                  const_1 = 2;
                  const_0 = 1;

                  plusInt(&tmp_0, &const_0, &const_1);
                  printInt(&tmp_0);
                }

            ''',
        )

    def test_3(self):
        body = [
            ast.FunctionCall(
                expression=ast.Identifier('printInt'),
                argument_list=[
                    ast.FunctionCall(
                        expression=ast.Identifier('plusInt'),
                        argument_list=[
                            ast.Number(1),
                            ast.FunctionCall(
                                expression=ast.Identifier('plusInt'),
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
                  Int const_2;
                  Int const_1;
                  Int const_0;

                  const_2 = 3;
                  const_1 = 2;
                  const_0 = 1;

                  plusInt(&tmp_0, &const_1, &const_2);
                  plusInt(&tmp_1, &const_0, &tmp_0);
                  printInt(&tmp_1);
                }

            ''',
        )

    def test_import_simple(self):
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                import_list=['module1', 'module2'],
                declaration_sequence=[],
            ),
            expected_output='''
                // import: module1
                // import: module2


            ''',
        )

    def test_generate_full(self):
        ''' Just generate something '''
        input_ast = ast.Module(
            import_list=[],
            declaration_sequence=[],
        )
        marked_out_ast = datatype.mark_out_datatypes(input_ast)
        generator_ = generator.Generator(marked_out_ast)
        real_output = generator_.generate_full()
        assert real_output != ''

    def test_multiply_function_parameters(self):
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                declaration_sequence=[
                    ast.FunctionDeclaration(
                        name='testFunc',
                        interface=ast.FunctionInterface(
                            parameter_list=[
                                ast.Parameter(
                                    name='n1',
                                    datatype=ast.Identifier('Int')
                                ),
                                ast.Parameter(
                                    name='n2',
                                    datatype=ast.Identifier('Int')
                                ),
                            ],
                        ),
                        body=[],
                    ),
                    ast.FunctionDeclaration(
                        name='start',
                        interface=ast.FunctionInterface(parameter_list=[]),
                        body=[
                            ast.FunctionCall(
                                expression=ast.Identifier('testFunc'),
                                argument_list=[ast.Number(1), ast.Number(2)],
                            ),
                        ]
                    )
                ]
            ),
            expected_output='''
                void testFunc(Int* n1, Int* n2);
                void start(void);

                void testFunc(Int* n1, Int* n2) {


                }

                void start(void) {
                  Int const_1;
                  Int const_0;

                  const_1 = 2;
                  const_0 = 1;

                  testFunc(&const_0, &const_1);
                }

            ''',
        )


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
