# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Functional tests. '''


import unittest
import misc
import generator
import table
import parse
import datatype
import textwrap


def get_generator(input_string):
    generator_ = generator.Generator(
        table=table.Table.from_ast(
            ast_=datatype.mark_out_datatypes(
                parse.make_parser().parse(
                    input_string,
                    lexer=parse.make_lexer(),
                )
            )
        )
    )
    return generator_


def translate_mis_to_c(input_string):
    ''' Helper function, compiles program in Mis to program in C. '''
    real_output = get_generator(input_string).generate()
    return real_output


# TODO: try to compile and run
def translate_mis_to_c_and_write_to_file(input_string, filename='out.c'):
    ''' Translate to full C version and write to file. '''
    with open(filename, 'w') as file:
        file.write(get_generator(input_string).generate_full())


def check_translation(test_case, input_string, expected_output):
    ''' Small helper function. '''
    real_output = translate_mis_to_c(textwrap.dedent(input_string))
    misc.assert_equal(test_case, textwrap.dedent(expected_output), real_output)
    # translate_mis_to_c_and_write_to_file(
    #     input_string=input_string,
    #     filename = misc.get_caller_func_name()[5:] + '_out.c',
    # )
    # try_to_compile_and_run_file()


class TestTranslator(unittest.TestCase):

    def test_var_declaration_with_integer_literal(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  testVar := 1
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  Int testVar;

                  testVar = 1;
                }

            ''',
        )

    def test_struct(self):
        check_translation(
            test_case=self,
            input_string='''
                MyStruct := struct {
                  field1: Int
                  field2: Int
                }
                start := func () {
                  t := MyStruct()
                }
            ''',
            expected_output='''
                typedef struct MyStruct MyStruct;
                void start(void);

                typedef struct {
                  Int field2;
                  Int field1;
                } MyStruct;

                void start(void) {
                  MyStruct tmp_0;
                  MyStruct t;

                  MyStruct(&tmp_0);
                  t = tmp_0;
                }

            ''',
        )

    def test_struct_as_func_argument(self):
        check_translation(
            test_case=self,
            input_string='''
                MyStruct := struct {
                  field1: Int
                  field2: Int
                }
                someFunc := func (x:MyStruct) -> MyStruct{
                  return x
                }
                start := func () {
                  t := MyStruct()
                  t2 := someFunc(t)
                }
            ''',
            expected_output='''
                typedef struct MyStruct MyStruct;
                void someFunc(MyStruct* __result, MyStruct x);
                void start(void);

                typedef struct {
                  Int field2;
                  Int field1;
                } MyStruct;

                void someFunc(MyStruct* __result, MyStruct x) {

                  *__result = x;
                  return;
                }

                void start(void) {
                  MyStruct tmp_0;
                  MyStruct t;
                  MyStruct tmp_2;
                  MyStruct t2;

                  MyStruct(&tmp_0);
                  t = tmp_0;
                  someFunc(&tmp_2, t);
                  t2 = tmp_2;
                }

            ''',
        )

    def test_var_declaration_with_string_literal(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  testVar := "some string"
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  String testVar;

                  testVar = "some string";
                }

            ''',
        )

    def test_print_string_literal(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  printString("hello")
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {

                  printString("hello");
                }

            ''',
        )

    def test_print_string_var(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  testVar := "print this to console, please"
                  printString(testVar)
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  String testVar;

                  testVar = "print this to console, please";
                  printString(testVar);
                }

            ''',
        )

    def test_basic_assignment_of_integer_literal(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  testVar := 1 testVar = 2
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  Int testVar;

                  testVar = 1;
                  testVar = 2;
                }

            ''',
        )

    def test_simple_loop_from_1_to_5(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  i := 0
                  for isLessInteger(i 5) {
                    printInteger(i)
                    i = plusInteger(i 1)
                  }
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  Int i;
                  Int tmp_1;
                  Int tmp_2;

                  i = 0;
                  while (1) {
                    isLessInteger(&tmp_1, i, 5);
                    if (!tmp_1) {
                      break;
                    }
                    printInteger(i);
                    plusInteger(&tmp_2, i, 1);
                    i = tmp_2;
                  }
                }

            ''',
        )

    def test_var_declaration_with_function_call_returning_string(self):
        check_translation(
            test_case=self,
            input_string='''
                someString := func () -> String {
                  return "hi"
                }
                start := func () {
                  s := someString() printString(s)
                }
            ''',
            expected_output='''
                void someString(String* __result);
                void start(void);

                void someString(String* __result) {

                  *__result = "hi";
                  return;
                }

                void start(void) {
                  String tmp_0;
                  String s;

                  someString(&tmp_0);
                  s = tmp_0;
                  printString(s);
                }

            ''',
        )

    def test_nested_func_calls_with_strings(self):
        check_translation(
            test_case=self,
            input_string='''
                someString := func () -> String {
                  return "hi"
                }
                start := func () {
                  printString(someString())
                }
            ''',
            expected_output='''
                void someString(String* __result);
                void start(void);

                void someString(String* __result) {

                  *__result = "hi";
                  return;
                }

                void start(void) {
                  String tmp_0;

                  someString(&tmp_0);
                  printString(tmp_0);
                }

            ''',
        )

    def test_var_declaration_with_function_call_returning_integer(self):
        check_translation(
            test_case=self,
            input_string='''
                someNumber := func () -> Int {
                  return 99
                }
                start := func () {
                  testVar := someNumber()
                }
            ''',
            expected_output='''
                void someNumber(Int* __result);
                void start(void);

                void someNumber(Int* __result) {

                  *__result = 99;
                  return;
                }

                void start(void) {
                  Int tmp_0;
                  Int testVar;

                  someNumber(&tmp_0);
                  testVar = tmp_0;
                }

            ''',
        )

    def test_simple_func_1(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  printInteger(minusInteger(666 99))
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  Int tmp_0;

                  minusInteger(&tmp_0, 666, 99);
                  printInteger(tmp_0);
                }

            ''',
        )

    def test_simple_func_2(self):
        check_translation(
            test_case=self,
            input_string='''
                someNumber := func () -> Int {
                  return 99
                }
                start := func () {
                  printInteger(minusInteger(666 someNumber()))
                }
            ''',
            expected_output='''
                void someNumber(Int* __result);
                void start(void);

                void someNumber(Int* __result) {

                  *__result = 99;
                  return;
                }

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;

                  someNumber(&tmp_1);
                  minusInteger(&tmp_0, 666, tmp_1);
                  printInteger(tmp_0);
                }

            ''',
        )

    def test_simple_func_3(self):
        check_translation(
            test_case=self,
            input_string='''
                someNumber := func () -> Int {
                  return minusInteger(100 1)
                }
                start := func () {
                  printInteger(
                    minusInteger(666 someNumber())
                  )
                }
            ''',
            expected_output='''
                void someNumber(Int* __result);
                void start(void);

                void someNumber(Int* __result) {
                  Int tmp_0;

                  minusInteger(&tmp_0, 100, 1);
                  *__result = tmp_0;
                  return;
                }

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;

                  someNumber(&tmp_1);
                  minusInteger(&tmp_0, 666, tmp_1);
                  printInteger(tmp_0);
                }

            ''',
        )

    def test_simple_func_4(self):
        check_translation(
            test_case=self,
            input_string='''
                someNumber := func (xxx:Int) -> Int {
                  return minusInteger(100 xxx)
                }
                start := func () {
                  printInteger(
                    minusInteger(666 someNumber(1))
                  )
                }
            ''',
            expected_output='''
                void someNumber(Int* __result, Int xxx);
                void start(void);

                void someNumber(Int* __result, Int xxx) {
                  Int tmp_0;

                  minusInteger(&tmp_0, 100, xxx);
                  *__result = tmp_0;
                  return;
                }

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;

                  someNumber(&tmp_1, 1);
                  minusInteger(&tmp_0, 666, tmp_1);
                  printInteger(tmp_0);
                }

            ''',
        )

    def test_some_bug(self):
        ''' Process factorial function. '''
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                    printInteger(fac())
                    fac()
                }
                fac := func () -> Int {
                    return 1
                }
            ''',
            expected_output='''
                void start(void);
                void fac(Int* __result);

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;

                  fac(&tmp_0);
                  printInteger(tmp_0);
                  fac(&tmp_1);
                }

                void fac(Int* __result) {

                  *__result = 1;
                  return;
                }

            ''',
        )

    def test_fib_1(self):
        ''' Process fib function. '''
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  printInteger(fib(10))
                }
                fib := func (n:Int) -> Int {
                  if isLessInteger(n 2) {
                    return n
                  } else {
                    return plusInteger (
                      fib(minusInteger(n 1))
                      fib(minusInteger(n 2))
                    )
                  }
                }
            ''',
            expected_output='''
                void start(void);
                void fib(Int* __result, Int n);

                void start(void) {
                  Int tmp_0;

                  fib(&tmp_0, 10);
                  printInteger(tmp_0);
                }

                void fib(Int* __result, Int n) {
                  Int tmp_0;
                  Int tmp_1;
                  Int tmp_2;
                  Int tmp_3;
                  Int tmp_4;
                  Int tmp_5;

                  isLessInteger(&tmp_0, n, 2);
                  if (tmp_0) {
                    *__result = n;
                    return;
                  } else {
                    minusInteger(&tmp_3, n, 1);
                    fib(&tmp_2, tmp_3);
                    minusInteger(&tmp_5, n, 2);
                    fib(&tmp_4, tmp_5);
                    plusInteger(&tmp_1, tmp_2, tmp_4);
                    *__result = tmp_1;
                    return;
                  }
                }

            ''',
        )

    def test_factorial_1(self):
        ''' Process factorial function. '''
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  printInteger(fac(3))
                }
                fac := func (n:Int) -> Int {
                  if isEqualInteger(n 0) {
                    return 1
                  }
                  return multiplyInteger(
                    fac(minusInteger(n 1))
                    n
                  )
                }
            ''',
            expected_output='''
                void start(void);
                void fac(Int* __result, Int n);

                void start(void) {
                  Int tmp_0;

                  fac(&tmp_0, 3);
                  printInteger(tmp_0);
                }

                void fac(Int* __result, Int n) {
                  Int tmp_0;
                  Int tmp_1;
                  Int tmp_2;
                  Int tmp_3;

                  isEqualInteger(&tmp_0, n, 0);
                  if (tmp_0) {
                    *__result = 1;
                    return;
                  }
                  minusInteger(&tmp_3, n, 1);
                  fac(&tmp_2, tmp_3);
                  multiplyInteger(&tmp_1, tmp_2, n);
                  *__result = tmp_1;
                  return;
                }

            ''',
        )

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
