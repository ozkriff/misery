# -*- coding: utf-8 -*-


import unittest
import ast
import misc
import table
import generator  # TODO: table should not depend on generator!!!


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

    def test_2(self):
        ''' bla bla bla. '''
        ast_ = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='main',
                    interface=ast.NodeFunctionInterface(parameter_list=[]),
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
        gen = generator.Generator()
        gen.table = table_
        real_output = gen.generate()
        expected_output = (
            '\n'
            'void main();\n'
            '\n'
            'void main() {\n'
            '  int tmp_0;\n'
            '\n'
            '  plus(&tmp_0, 1, 2);\n'
            '}\n'
            '\n'
        )
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
