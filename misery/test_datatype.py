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
                    signature=ast.FuncSignature(par_list=[]),
                    body=[],
                )
            ]
        )
        expected_output = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(par_list=[]),
                    body=[],
                )
            ]
        )
        real_output = datatype.mark_out_datatypes(input_ast)
        misc.assert_equal(self, expected_output, real_output)

    def test_copy(self):
        input_ast = ast.Module(
            decl_list=[],
        )
        real_output = datatype.mark_out_datatypes(input_ast)
        # change original data
        input_ast.decl_list.append('hi')
        self.assertEquals(len(real_output.decl_list), 0)

    def test_simple_integer_var_decl(self):
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(par_list=[]),
                    body=[
                        ast.VarDecl(
                            name='testVar',
                            expr=ast.Number(666),
                        ),
                    ],
                )
            ]
        )
        expected_output = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(par_list=[]),
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
        real_output = datatype.mark_out_datatypes(input_ast)
        misc.assert_equal(self, expected_output, real_output)

    def test_integer_var_decl_with_plus_integer(self):
        int_data_type = datatype.SimpleDataType('Int'),
        std_ident_list = {
            'plusInt': ast.FuncSignature(
                return_type=datatype.SimpleDataType('Int'),
                par_list=[
                    ast.Parameter(name='a', datatype=int_data_type),
                    ast.Parameter(name='b', datatype=int_data_type),
                ],
            ),
        }
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(par_list=[]),
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
        expected_output = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(par_list=[]),
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
                            datatype=datatype.SimpleDataType('Int'),
                        ),
                    ],
                )
            ]
        )
        expected_output.ident_list = std_ident_list
        real_output = datatype.mark_out_datatypes(input_ast)
        misc.assert_equal(self, expected_output, real_output)

    def test_bad_func_error(self):
        input_ast = ast.Module(
            decl_list=[
                ast.FuncDecl(
                    name='start',
                    signature=ast.FuncSignature(par_list=[]),
                    body=[
                        ast.VarDecl(
                            name='testVar',
                            expr=ast.FuncCall(
                                expr=ast.Ident('badFuncName'),
                                arg_list=[],
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
                    signature=ast.FuncSignature(par_list=[]),
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
                    signature=ast.FuncSignature(par_list=[]),
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
