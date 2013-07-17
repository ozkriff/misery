# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Functional tests. '''


import unittest
import misc
import generator
import table
import parse


def compile(input_string):
    ''' Helper function, compiles program in Mis to program in C. '''
    generator_ = generator.Generator(
        table=table.Table.from_ast(
            ast_=parse.make_parser().parse(
                input_string,
                lexer=parse.make_lexer(),
            )
        )
    )
    real_output = generator_.generate()
    return real_output


class TestTranslator(unittest.TestCase):

    def test_simple_func_1(self):
        input_string = '''
            func start() {
                printInteger(minusInteger(666, 99))
            }
        '''
        real_output = compile(input_string)
        expected_output = (
            '\n'
            'void start(void);\n'
            '\n'
            'void start(void) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '\n'
            '  minusInteger(&tmp_1, 666, 99);\n'
            '  printInteger(&tmp_0, tmp_1);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_simple_func_2(self):
        input_string = '''
            func someNumber() -> int {
                return 99
            }
            func start() {
                printInteger(minusInteger(666, someNumber()))
            }
        '''
        real_output = compile(input_string)
        expected_output = (
            '\n'
            'void someNumber(int* __result);\n'
            'void start(void);\n'
            '\n'
            'void someNumber(int* __result) {\n'
            '\n'
            '  *__result = 99;\n'
            '  return;\n'
            '}\n'
            '\n'
            'void start(void) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '  int tmp_2;\n'
            '\n'
            '  someNumber(&tmp_2);\n'
            '  minusInteger(&tmp_1, 666, tmp_2);\n'
            '  printInteger(&tmp_0, tmp_1);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_simple_func_3(self):
        input_string = '''
            func someNumber() -> int {
                return minusInteger(100, 1)
            }
            func start() {
                printInteger(
                    minusInteger(666, someNumber()),
                )
            }
        '''
        real_output = compile(input_string)
        expected_output = (
            '\n'
            'void someNumber(int* __result);\n'
            'void start(void);\n'
            '\n'
            'void someNumber(int* __result) {\n'
            '  int tmp_0;\n'
            '\n'
            '  minusInteger(&tmp_0, 100, 1);\n'
            '  *__result = tmp_0;\n'
            '  return;\n'
            '}\n'
            '\n'
            'void start(void) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '  int tmp_2;\n'
            '\n'
            '  someNumber(&tmp_2);\n'
            '  minusInteger(&tmp_1, 666, tmp_2);\n'
            '  printInteger(&tmp_0, tmp_1);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_simple_func_4(self):
        input_string = '''
            func someNumber(xxx int) -> int {
                return minusInteger(100, xxx)
            }
            func start() {
                printInteger(
                    minusInteger(666, someNumber(1)),
                )
            }
        '''
        real_output = compile(input_string)
        expected_output = (
            '\n'
            'void someNumber(int* __result, int xxx);\n'
            'void start(void);\n'
            '\n'
            'void someNumber(int* __result, int xxx) {\n'
            '  int tmp_0;\n'
            '\n'
            '  minusInteger(&tmp_0, 100, xxx);\n'
            '  *__result = tmp_0;\n'
            '  return;\n'
            '}\n'
            '\n'
            'void start(void) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '  int tmp_2;\n'
            '\n'
            '  someNumber(&tmp_2, 1);\n'
            '  minusInteger(&tmp_1, 666, tmp_2);\n'
            '  printInteger(&tmp_0, tmp_1);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_some_bug(self):
        ''' Process factorial function. '''
        input_string = '''
            func start() {
                printInteger(fac())
                fac()
            }
            func fac() -> int {
                return 1
            }
        '''
        real_output = compile(input_string)
        expected_output = (
            '\n'
            'void start(void);\n'
            'void fac(int* __result);\n'
            '\n'
            'void start(void) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '  int tmp_2;\n'
            '\n'
            '  fac(&tmp_1);\n'
            '  printInteger(&tmp_0, tmp_1);\n'
            '  fac(&tmp_2);\n'
            '}\n'
            '\n'
            'void fac(int* __result) {\n'
            '\n'
            '  *__result = 1;\n'
            '  return;\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_factorial_1(self):
        ''' Process factorial function. '''
        input_string = '''
            func start() {
                printInteger(fac(3))
            }
            func fac(n int) -> int {
                if isEqualInteger(n, 0) {
                    return 1
                }
                return multiplyInteger(
                    fac(minusInteger(n, 1)),
                    n,
                )
            }
        '''
        real_output = compile(input_string)
        expected_output = (
            '\n'
            'void start(void);\n'
            'void fac(int* __result, int n);\n'
            '\n'
            'void start(void) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '\n'
            '  fac(&tmp_1, 3);\n'
            '  printInteger(&tmp_0, tmp_1);\n'
            '}\n'
            '\n'
            'void fac(int* __result, int n) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '  int tmp_2;\n'
            '  int tmp_3;\n'
            '\n'
            '  isEqualInteger(&tmp_0, n, 0);\n'
            '  if (tmp_0) {\n'
            '    *__result = 1;\n'
            '    return;\n'
            '  }\n'
            '  minusInteger(&tmp_3, n, 1);\n'
            '  fac(&tmp_2, tmp_3);\n'
            '  multiplyInteger(&tmp_1, tmp_2, n);\n'
            '  *__result = tmp_1;\n'
            '  return;\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

        # TODO:
        # with open('out.c', 'w') as file:
        #    file.write(gen.generate_full())
