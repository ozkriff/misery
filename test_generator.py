# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'generator' module. '''


import unittest
import ast
import misc
import generator
import table


class TestGenerator(unittest.TestCase):
    ''' Test 'Generator' class. '''

    def test_1(self):
        ''' Generate some code. '''
        ast_ = ast.Module(
            import_list=['stdio', 'ogre3d'],
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='f1',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            expression=ast.FunctionCall(
                                expression=ast.Identifier('plus'),
                                argument_list=[
                                    ast.Number(1),
                                    ast.Number(2),
                                ]
                            ),
                            name='a',
                            type=ast.Identifier('int'),
                        ),
                    ]
                ),
                ast.FunctionDeclaration(
                    name='f2',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.VariableDeclaration(
                            expression=ast.FunctionCall(
                                expression=ast.Identifier('x'),
                                argument_list=[]
                            ),
                            name='a',
                            type=ast.Identifier('int'),
                        ),
                    ]
                ),
                ast.FunctionDeclaration(
                    name='main',
                    interface=ast.FunctionInterface(parameter_list=[]),
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

    def test_nested_func_calls(self):
        ''' Generate nested function calls. '''
        ast_ = ast.Module(
            import_list=[],
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='main',
                    interface=ast.FunctionInterface(parameter_list=[]),
                    body=[
                        ast.FunctionCall(
                            expression=ast.Identifier('a'),
                            argument_list=[
                                ast.FunctionCall(
                                    expression=ast.Identifier('b'),
                                    argument_list=[]
                                ),
                            ]
                        ),
                    ]
                )
            ]
        )
        gen = generator.Generator()
        gen.table = table.Table()
        gen.table.generate_tables(ast_)
        real_output = gen.generate()
        # TODO: fix indentation
        expected_output = (
            '\n'
            'void main();\n'
            '\n'
            'void main() {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '\n'
            '    b(&tmp_1);\n'
            'a(&tmp_0, tmp_1);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_2(self):
        ''' Generate some simple code. '''
        ast_ = ast.Module(
            declaration_sequence=[
                ast.FunctionDeclaration(
                    name='f1',
                    interface=ast.FunctionInterface(
                        parameter_list=[
                            ast.Parameter(
                                name='a',
                                type=ast.Identifier('int')
                            ),
                            ast.Parameter(
                                name='b',
                                type=ast.Identifier('int')
                            ),
                        ],
                        return_type=ast.Identifier('int'),
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

    def test_if(self):
        ''' Test if. '''
        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
        )
        func.constant_list = []
        func.variable_list = [
            table.Variable(type='int', name='tmp_0'),
            table.Variable(type='int', name='tmp_1'),
        ]
        func.block_list = [
            [
                table.IfStatement(
                    expression_id=table.LinkToFunctionCall(id=0),
                    if_branch_id=1,
                ),
            ],
            [
                table.FunctionCallStatement(
                    expression_id=table.LinkToFunctionCall(id=1)),
                table.FunctionCallStatement(
                    expression_id=table.LinkToFunctionCall(id=2)),
            ],
        ]
        func.expression_list = [
            table.FunctionCallExpression(
                result_id=table.LinkToVariable(id=0),
                name='f1',
                argument_id_list=[],
            ),
            table.FunctionCallExpression(
                result_id=table.LinkToVariable(id=1),
                name='f2',
                argument_id_list=[],
            ),
            table.FunctionCallExpression(
                result_id=table.LinkToVariable(id=1),
                name='f3',
                argument_id_list=[],
            ),
        ]
        table_ = table.Table()
        table_.declaration_list = [func]

        gen = generator.Generator()
        gen.table = table_
        real_output = gen.generate()
        expected_output = (
            '\n'
            'void main();\n'
            '\n'
            'void main() {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '\n'
            '  if (f1(&tmp_0)) {\n'
            '    f2(&tmp_1);\n'
            '    f3(&tmp_1);\n'
            '  }\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_return(self):
        ''' Test return. '''
        func = table.Function(
            name='main',
            interface=ast.FunctionInterface(
                return_type=None,
                parameter_list=[],
            ),
        )
        func.constant_list = [table.Constant(type="int", value=0)]
        func.variable_list = []
        func.block_list = [
            [
                table.ReturnStatement(
                    expression_id=table.LinkToNumberConstant(id=0),
                ),
            ],
        ]
        func.expression_list = []
        table_ = table.Table()
        table_.declaration_list = [func]

        gen = generator.Generator()
        gen.table = table_
        real_output = gen.generate()
        expected_output = (
            '\n'
            'void main();\n'
            '\n'
            'void main() {\n'
            '\n'
            '  return 0;\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
