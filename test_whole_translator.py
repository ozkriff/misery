# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Functional tests. '''


import unittest
import misc
import generator
import table
import parse
import datatype


def get_generator(input_string):
    ast_ = parse.make_parser().parse(
        input_string,
        lexer=parse.make_lexer(),
    )
    datatype.mark_out_datatypes(ast_)
    generator_ = generator.Generator(
        table=table.Table.from_ast(ast_=ast_)
    )
    return generator_


def translate_mis_to_c(input_string):
    ''' Helper function, compiles program in Mis to program in C. '''
    real_output = get_generator(input_string).generate()
    return real_output


class TestTranslator(unittest.TestCase):

    def test_var_declaration_with_integer_literal(self):
        input_string = 'start := func () { testVar := 1 }\n'
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void start(void);\n'
            '\n'
            'void start(void) {\n'
            '  Int testVar;\n'
            '\n'
            '  testVar = 1;\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_basic_assignment_of_integer_literal(self):
        input_string = 'start := func () { testVar := 1 testVar = 2 }\n'
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void start(void);\n'
            '\n'
            'void start(void) {\n'
            '  Int testVar;\n'
            '\n'
            '  testVar = 1;\n'
            '  testVar = 2;\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_simple_loop_from_1_to_5(self):
        input_string = (
            'start := func () {\n'
            '  i := 0\n'
            '  for isLessInteger(i 5) {'
            '    printInteger(i)\n'
            '    i = plusInteger(i 1)\n'
            '  }'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void start(void);\n'
            '\n'
            'void start(void) {\n'
            '  Int i;\n'
            '  Int tmp_1;\n'
            '  Int tmp_2;\n'
            '\n'
            '  i = 0;\n'
            '  while (1) {\n'
            '    isLessInteger(&tmp_1, i, 5);\n'
            '    if (!tmp_1) {\n'
            '      break;\n'
            '    }\n'
            '    printInteger(i);\n'
            '    plusInteger(&tmp_2, i, 1);\n'
            '    i = tmp_2;\n'
            '  }\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_var_declaration_with_function_call_returning_integer(self):
        input_string = (
            'someNumber := func () -> Int { return 99 }\n'
            'start := func () { testVar := someNumber() }\n'
        )
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void someNumber(Int* __result);\n'
            'void start(void);\n'
            '\n'
            'void someNumber(Int* __result) {\n'
            '\n'
            '  *__result = 99;\n'
            '  return;\n'
            '}\n'
            '\n'
            'void start(void) {\n'
            '  Int tmp_0;\n'
            '  Int testVar;\n'
            '\n'
            '  someNumber(&tmp_0);\n'
            '  testVar = tmp_0;\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_simple_func_1(self):
        input_string = (
            'start := func () {\n'
            '  printInteger(minusInteger(666 99))\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void start(void);\n'
            '\n'
            'void start(void) {\n'
            '  Int tmp_0;\n'
            '\n'
            '  minusInteger(&tmp_0, 666, 99);\n'
            '  printInteger(tmp_0);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_simple_func_2(self):
        input_string = (
            'someNumber := func () -> Int {\n'
            '  return 99\n'
            '}\n'
            'start := func () {\n'
            '  printInteger(minusInteger(666 someNumber()))\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void someNumber(Int* __result);\n'
            'void start(void);\n'
            '\n'
            'void someNumber(Int* __result) {\n'
            '\n'
            '  *__result = 99;\n'
            '  return;\n'
            '}\n'
            '\n'
            'void start(void) {\n'
            '  Int tmp_0;\n'
            '  Int tmp_1;\n'
            '\n'
            '  someNumber(&tmp_1);\n'
            '  minusInteger(&tmp_0, 666, tmp_1);\n'
            '  printInteger(tmp_0);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_simple_func_3(self):
        input_string = (
            'someNumber := func () -> Int {\n'
            '  return minusInteger(100 1)\n'
            '}\n'
            'start := func () {\n'
            '  printInteger(\n'
            '    minusInteger(666 someNumber())\n'
            '  )\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void someNumber(Int* __result);\n'
            'void start(void);\n'
            '\n'
            'void someNumber(Int* __result) {\n'
            '  Int tmp_0;\n'
            '\n'
            '  minusInteger(&tmp_0, 100, 1);\n'
            '  *__result = tmp_0;\n'
            '  return;\n'
            '}\n'
            '\n'
            'void start(void) {\n'
            '  Int tmp_0;\n'
            '  Int tmp_1;\n'
            '\n'
            '  someNumber(&tmp_1);\n'
            '  minusInteger(&tmp_0, 666, tmp_1);\n'
            '  printInteger(tmp_0);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_simple_func_4(self):
        input_string = (
            'someNumber := func (xxx:Int) -> Int {\n'
            '  return minusInteger(100 xxx)\n'
            '}\n'
            'start := func () {\n'
            '  printInteger(\n'
            '    minusInteger(666 someNumber(1))\n'
            '  )\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void someNumber(Int* __result, Int xxx);\n'
            'void start(void);\n'
            '\n'
            'void someNumber(Int* __result, Int xxx) {\n'
            '  Int tmp_0;\n'
            '\n'
            '  minusInteger(&tmp_0, 100, xxx);\n'
            '  *__result = tmp_0;\n'
            '  return;\n'
            '}\n'
            '\n'
            'void start(void) {\n'
            '  Int tmp_0;\n'
            '  Int tmp_1;\n'
            '\n'
            '  someNumber(&tmp_1, 1);\n'
            '  minusInteger(&tmp_0, 666, tmp_1);\n'
            '  printInteger(tmp_0);\n'
            '}\n'
            '\n'
        )
        misc.assert_equal(self, expected_output, real_output)

    def test_some_bug(self):
        ''' Process factorial function. '''
        input_string = (
            'start := func () {\n'
            '    printInteger(fac())\n'
            '    fac()\n'
            '}\n'
            'fac := func () -> Int {\n'
            '    return 1\n'
            '}\n'
        )
        real_output = translate_mis_to_c(input_string)
        expected_output = (
            '\n'
            'void start(void);\n'
            'void fac(Int* __result);\n'
            '\n'
            'void start(void) {\n'
            '  Int tmp_0;\n'
            '  Int tmp_1;\n'
            '\n'
            '  fac(&tmp_0);\n'
            '  printInteger(tmp_0);\n'
            '  fac(&tmp_1);\n'
            '}\n'
            '\n'
            'void fac(Int* __result) {\n'
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
            'start := func () {\n'
            '  printInteger(fib(10))\n'
            '}\n'
            'fib := func (n:Int) -> Int {\n'
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
            'void fib(Int* __result, Int n);\n'
            '\n'
            'void start(void) {\n'
            '  Int tmp_0;\n'
            '\n'
            '  fib(&tmp_0, 10);\n'
            '  printInteger(tmp_0);\n'
            '}\n'
            '\n'
            'void fib(Int* __result, Int n) {\n'
            '  Int tmp_0;\n'
            '  Int tmp_1;\n'
            '  Int tmp_2;\n'
            '  Int tmp_3;\n'
            '  Int tmp_4;\n'
            '  Int tmp_5;\n'
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
            'start := func () {\n'
            '  printInteger(fac(3))\n'
            '}\n'
            'fac := func (n:Int) -> Int {\n'
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
            'void fac(Int* __result, Int n);\n'
            '\n'
            'void start(void) {\n'
            '  Int tmp_0;\n'
            '\n'
            '  fac(&tmp_0, 3);\n'
            '  printInteger(tmp_0);\n'
            '}\n'
            '\n'
            'void fac(Int* __result, Int n) {\n'
            '  Int tmp_0;\n'
            '  Int tmp_1;\n'
            '  Int tmp_2;\n'
            '  Int tmp_3;\n'
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
