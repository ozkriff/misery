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
    ident_table,
)


def check_translation(test_case, input_ast, expected_output):
    ''' Small helper func. '''
    input_ast.ident_list = ident_table.ident_table(input_ast)
    input_ast = datatype.mark_out_datatypes(ast_=input_ast)
    generator_ = generator.Generator(input_ast)
    real_output = generator_.generate()
    misc.assert_equal(test_case, textwrap.dedent(expected_output), real_output)


class TestGenerator(unittest.TestCase):

    def test_print_int_constant(self):
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                decl_list=[
                    ast.FuncDecl(
                        name='start',
                        signature=ast.FuncSignature(),
                        body=[
                            ast.FuncCall(
                                expr=ast.Ident('print'),
                                arg_list=[ast.Number(1)],
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

                  print_Int(&const_0);
                }

            ''',
        )

    def test_print_plus_int_result(self):
        body = [
            ast.FuncCall(
                expr=ast.Ident('print'),
                arg_list=[
                    ast.FuncCall(
                        expr=ast.Ident('plus'),
                        arg_list=[ast.Number(1), ast.Number(2)],
                    ),
                ],
            ),
        ]
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                decl_list=[
                    ast.FuncDecl(
                        name='start',
                        signature=ast.FuncSignature(),
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

                  plus_Int_Int(&tmp_0, &const_0, &const_1);
                  print_Int(&tmp_0);
                }

            ''',
        )

    def test_print_result_of_nested_calls(self):
        body = [
            ast.FuncCall(
                expr=ast.Ident('print'),
                arg_list=[
                    ast.FuncCall(
                        expr=ast.Ident('plus'),
                        arg_list=[
                            ast.Number(1),
                            ast.FuncCall(
                                expr=ast.Ident('plus'),
                                arg_list=[
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
                decl_list=[
                    ast.FuncDecl(
                        name='start',
                        signature=ast.FuncSignature(),
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

                  plus_Int_Int(&tmp_0, &const_1, &const_2);
                  plus_Int_Int(&tmp_1, &const_0, &tmp_0);
                  print_Int(&tmp_1);
                }

            ''',
        )

    def test_import_simple(self):
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                import_list=['module1', 'module2'],
            ),
            expected_output='''
                // import: module1
                // import: module2


            ''',
        )

    def test_generate_full(self):
        ''' Just generate something '''
        input_ast = ast.Module()
        marked_out_ast = datatype.mark_out_datatypes(input_ast)
        generator_ = generator.Generator(marked_out_ast)
        real_output = generator_.generate_full()
        self.assertNotEqual('', real_output)

    def test_multiply_func_parameters(self):
        check_translation(
            test_case=self,
            input_ast=ast.Module(
                decl_list=[
                    ast.FuncDecl(
                        name='testFunc',
                        signature=ast.FuncSignature(
                            par_list=[
                                ast.Parameter(
                                    name='n1',
                                    datatype=ast.Ident('Int')
                                ),
                                ast.Parameter(
                                    name='n2',
                                    datatype=ast.Ident('Int')
                                ),
                            ],
                        ),
                    ),
                    ast.FuncDecl(
                        name='start',
                        signature=ast.FuncSignature(),
                        body=[
                            ast.FuncCall(
                                expr=ast.Ident('testFunc'),
                                arg_list=[ast.Number(1), ast.Number(2)],
                            ),
                        ]
                    )
                ]
            ),
            expected_output='''
                void testFunc_Int_Int(Int* n1, Int* n2);
                void start(void);

                void testFunc_Int_Int(Int* n1, Int* n2) {
                }

                void start(void) {
                  Int const_0;
                  Int const_1;

                  const_0 = 1;
                  const_1 = 2;

                  testFunc_Int_Int(&const_0, &const_1);
                }

            ''',
        )

    def test_bad_constant_type_error(self):
        class BadConstantClass(object):
            def __init__(self):
                pass
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(),
                )
            ]
        )
        constants = input_ast.decl_list[0].constants  # shortcut
        constants['badConst'] = BadConstantClass()
        input_ast.ident_list = {}
        generator_ = generator.Generator(input_ast)
        self.assertRaisesRegexp(
            Exception,
            'bad type:.*BadConstantClass',
            generator_.generate,
        )

    def test_bad_expr_type_error(self):
        class BadExprClass(object):
            def __init__(self):
                self.binded_var_name = 'xxx'
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(),
                    body=[
                        ast.VarDecl(
                            name='testVar',
                            expr=BadExprClass(),
                            datatype=datatype.SimpleDataType('Int'),
                        ),
                    ],
                )
            ]
        )
        input_ast.ident_list = \
            ident_table.ident_table(input_ast)
        generator_ = generator.Generator(input_ast)
        self.assertRaisesRegexp(
            Exception,
            'Bad expr type:.*BadExprClass',
            generator_.generate,
        )

    def test_bad_decl_type_error(self):
        class BadDeclClass(object):
            def __init__(self):
                pass
        input_ast = ast.Module(
            decl_list=[
                BadDeclClass(),
            ],
        )
        input_ast.ident_list = \
            ident_table.ident_table(input_ast)
        generator_ = generator.Generator(input_ast)
        self.assertRaisesRegexp(
            Exception,
            'Bad type:.*BadDeclClass',
            generator_.generate,
        )

    def test_bad_stmt_type_error(self):
        class BadStmtClass(object):
            def __init__(self):
                pass
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(),
                    body=[
                        BadStmtClass(),
                    ],
                )
            ]
        )
        input_ast.ident_list = \
            ident_table.ident_table(input_ast)
        generator_ = generator.Generator(input_ast)
        self.assertRaisesRegexp(
            Exception,
            'Bad stmt type:.*BadStmtClass',
            generator_.generate,
        )


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
