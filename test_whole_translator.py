# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Functional tests. '''


import unittest
import subprocess
import misc
import generator
import parse
import datatype
import textwrap
import identifier_table


def get_generator(input_string):
    ast_ = parse.make_parser().parse(
        input_string,
        lexer=parse.make_lexer(),
    )
    ast_.identifier_list = identifier_table.identifier_table(ast_)
    ast_ = datatype.mark_out_datatypes(ast_=ast_)
    generator_ = generator.Generator(ast_=ast_)
    return generator_


def translate_mis_to_c(input_string):
    ''' Helper function, compiles program in Mis to program in C. '''
    real_output = get_generator(input_string).generate()
    return real_output


def translate_mis_to_c_and_write_to_file(input_string, filename='out.c'):
    ''' Translate to full C version and write to file. '''
    with open(filename, 'w') as file:
        file.write(get_generator(input_string).generate_full())


def try_to_compile_and_run_file(file_name, input_string):
    # translate mis to ANSI C and write to file
    translate_mis_to_c_and_write_to_file(
        input_string=input_string,
        filename=file_name,
    )

    # compile c code with c compiler TODO: support other compilers
    compiler_proc = subprocess.Popen(
        ['tcc', file_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    compiler_out, compiler_err = compiler_proc.communicate()
    assert compiler_out == ''
    if compiler_err != '':
        raise Exception('ANSI C compiler error: ' + compiler_err)

    # run compiler program and check its output
    proc = subprocess.Popen(
        [file_name.replace('.c', '.exe')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    # TODO: check output # if out != '': print '\nOUT: ', out, '\n'
    if err != '':
        raise Exception('Compiled prog error: ' + compiler_err)


def check_translation(test_case, input_string, expected_output):
    ''' Small helper function. '''
    real_output = translate_mis_to_c(textwrap.dedent(input_string))
    misc.assert_equal(test_case, textwrap.dedent(expected_output), real_output)
    file_name = misc.get_caller_func_name()[5:] + '_out.c'
    try_to_compile_and_run_file(file_name, input_string)


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

                struct MyStruct {
                  Int field1;
                  Int field2;
                };

                void MyStruct_init(MyStruct* __result) {
                  /* todo */
                }

                void start(void) {
                  MyStruct t;
                  MyStruct tmp_1;

                  MyStruct_init(&tmp_1);
                  t = tmp_1;
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

                struct MyStruct {
                  Int field1;
                  Int field2;
                };

                void MyStruct_init(MyStruct* __result) {
                  /* todo */
                }

                void someFunc(MyStruct* __result, MyStruct x) {

                  *__result = x;
                  return;
                }

                void start(void) {
                  MyStruct tmp_3;
                  MyStruct t2;
                  MyStruct t;
                  MyStruct tmp_1;

                  MyStruct_init(&tmp_1);
                  t = tmp_1;
                  someFunc(&tmp_3, t);
                  t2 = tmp_3;
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
                  Int tmp_2;
                  Int tmp_1;

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
                  String s;
                  String tmp_1;

                  someString(&tmp_1);
                  s = tmp_1;
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
                  Int testVar;
                  Int tmp_1;

                  someNumber(&tmp_1);
                  testVar = tmp_1;
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
                  Int tmp_1;
                  Int tmp_0;

                  someNumber(&tmp_0);
                  minusInteger(&tmp_1, 666, tmp_0);
                  printInteger(tmp_1);
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
                  Int tmp_1;
                  Int tmp_0;

                  someNumber(&tmp_0);
                  minusInteger(&tmp_1, 666, tmp_0);
                  printInteger(tmp_1);
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
                  Int tmp_1;
                  Int tmp_0;

                  someNumber(&tmp_0, 1);
                  minusInteger(&tmp_1, 666, tmp_0);
                  printInteger(tmp_1);
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
                  Int tmp_1;
                  Int tmp_0;

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
                  Int tmp_5;
                  Int tmp_4;
                  Int tmp_3;
                  Int tmp_2;
                  Int tmp_1;
                  Int tmp_0;

                  isLessInteger(&tmp_0, n, 2);
                  if (tmp_0) {
                    *__result = n;
                    return;
                  } else {
                    minusInteger(&tmp_1, n, 1);
                    fib(&tmp_2, tmp_1);
                    minusInteger(&tmp_3, n, 2);
                    fib(&tmp_4, tmp_3);
                    plusInteger(&tmp_5, tmp_2, tmp_4);
                    *__result = tmp_5;
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
                  Int tmp_3;
                  Int tmp_2;
                  Int tmp_1;
                  Int tmp_0;

                  isEqualInteger(&tmp_0, n, 0);
                  if (tmp_0) {
                    *__result = 1;
                    return;
                  }
                  minusInteger(&tmp_1, n, 1);
                  fac(&tmp_2, tmp_1);
                  multiplyInteger(&tmp_3, tmp_2, n);
                  *__result = tmp_3;
                  return;
                }

            ''',
        )

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
