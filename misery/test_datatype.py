# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'datatype' module. '''


import unittest
from misery import (
    misc,
    ast,
    datatype,
)


class TestMarkOutDatatypes(unittest.TestCase):

    def test_simple_func_decl(self):
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(),
                )
            ]
        )
        expected_output = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(),
                )
            ]
        )
        real_output = datatype.mark_out_datatypes(input_ast)
        misc.assert_equal(self, expected_output, real_output)

    def test_copy(self):
        input_ast = ast.Module()
        real_output = datatype.mark_out_datatypes(input_ast)
        # change original data
        input_ast.decl_list.append('hi')
        self.assertEquals(len(real_output.decl_list), 0)

    def test_simple_integer_var_decl(self):
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(),
                    body=[
                        ast.VarDecl(
                            name='testVar',
                            expr=ast.Number(666),
                        ),
                    ],
                )
            ]
        )

        def get_expected_output():
            expected_output = ast.Module(
                decl_list=[
                    ast.FuncDecl(
                        name='start',
                        signature=ast.FuncSignature(),
                        body=[
                            ast.VarDecl(
                                name='testVar',
                                expr=ast.Number(666),
                                datatype=datatype.SimpleDataType('Int'),
                            ),
                        ],
                    )
                ]
            )
            expected_start_func = expected_output.decl_list[0]
            expected_start_func.constants = {
                'const_0': ast.Number(value=666),
            }
            expected_start_func.vars = {
                'testVar': datatype.SimpleDataType('Int'),
            }
            var_decl = expected_start_func.body[0]
            var_decl.rvalue_expr.binded_var_name = 'const_0'
            return expected_output

        expected_output = get_expected_output()
        real_output = datatype.mark_out_datatypes(input_ast)
        misc.assert_equal(self, expected_output, real_output)

    def test_integer_var_decl_with_plus_integer(self):
        int_data_type = datatype.SimpleDataType('Int')
        std_ident_list = {
            'plusInt': ast.FuncSignature(
                return_type=datatype.SimpleDataType('Int'),
                param_list=[
                    ast.Param(name='a', datatype=int_data_type),
                    ast.Param(name='b', datatype=int_data_type),
                ],
            ),
        }
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(),
                    body=[
                        ast.VarDecl(
                            name='testVar',
                            expr=ast.FuncCall(
                                expr=ast.Ident('plusInt'),
                                arg_list=[
                                    ast.Number(1),
                                    ast.Number(2),
                                ],
                            ),
                        ),
                    ],
                )
            ]
        )
        input_ast.ident_list = std_ident_list

        def get_expected_output():
            expected_output = ast.Module(
                decl_list=[
                    ast.FuncDecl(
                        name='start',
                        signature=ast.FuncSignature(),
                        body=[
                            ast.VarDecl(
                                name='testVar',
                                expr=ast.FuncCall(
                                    expr=ast.Ident('plusInt'),
                                    arg_list=[
                                        ast.Number(1),
                                        ast.Number(2),
                                    ],
                                ),
                                datatype=int_data_type,
                            ),
                        ],
                    ),
                ]
            )
            expected_start_func = expected_output.decl_list[0]
            expected_start_func.constants = {
                'const_0': ast.Number(value=1),
                'const_1': ast.Number(value=2),
            }
            expected_start_func.tmp_vars = {
                'tmp_0': int_data_type,
            }
            expected_start_func.vars = {
                'testVar': int_data_type,
            }
            var_decl = expected_start_func.body[0]
            var_decl.rvalue_expr.binded_var_name = 'tmp_0'
            arg_list = var_decl.rvalue_expr.arg_list
            arg_list[0].binded_var_name = 'const_0'
            arg_list[1].binded_var_name = 'const_1'
            expected_output.ident_list = std_ident_list
            return expected_output

        expected_output = get_expected_output()
        real_output = datatype.mark_out_datatypes(input_ast)
        misc.assert_equal(self, expected_output, real_output)

    def test_bad_func_error(self):
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(),
                    body=[
                        ast.VarDecl(
                            name='testVar',
                            expr=ast.FuncCall(
                                expr=ast.Ident('badFuncName'),
                            ),
                        ),
                    ],
                )
            ]
        )
        input_ast.ident_list = {}
        self.assertRaisesRegexp(
            Exception,
            'no func: \'badFuncName\'',
            datatype.mark_out_datatypes,
            input_ast,
        )

    def test_bad_expr_type_error(self):
        class BadExprClass(object):
            pass
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(),
                    body=[
                        ast.VarDecl(
                            name='testVar',
                            expr=BadExprClass(),
                        ),
                    ],
                )
            ]
        )
        self.assertRaisesRegexp(
            Exception,
            'Bad type:.*BadExprClass',
            datatype.mark_out_datatypes,
            input_ast,
        )

    def test_bad_stmt_type_error(self):
        class BadStmtClass(object):
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
        self.assertRaisesRegexp(
            Exception,
            'Bad type:.*BadStmtClass',
            datatype.mark_out_datatypes,
            input_ast,
        )

    def test_bad_decl_type_error(self):
        class BadDeclClass(object):
            pass
        input_ast = ast.Module(
            decl_list=[
                BadDeclClass(),
            ]
        )
        self.assertRaisesRegexp(
            Exception,
            'Bad type:.*BadDeclClass',
            datatype.mark_out_datatypes,
            input_ast,
        )


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
