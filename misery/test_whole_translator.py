# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Functional tests. '''


import unittest
import subprocess
import os
import textwrap
from misery import (
    misc,
    generator,
    parse,
    datatype,
    identifier_table,
)


def get_generator(input_string):
    ast_ = parse.make_parser().parse(
        input_string,
        lexer=parse.make_lexer(),
    )
    ast_.identifier_list = identifier_table.identifier_table(ast_)
    ast_ = datatype.mark_out_datatypes(ast_=ast_)
    generator.scan_module_vars(ast_)
    generator_ = generator.Generator(ast_=ast_)
    return generator_


def translate_mis_to_c(input_string):
    ''' Helper function, compiles program in Mis to program in C. '''
    real_output = get_generator(input_string).generate()
    return real_output


def translate_mis_to_c_and_write_to_file(input_string, filename='out.c'):
    ''' Translate to full C version and write to file. '''
    with open(filename, 'w') as f:
        f.write(get_generator(input_string).generate_full())


def try_to_compile_and_run_file(
    test_case,
    c_file_name,
    input_string,
    expected_stdout,
):
    # translate mis to ANSI C and write to file
    translate_mis_to_c_and_write_to_file(
        input_string=input_string,
        filename=c_file_name,
    )

    # compile c code with c compiler TODO: support other compilers
    compiler_proc = subprocess.Popen(
        ['tcc', c_file_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    compiler_out, compiler_err = compiler_proc.communicate()
    assert os.path.isfile(c_file_name)
    os.remove(c_file_name)
    assert compiler_out == ''
    test_case.assertEqual(
        compiler_err, '',
        'ANSI C compiler error:\n' + compiler_err,
    )

    # run compiler program and check its output
    exe_file_name = c_file_name.replace('.c', '.exe')
    proc = subprocess.Popen(
        [exe_file_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    out, err = proc.communicate()
    assert os.path.isfile(exe_file_name)
    if out != '':
        misc.assert_equal(test_case, '\n', out[-1])
    os.remove(exe_file_name)
    misc.assert_equal(test_case, expected_stdout, out)
    test_case.assertEqual(err, '', 'Compiled prog error:\n' + err)


def check_translation(
    test_case,
    input_string,
    expected_output,
    expected_stdout='',
):
    ''' Small helper function. '''
    real_output = translate_mis_to_c(textwrap.dedent(input_string))
    misc.assert_equal(test_case, textwrap.dedent(expected_output), real_output)
    c_file_name = misc.get_caller_func_name().replace('test_', '') + '_out.c'
    try_to_compile_and_run_file(
        test_case,
        c_file_name,
        input_string,
        expected_stdout,
    )


class TestTranslator(unittest.TestCase):

    def test_var_declaration_with_integer_literal(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  testVar ::= 1
                  testVar = 2
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  Int* testVar;
                  Int tmp_0;
                  Int const_0;
                  Int const_1;

                  const_0 = 1;
                  const_1 = 2;

                  testVar = &tmp_0;
                  *testVar = const_0;
                  *testVar = const_1;
                }

            ''',
        )

    def test_integer_var_declaration_with_constructor(self):
        pass
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  testVar := Int(1)
                  printInt(testVar)
                  printNewLine()
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  Int* testVar;
                  Int tmp_0;
                  Int const_0;

                  const_0 = 1;

                  testVar = &tmp_0;
                  Int_init(&tmp_0, &const_0);
                  *testVar = tmp_0;
                  printInt(testVar);
                  printNewLine();
                }

            ''',
            expected_stdout='1\n',
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
                  MyStruct* t;
                  MyStruct tmp_0;

                  t = &tmp_0;
                  MyStruct_init(&tmp_0);
                  *t = tmp_0;
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
                void someFunc(MyStruct* __result, MyStruct* x);
                void start(void);

                struct MyStruct {
                  Int field1;
                  Int field2;
                };

                void MyStruct_init(MyStruct* __result) {
                  /* todo */
                }

                void someFunc(MyStruct* __result, MyStruct* x) {
                  *__result = *x;
                  return;
                }

                void start(void) {
                  MyStruct* t;
                  MyStruct* t2;
                  MyStruct tmp_0;
                  MyStruct tmp_1;

                  t = &tmp_0;
                  MyStruct_init(&tmp_0);
                  *t = tmp_0;
                  t2 = &tmp_1;
                  someFunc(&tmp_1, t);
                  *t2 = tmp_1;
                }

            ''',
        )

    def test_var_declaration_with_string_literal(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  testVar ::= "some string"
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  String* testVar;
                  String tmp_0;
                  String const_0;

                  const_0 = "some string";

                  testVar = &tmp_0;
                  *testVar = const_0;
                }

            ''',
        )

    def test_print_string_literal(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  printString("hello")
                  printNewLine()
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  String const_0;

                  const_0 = "hello";

                  printString(&const_0);
                  printNewLine();
                }

            ''',
            expected_stdout='hello\n',
        )

    def test_print_string_var(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  testVar ::= "print this to console, please"
                  printString(testVar)
                  printNewLine()
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  String* testVar;
                  String tmp_0;
                  String const_0;

                  const_0 = "print this to console, please";

                  testVar = &tmp_0;
                  *testVar = const_0;
                  printString(testVar);
                  printNewLine();
                }

            ''',
            expected_stdout='print this to console, please\n',
        )

    def test_basic_assignment_of_integer_literal(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  testVar ::= 1 testVar = 2
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  Int* testVar;
                  Int tmp_0;
                  Int const_0;
                  Int const_1;

                  const_0 = 1;
                  const_1 = 2;

                  testVar = &tmp_0;
                  *testVar = const_0;
                  *testVar = const_1;
                }

            ''',
        )

    def test_simple_loop_from_1_to_5(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  i ::= 0
                  for isLessInt(i 5) {
                    printInt(i)
                    printNewLine()
                    i = plusInt(i 1)
                  }
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  Int* i;
                  Int tmp_0;
                  Int tmp_1;
                  Int tmp_2;
                  Int const_0;
                  Int const_1;
                  Int const_2;

                  const_0 = 0;
                  const_1 = 5;
                  const_2 = 1;

                  i = &tmp_0;
                  *i = const_0;
                  while (1) {
                    isLessInt(&tmp_1, i, &const_1);
                    if (!tmp_1) {
                      break;
                    }
                    printInt(i);
                    printNewLine();
                    plusInt(&tmp_2, i, &const_2);
                    *i = tmp_2;
                  }
                }

            ''',
            expected_stdout=(
                '0\n'
                '1\n'
                '2\n'
                '3\n'
                '4\n'
            ),
        )

    def test_var_declaration_with_function_call_returning_string(self):
        check_translation(
            test_case=self,
            input_string='''
                someString := func () -> String {
                  return "hi"
                }
                start := func () {
                  s ::= someString()
                  printString(s)
                  printNewLine()
                }
            ''',
            expected_output='''
                void someString(String* __result);
                void start(void);

                void someString(String* __result) {
                  String const_0;

                  const_0 = "hi";

                  *__result = const_0;
                  return;
                }

                void start(void) {
                  String* s;
                  String tmp_0;
                  String tmp_1;

                  s = &tmp_0;
                  someString(&tmp_1);
                  *s = tmp_1;
                  printString(s);
                  printNewLine();
                }

            ''',
            expected_stdout='hi\n',
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
                  printNewLine()
                }
            ''',
            expected_output='''
                void someString(String* __result);
                void start(void);

                void someString(String* __result) {
                  String const_0;

                  const_0 = "hi";

                  *__result = const_0;
                  return;
                }

                void start(void) {
                  String tmp_0;

                  someString(&tmp_0);
                  printString(&tmp_0);
                  printNewLine();
                }

            ''',
            expected_stdout='hi\n',
        )

    def test_var_declaration_with_function_call_returning_integer(self):
        check_translation(
            test_case=self,
            input_string='''
                someNumber := func () -> Int {
                  return 99
                }
                start := func () {
                  testVar ::= someNumber()
                }
            ''',
            expected_output='''
                void someNumber(Int* __result);
                void start(void);

                void someNumber(Int* __result) {
                  Int const_0;

                  const_0 = 99;

                  *__result = const_0;
                  return;
                }

                void start(void) {
                  Int* testVar;
                  Int tmp_0;
                  Int tmp_1;

                  testVar = &tmp_0;
                  someNumber(&tmp_1);
                  *testVar = tmp_1;
                }

            ''',
        )

    def test_simple_func_1(self):
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  printInt(minusInt(666 99))
                  printNewLine()
                }
            ''',
            expected_output='''
                void start(void);

                void start(void) {
                  Int tmp_0;
                  Int const_0;
                  Int const_1;

                  const_0 = 666;
                  const_1 = 99;

                  minusInt(&tmp_0, &const_0, &const_1);
                  printInt(&tmp_0);
                  printNewLine();
                }

            ''',
            expected_stdout='567\n',
        )

    def test_simple_func_2(self):
        check_translation(
            test_case=self,
            input_string='''
                someNumber := func () -> Int {
                  return 99
                }
                start := func () {
                  printInt(minusInt(666 someNumber()))
                  printNewLine()
                }
            ''',
            expected_output='''
                void someNumber(Int* __result);
                void start(void);

                void someNumber(Int* __result) {
                  Int const_0;

                  const_0 = 99;

                  *__result = const_0;
                  return;
                }

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;
                  Int const_0;

                  const_0 = 666;

                  someNumber(&tmp_0);
                  minusInt(&tmp_1, &const_0, &tmp_0);
                  printInt(&tmp_1);
                  printNewLine();
                }

            ''',
            expected_stdout='567\n',
        )

    def test_simple_func_3(self):
        check_translation(
            test_case=self,
            input_string='''
                someNumber := func () -> Int {
                  return minusInt(100 1)
                }
                start := func () {
                  printInt(
                    minusInt(666 someNumber())
                  )
                  printNewLine()
                }
            ''',
            expected_output='''
                void someNumber(Int* __result);
                void start(void);

                void someNumber(Int* __result) {
                  Int tmp_0;
                  Int const_0;
                  Int const_1;

                  const_0 = 100;
                  const_1 = 1;

                  minusInt(&tmp_0, &const_0, &const_1);
                  *__result = tmp_0;
                  return;
                }

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;
                  Int const_0;

                  const_0 = 666;

                  someNumber(&tmp_0);
                  minusInt(&tmp_1, &const_0, &tmp_0);
                  printInt(&tmp_1);
                  printNewLine();
                }

            ''',
            expected_stdout='567\n',
        )

    def test_simple_func_4(self):
        check_translation(
            test_case=self,
            input_string='''
                someNumber := func (xxx:Int) -> Int {
                  return minusInt(100 xxx)
                }
                start := func () {
                  printInt(
                    minusInt(666 someNumber(1))
                  )
                  printNewLine()
                }
            ''',
            expected_output='''
                void someNumber(Int* __result, Int* xxx);
                void start(void);

                void someNumber(Int* __result, Int* xxx) {
                  Int tmp_0;
                  Int const_0;

                  const_0 = 100;

                  minusInt(&tmp_0, &const_0, xxx);
                  *__result = tmp_0;
                  return;
                }

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;
                  Int const_0;
                  Int const_1;

                  const_0 = 666;
                  const_1 = 1;

                  someNumber(&tmp_0, &const_1);
                  minusInt(&tmp_1, &const_0, &tmp_0);
                  printInt(&tmp_1);
                  printNewLine();
                }

            ''',
            expected_stdout='567\n',
        )

    def test_some_bug(self):
        ''' Process factorial function. '''
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                    printInt(fac())
                    printNewLine()
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
                  printInt(&tmp_0);
                  printNewLine();
                  fac(&tmp_1);
                }

                void fac(Int* __result) {
                  Int const_0;

                  const_0 = 1;

                  *__result = const_0;
                  return;
                }

            ''',
            expected_stdout='1\n',
        )

    def test_fib_1(self):
        ''' Process fib function. '''
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  printInt(fib(10))
                  printNewLine()
                }
                fib := func (n:Int) -> Int {
                  if isLessInt(n 2) {
                    return n
                  } else {
                    return plusInt (
                      fib(minusInt(n 1))
                      fib(minusInt(n 2))
                    )
                  }
                }
            ''',
            expected_output='''
                void start(void);
                void fib(Int* __result, Int* n);

                void start(void) {
                  Int tmp_0;
                  Int const_0;

                  const_0 = 10;

                  fib(&tmp_0, &const_0);
                  printInt(&tmp_0);
                  printNewLine();
                }

                void fib(Int* __result, Int* n) {
                  Int tmp_0;
                  Int tmp_1;
                  Int tmp_2;
                  Int tmp_3;
                  Int tmp_4;
                  Int tmp_5;
                  Int const_0;
                  Int const_1;
                  Int const_2;

                  const_0 = 2;
                  const_1 = 1;
                  const_2 = 2;

                  isLessInt(&tmp_0, n, &const_0);
                  if (tmp_0) {
                    *__result = *n;
                    return;
                  } else {
                    minusInt(&tmp_1, n, &const_1);
                    fib(&tmp_2, &tmp_1);
                    minusInt(&tmp_3, n, &const_2);
                    fib(&tmp_4, &tmp_3);
                    plusInt(&tmp_5, &tmp_2, &tmp_4);
                    *__result = tmp_5;
                    return;
                  }
                }

            ''',
            expected_stdout='55\n',
        )

    def test_factorial_1(self):
        ''' Process factorial function. '''
        check_translation(
            test_case=self,
            input_string='''
                start := func () {
                  printInt(fac(3))
                  printNewLine()
                }
                fac := func (n:Int) -> Int {
                  if isEqualInt(n 0) {
                    return 1
                  }
                  return multiplyInt(
                    fac(minusInt(n 1))
                    n
                  )
                }
            ''',
            expected_output='''
                void start(void);
                void fac(Int* __result, Int* n);

                void start(void) {
                  Int tmp_0;
                  Int const_0;

                  const_0 = 3;

                  fac(&tmp_0, &const_0);
                  printInt(&tmp_0);
                  printNewLine();
                }

                void fac(Int* __result, Int* n) {
                  Int tmp_0;
                  Int tmp_1;
                  Int tmp_2;
                  Int tmp_3;
                  Int const_0;
                  Int const_1;
                  Int const_2;

                  const_0 = 0;
                  const_1 = 1;
                  const_2 = 1;

                  isEqualInt(&tmp_0, n, &const_0);
                  if (tmp_0) {
                    *__result = const_1;
                    return;
                  }
                  minusInt(&tmp_1, n, &const_2);
                  fac(&tmp_2, &tmp_1);
                  multiplyInt(&tmp_3, &tmp_2, n);
                  *__result = tmp_3;
                  return;
                }

            ''',
            expected_stdout='6\n',
        )

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
