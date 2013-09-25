# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Funcal tests. '''


import unittest
import subprocess
import os
import sys
import textwrap
from misery import (
    misc,
    generator,
    parse,
    datatype,
    ident_table,
)


def get_generator(input_mis_code):
    ast_ = parse.make_parser().parse(
        input_mis_code,
        lexer=parse.make_lexer(),
    )
    ast_.ident_list = ident_table.ident_table(ast_)
    ast_ = datatype.mark_out_datatypes(ast_=ast_)
    generator_ = generator.Generator(ast_=ast_)
    return generator_


def translate_mis_to_c(input_mis_code):
    ''' Helper func, compiles program in Mis to program in C. '''
    real_output = get_generator(input_mis_code).generate()
    return real_output


def translate_mis_to_c_and_write_to_file(input_mis_code, filename='out.c'):
    ''' Translate to full C version and write to file. '''
    with open(filename, 'w') as f:
        f.write(get_generator(input_mis_code).generate_full())


def try_to_compile_and_run_file(
    test_case,
    c_file_name,
    input_mis_code,
    expected_stdout,
):
    # translate mis to ANSI C and write to file
    translate_mis_to_c_and_write_to_file(
        input_mis_code=input_mis_code,
        filename=c_file_name,
    )

    if sys.platform == 'win32':
        exe_file_name = c_file_name.replace('.c', '.exe')
    else:
        exe_file_name = c_file_name.replace('.c', '')

    # compile c code with c compiler
    compiler_proc = subprocess.Popen(
        ['tcc', c_file_name, '-o', exe_file_name],
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
    if sys.platform == 'win32':
        cmd = [exe_file_name]
    else:
        cmd = ['./' + exe_file_name]
    proc = subprocess.Popen(
        cmd,
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
    input_mis_code,
    expected_c_code,
    expected_stdout='',
):
    ''' Small helper func. '''
    real_output = translate_mis_to_c(textwrap.dedent(input_mis_code))
    misc.assert_equal(test_case, textwrap.dedent(expected_c_code), real_output)
    c_file_name = misc.get_caller_func_name().replace('test_', '') + '_out.c'
    try_to_compile_and_run_file(
        test_case,
        c_file_name,
        input_mis_code,
        expected_stdout,
    )


class TestTranslator(unittest.TestCase):

    def test_var_decl_with_integer_literal(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                  testVar ::= 1
                  testVar = 2
                }
            ''',
            expected_c_code='''
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

    def test_integer_var_decl_with_constructor(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                  testVar := Int(1)
                  print(testVar)
                  printNewLine()
                }
            ''',
            expected_c_code='''
                void start(void);

                void start(void) {
                  Int* testVar;
                  Int tmp_0;
                  Int const_0;

                  const_0 = 1;

                  Int_Int_init(&tmp_0, &const_0);
                  testVar = &tmp_0;
                  print_Int(testVar);
                  printNewLine();
                }

            ''',
            expected_stdout='1\n',
        )

    def test_struct(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                struct MyStruct {
                  field1 Int
                  field2 Int
                }
                func start () {
                  t := MyStruct()
                }
            ''',
            expected_c_code='''
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

                  MyStruct_init(&tmp_0);
                  t = &tmp_0;
                }

            ''',
        )

    def test_struct_as_func_arg(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                struct MyStruct {
                  field1 Int
                  field2 Int
                }
                func someFunc (x MyStruct) -> MyStruct{
                  return x
                }
                func start () {
                  t := MyStruct()
                  t2 := someFunc(t)
                }
            ''',
            expected_c_code='''
                typedef struct MyStruct MyStruct;
                void someFunc_MyStruct(MyStruct* __result, MyStruct* x);
                void start(void);

                struct MyStruct {
                  Int field1;
                  Int field2;
                };

                void MyStruct_init(MyStruct* __result) {
                  /* todo */
                }

                void someFunc_MyStruct(MyStruct* __result, MyStruct* x) {
                  *__result = *x;
                  return;
                }

                void start(void) {
                  MyStruct* t;
                  MyStruct* t2;
                  MyStruct tmp_0;
                  MyStruct tmp_1;

                  MyStruct_init(&tmp_0);
                  t = &tmp_0;
                  someFunc_MyStruct(&tmp_1, t);
                  t2 = &tmp_1;
                }

            ''',
        )

    def test_var_decl_with_string_literal(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                  testVar ::= "some string"
                }
            ''',
            expected_c_code='''
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
            input_mis_code='''
                func start () {
                  print("hello")
                  printNewLine()
                }
            ''',
            expected_c_code='''
                void start(void);

                void start(void) {
                  String const_0;

                  const_0 = "hello";

                  print_String(&const_0);
                  printNewLine();
                }

            ''',
            expected_stdout='hello\n',
        )

    def test_print_string_var(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                  testVar ::= "print this to console, please"
                  print(testVar)
                  printNewLine()
                }
            ''',
            expected_c_code='''
                void start(void);

                void start(void) {
                  String* testVar;
                  String tmp_0;
                  String const_0;

                  const_0 = "print this to console, please";

                  testVar = &tmp_0;
                  *testVar = const_0;
                  print_String(testVar);
                  printNewLine();
                }

            ''',
            expected_stdout='print this to console, please\n',
        )

    def test_basic_assignment_of_integer_literal(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                  testVar ::= 1 testVar = 2
                }
            ''',
            expected_c_code='''
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
            input_mis_code='''
                func start () {
                  i ::= 0
                  for isLess(i 5) {
                    print(i)
                    printNewLine()
                    i = plus(i 1)
                  }
                }
            ''',
            expected_c_code='''
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
                    isLess_Int_Int(&tmp_1, i, &const_1);
                    if (!tmp_1) {
                      break;
                    }
                    print_Int(i);
                    printNewLine();
                    plus_Int_Int(&tmp_2, i, &const_2);
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

    def test_var_decl_with_func_call_returning_string(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func someString () -> String {
                  return "hi"
                }
                func start () {
                  s ::= someString()
                  print(s)
                  printNewLine()
                }
            ''',
            expected_c_code='''
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
                  print_String(s);
                  printNewLine();
                }

            ''',
            expected_stdout='hi\n',
        )

    def test_nested_func_calls_with_strings(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func someString () -> String {
                  return "hi"
                }
                func start () {
                  print(someString())
                  printNewLine()
                }
            ''',
            expected_c_code='''
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
                  print_String(&tmp_0);
                  printNewLine();
                }

            ''',
            expected_stdout='hi\n',
        )

    def test_var_decl_with_func_call_returning_integer(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func someNumber () -> Int {
                  return 99
                }
                func start () {
                  testVar ::= someNumber()
                }
            ''',
            expected_c_code='''
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
            input_mis_code='''
                func start () {
                  print(minus(666 99))
                  printNewLine()
                }
            ''',
            expected_c_code='''
                void start(void);

                void start(void) {
                  Int tmp_0;
                  Int const_0;
                  Int const_1;

                  const_0 = 666;
                  const_1 = 99;

                  minus_Int_Int(&tmp_0, &const_0, &const_1);
                  print_Int(&tmp_0);
                  printNewLine();
                }

            ''',
            expected_stdout='567\n',
        )

    def test_simple_func_2(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func someNumber () -> Int {
                  return 99
                }
                func start () {
                  print(minus(666 someNumber()))
                  printNewLine()
                }
            ''',
            expected_c_code='''
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
                  minus_Int_Int(&tmp_1, &const_0, &tmp_0);
                  print_Int(&tmp_1);
                  printNewLine();
                }

            ''',
            expected_stdout='567\n',
        )

    def test_simple_func_3(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func someNumber () -> Int {
                  return minus(100 1)
                }
                func start () {
                  print(
                    minus(666 someNumber())
                  )
                  printNewLine()
                }
            ''',
            expected_c_code='''
                void someNumber(Int* __result);
                void start(void);

                void someNumber(Int* __result) {
                  Int tmp_0;
                  Int const_0;
                  Int const_1;

                  const_0 = 100;
                  const_1 = 1;

                  minus_Int_Int(&tmp_0, &const_0, &const_1);
                  *__result = tmp_0;
                  return;
                }

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;
                  Int const_0;

                  const_0 = 666;

                  someNumber(&tmp_0);
                  minus_Int_Int(&tmp_1, &const_0, &tmp_0);
                  print_Int(&tmp_1);
                  printNewLine();
                }

            ''',
            expected_stdout='567\n',
        )

    def test_simple_func_4(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func someNumber (xxx Int) -> Int {
                  return minus(100 xxx)
                }
                func start () {
                  print(
                    minus(666 someNumber(1))
                  )
                  printNewLine()
                }
            ''',
            expected_c_code='''
                void someNumber_Int(Int* __result, Int* xxx);
                void start(void);

                void someNumber_Int(Int* __result, Int* xxx) {
                  Int tmp_0;
                  Int const_0;

                  const_0 = 100;

                  minus_Int_Int(&tmp_0, &const_0, xxx);
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

                  someNumber_Int(&tmp_0, &const_1);
                  minus_Int_Int(&tmp_1, &const_0, &tmp_0);
                  print_Int(&tmp_1);
                  printNewLine();
                }

            ''',
            expected_stdout='567\n',
        )

    def test_some_bug(self):
        ''' Process factorial func. '''
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                    print(fac())
                    printNewLine()
                    fac()
                }
                func fac () -> Int {
                    return 1
                }
            ''',
            expected_c_code='''
                void start(void);
                void fac(Int* __result);

                void start(void) {
                  Int tmp_0;
                  Int tmp_1;

                  fac(&tmp_0);
                  print_Int(&tmp_0);
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

    def test_two_vars_for_one_memory_location(self):
        ''' Try to create two variables for one memory location. '''
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                    a := Int(1)
                    print(a)
                    printNewLine()
                    b := a
                    print(b)
                    printNewLine()
                    b = 2
                    print(a)
                    printNewLine()
                }
            ''',
            expected_c_code='''
                void start(void);

                void start(void) {
                  Int* a;
                  Int* b;
                  Int tmp_0;
                  Int const_0;
                  Int const_1;

                  const_0 = 1;
                  const_1 = 2;

                  Int_Int_init(&tmp_0, &const_0);
                  a = &tmp_0;
                  print_Int(a);
                  printNewLine();
                  b = a;
                  print_Int(b);
                  printNewLine();
                  *b = const_1;
                  print_Int(a);
                  printNewLine();
                }

            ''',
            expected_stdout=(
                '1\n'
                '1\n'
                '2\n'
            ),
        )

    def test_func_overloading_1(self):
        check_translation(
            test_case=self,
            input_mis_code='''
                func pr(n Int) {
                  print(n)
                }
                func pr(s String) {
                  print(s)
                }
                func start () {
                  pr(1)
                  printNewLine()
                  pr("str")
                  printNewLine()
                }
            ''',
            expected_c_code='''
                void pr_Int(Int* n);
                void pr_String(String* s);
                void start(void);

                void pr_Int(Int* n) {
                  print_Int(n);
                }

                void pr_String(String* s) {
                  print_String(s);
                }

                void start(void) {
                  Int const_0;
                  String const_1;

                  const_0 = 1;
                  const_1 = "str";

                  pr_Int(&const_0);
                  printNewLine();
                  pr_String(&const_1);
                  printNewLine();
                }

            ''',
            expected_stdout=(
                '1\n'
                'str\n'
            ),
        )

    def test_return_reference_1(self):
        ''' Return reference to allocated on heap memory. '''
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                  a := allocInt()
                  print(a)
                  printNewLine()
                  a = 1
                  print(a)
                  printNewLine()
                }
            ''',
            expected_c_code='''
                void start(void);

                void start(void) {
                  Int* a;
                  Int* tmp_0;
                  Int const_0;

                  const_0 = 1;

                  allocInt(&tmp_0);
                  a = tmp_0;
                  print_Int(a);
                  printNewLine();
                  *a = const_0;
                  print_Int(a);
                  printNewLine();
                }

            ''',
            expected_stdout=(
                '0\n'
                '1\n'
            ),
        )

    def test_fib_1(self):
        ''' Process fib func. '''
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                  print(fib(10))
                  printNewLine()
                }
                func fib (n Int) -> Int {
                  if isLess(n 2) {
                    return n
                  } else {
                    return plus (
                      fib(minus(n 1))
                      fib(minus(n 2))
                    )
                  }
                }
            ''',
            expected_c_code='''
                void start(void);
                void fib_Int(Int* __result, Int* n);

                void start(void) {
                  Int tmp_0;
                  Int const_0;

                  const_0 = 10;

                  fib_Int(&tmp_0, &const_0);
                  print_Int(&tmp_0);
                  printNewLine();
                }

                void fib_Int(Int* __result, Int* n) {
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

                  isLess_Int_Int(&tmp_0, n, &const_0);
                  if (tmp_0) {
                    *__result = *n;
                    return;
                  } else {
                    minus_Int_Int(&tmp_1, n, &const_1);
                    fib_Int(&tmp_2, &tmp_1);
                    minus_Int_Int(&tmp_3, n, &const_2);
                    fib_Int(&tmp_4, &tmp_3);
                    plus_Int_Int(&tmp_5, &tmp_2, &tmp_4);
                    *__result = tmp_5;
                    return;
                  }
                }

            ''',
            expected_stdout='55\n',
        )

    def test_factorial_1(self):
        ''' Process factorial func. '''
        check_translation(
            test_case=self,
            input_mis_code='''
                func start () {
                  print(fac(3))
                  printNewLine()
                }
                func fac (n Int) -> Int {
                  if isEqual(n 0) {
                    return 1
                  }
                  return multiply(
                    fac(minus(n 1))
                    n
                  )
                }
            ''',
            expected_c_code='''
                void start(void);
                void fac_Int(Int* __result, Int* n);

                void start(void) {
                  Int tmp_0;
                  Int const_0;

                  const_0 = 3;

                  fac_Int(&tmp_0, &const_0);
                  print_Int(&tmp_0);
                  printNewLine();
                }

                void fac_Int(Int* __result, Int* n) {
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

                  isEqual_Int_Int(&tmp_0, n, &const_0);
                  if (tmp_0) {
                    *__result = const_1;
                    return;
                  }
                  minus_Int_Int(&tmp_1, n, &const_2);
                  fac_Int(&tmp_2, &tmp_1);
                  multiply_Int_Int(&tmp_3, &tmp_2, n);
                  *__result = tmp_3;
                  return;
                }

            ''',
            expected_stdout='6\n',
        )

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
