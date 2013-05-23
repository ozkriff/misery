# -*- coding: utf-8 -*-


import unittest
import ast
import misc
import generator
import table


class TestGenerator(unittest.TestCase):

    def test_1(self):
        ast_ = ast.NodeModule(
            import_list=['stdio', 'ogre3d'],
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='f1',
                    interface=ast.NodeFunctionInterface(parameter_list=[]),
                    body=[
                        ast.NodeVariableDeclaration(
                            expression=ast.NodeFunctionCall(
                                expression=ast.NodeIdentifier('plus'),
                                argument_list=[
                                    ast.NodeNumber(1),
                                    ast.NodeNumber(2),
                                ]
                            ),
                            name='a',
                            type=ast.NodeIdentifier('int'),
                        ),
                    ]
                ),
                ast.NodeFunctionDeclaration(
                    name='f2',
                    interface=ast.NodeFunctionInterface(parameter_list=[]),
                    body=[
                        ast.NodeVariableDeclaration(
                            expression=ast.NodeFunctionCall(
                                expression=ast.NodeIdentifier('x'),
                                argument_list=[]
                            ),
                            name='a',
                            type=ast.NodeIdentifier('int'),
                        ),
                    ]
                ),
                ast.NodeFunctionDeclaration(
                    name='main',
                    interface=ast.NodeFunctionInterface(parameter_list=[]),
                    body=[],
                ),
            ]
        )
        gen = generator.Generator()
        gen.table = table.Table()
        gen.table.generate_tables(ast_)
        # print('\n' + my_pretty_print(gen))
        real_output = gen.generate()
        expected_output = (
            '// import: stdio\n'
            '// import: ogre3d\n'
            '\n'
            'void f1();\n'
            'void f2();\n'
            'void main();\n'
            '\n'
            'void f1() {\n'
            '  int tmp_0;\n'
            '  int a;\n'
            '\n'
            '  plus(&tmp_0, 1, 2);\n'
            '  a = tmp_0;\n'
            '}\n'
            '\n'
            'void f2() {\n'
            '  int tmp_0;\n'
            '  int a;\n'
            '\n'
            '  x(&tmp_0);\n'
            '  a = tmp_0;\n'
            '}\n'
            '\n'
            'void main() {\n'
            '\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_2(self):
        ast_ = ast.NodeModule(
            declaration_sequence=[
                ast.NodeFunctionDeclaration(
                    name='f1',
                    interface=ast.NodeFunctionInterface(
                        parameter_list =[
                            ast.NodeFormalParameter(
                                name='a',
                                type=ast.NodeIdentifier('int')
                            ),
                            ast.NodeFormalParameter(
                                name='b',
                                type=ast.NodeIdentifier('int')
                            ),
                        ],
                        return_type=ast.NodeIdentifier('int'),
                    ),
                    body=[]
                ),
            ]
        )
        gen = generator.Generator()
        gen.table = table.Table()
        gen.table.generate_tables(ast_)
        # print('\n' + my_pretty_print(gen))
        real_output = gen.generate()
        expected_output = (
            '\n'
            'int f1(int a, int b);\n'
            '\n'
            'int f1(int a, int b) {\n'
            '\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
