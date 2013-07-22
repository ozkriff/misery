# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Functional tests. '''


import unittest
import misc
import generator
import table
import parse


def get_generator(input_string):
    generator_ = generator.Generator(
        table=table.Table.from_ast(
            ast_=parse.make_parser().parse(
                input_string,
                lexer=parse.make_lexer(),
            )
        )
    )
    return generator_


def translate_mis_to_c(input_string):
    ''' Helper function, compiles program in Mis to program in C. '''
    real_output = get_generator(input_string).generate()
    return real_output


class TestTranslator(unittest.TestCase):

    def test_simple_func_1(self):
        input_string = (
            'let start func () {\n'
            '  printInteger(minusInteger(666 99))\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
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
        input_string = (
            'let someNumber func () -> int {\n'
            '  return 99\n'
            '}\n'
            'let start func () {\n'
            '  printInteger(minusInteger(666 someNumber()))\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
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
        input_string = (
            'let someNumber func () -> int {\n'
            '  return minusInteger(100 1)\n'
            '}\n'
            'let start func () {\n'
            '  printInteger(\n'
            '    minusInteger(666 someNumber())\n'
            '  )\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
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
        input_string = (
            'let someNumber func (xxx:int) -> int {\n'
            '  return minusInteger(100 xxx)\n'
            '}\n'
            'let start func () {\n'
            '  printInteger(\n'
            '    minusInteger(666 someNumber(1))\n'
            '  )\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
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
        input_string = (
            'let start func () {\n'
            '    printInteger(fac())\n'
            '    fac()\n'
            '}\n'
            'let fac func () -> int {\n'
            '    return 1\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
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

    def test_fib_1(self):
        ''' Process fib function. '''
        input_string = (
            'let start func () {\n'
            '  printInteger(fib(10))\n'
            '}\n'
            'let fib func (n:int) -> int {\n'
            '  if isLessInteger(n 2) {\n'
            '    return n\n'
            '  } else {\n'
            '    return plusInteger (\n'
            '      fib(minusInteger(n 1))\n'
            '      fib(minusInteger(n 2))\n'
            '    )\n'
            '  }\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void start(void);\n'
            'void fib(int* __result, int n);\n'
            '\n'
            'void start(void) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '\n'
            '  fib(&tmp_1, 10);\n'
            '  printInteger(&tmp_0, tmp_1);\n'
            '}\n'
            '\n'
            'void fib(int* __result, int n) {\n'
            '  int tmp_0;\n'
            '  int tmp_1;\n'
            '  int tmp_2;\n'
            '  int tmp_3;\n'
            '  int tmp_4;\n'
            '  int tmp_5;\n'
            '\n'
            '  isLessInteger(&tmp_0, n, 2);\n'
            '  if (tmp_0) {\n'
            '    *__result = n;\n'
            '    return;\n'
            '  } else {\n'
            '    minusInteger(&tmp_3, n, 1);\n'
            '    fib(&tmp_2, tmp_3);\n'
            '    minusInteger(&tmp_5, n, 2);\n'
            '    fib(&tmp_4, tmp_5);\n'
            '    plusInteger(&tmp_1, tmp_2, tmp_4);\n'
            '    *__result = tmp_1;\n'
            '    return;\n'
            '  }\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_factorial_1(self):
        ''' Process factorial function. '''
        input_string = (
            'let start func () {\n'
            '  printInteger(fac(3))\n'
            '}\n'
            'let fac func (n:int) -> int {\n'
            '  if isEqualInteger(n 0) {\n'
            '    return 1\n'
            '  }\n'
            '  return multiplyInteger(\n'
            '    fac(minusInteger(n 1))\n'
            '    n\n'
            '  )\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
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

        # TODO: try to compile (and run?)
        # with open('out.c', 'w') as file:
        #     file.write(get_generator(input_string).generate_full())
