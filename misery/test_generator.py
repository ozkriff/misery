# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'generator' module. '''


import unittest
import textwrap
from misery import (
    ast,
    misc,
    generator,
    datatype,
    identifier_table,
)


def check_translation(test_case, input_ast, expected_output):
    ''' Small helper function. '''
    input_ast.identifier_list = identifier_table.identifier_table(input_ast)
    generator.scan_vars(input_ast)
    generator_ = generator.Generator(input_ast)
    real_output = generator_.generate()
    misc.assert_equal(test_case, textwrap.dedent(expected_output), real_output)


class TestGenerator(unittest.TestCase):

    def test_print_int_constant(self):
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                declaration_sequence=[
                    ast.FunctionDeclaration(
                        name='start',
                        signature=ast.FunctionSignature(
                            parameter_list=[],
                        ),
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

    def test_print_plus_int_result(self):
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
                        signature=ast.FunctionSignature(parameter_list=[]),
                        body=body,
                    )
                ]
            ),
            expected_output='''
                void start(void);

                void start(void) {
                  Int tmp_0;
                  Int const_0;
                  Int const_1;

                  const_0 = 1;
                  const_1 = 2;

                  plusInt(&tmp_0, &const_0, &const_1);
                  printInt(&tmp_0);
                }

            ''',
        )

    def test_print_result_of_nested_calls(self):
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
                        signature=ast.FunctionSignature(parameter_list=[]),
                        body=body,
                    )
                ]
            ),
            expected_output='''
                void start(void);

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;
                  Int const_0;
                  Int const_1;
                  Int const_2;

                  const_0 = 1;
                  const_1 = 2;
                  const_2 = 3;

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
                        signature=ast.FunctionSignature(
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
                        signature=ast.FunctionSignature(parameter_list=[]),
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
                  Int const_0;
                  Int const_1;

                  const_0 = 1;
                  const_1 = 2;

                  testFunc(&const_0, &const_1);
                }

            ''',
        )

    def test_bad_constant_type_error(self):
        class BadConstantClass(object):
            def __init__(self):
                pass
        input_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    signature=ast.FunctionSignature(parameter_list=[]),
                    body=[],
                )
            ]
        )
        constants = input_ast.declaration_sequence[0].constants  # shortcut
        constants['badConst'] = BadConstantClass()
        input_ast.identifier_list = {}
        generator_ = generator.Generator(input_ast)
        self.assertRaisesRegexp(
            Exception,
            'bad type:.*BadConstantClass',
            generator_.generate,
        )

    def test_bad_expression_type_error(self):
        class BadExpressionClass(object):
            def __init__(self):
                self.binded_variable_name = 'xxx'
        input_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    signature=ast.FunctionSignature(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            name='testVar',
                            expression=BadExpressionClass(),
                            datatype=datatype.SimpleDataType('Int'),
                        ),
                    ],
                )
            ]
        )
        input_ast.identifier_list = \
            identifier_table.identifier_table(input_ast)
        generator_ = generator.Generator(input_ast)
        self.assertRaisesRegexp(
            Exception,
            'Bad expression type:.*BadExpressionClass',
            generator_.generate,
        )

    def test_bad_declaration_type_error(self):
        class BadDeclarationClass(object):
            def __init__(self):
                pass
        input_ast = ast.Module(
            declaration_sequence=[
                BadDeclarationClass(),
            ],
        )
        input_ast.identifier_list = \
            identifier_table.identifier_table(input_ast)
        generator_ = generator.Generator(input_ast)
        self.assertRaisesRegexp(
            Exception,
            'Bad type:.*BadDeclarationClass',
            generator_.generate,
        )

    def test_bad_statement_type_error(self):
        class BadStatementClass(object):
            def __init__(self):
                pass
        input_ast = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='start',
                    signature=ast.FunctionSignature(parameter_list=[]),
                    body=[
                        BadStatementClass(),
                    ],
                )
            ]
        )
        input_ast.identifier_list = \
            identifier_table.identifier_table(input_ast)
        generator_ = generator.Generator(input_ast)
        self.assertRaisesRegexp(
            Exception,
            'Bad statement type:.*BadStatementClass',
            generator_.generate,
        )


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
