# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'misc' module. '''


import unittest
from misery import (
    misc,
)


class TestDiff(unittest.TestCase):
    ''' Test misc.diff func. '''

    def test_lists(self):
        ''' Diff lists. '''
        list1 = [1, 2, 3, 4, 5]
        list2 = [1, 2, 0, 0, 5]
        real_output = misc.diff(list1, list2)
        expected_output = (
            '--- \n'
            '+++ \n'
            '@@ -1,7 +1,7 @@\n'
            ' [\n'
            '     1,\n'
            '     2,\n'
            '-    3,\n'
            '-    4,\n'
            '+    0,\n'
            '+    0,\n'
            '     5,\n'
            ' ]'
        )
        self.assertEqual(expected_output, real_output)


class TestPrettyPrinter(unittest.TestCase):
    ''' Test misc.pretty_print func. '''

    def test_none(self):
        ''' Print None. '''
        input_data = None
        expected_output = '<None>'
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_empty_list(self):
        ''' Print empty list. '''
        input_data = []
        expected_output = '[]'
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_simple_list(self):
        ''' Print simple list. '''
        input_data = [1, 2, 3]
        expected_output = (
            '[\n'
            '    1,\n'
            '    2,\n'
            '    3,\n'
            ']'
        )
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_empty_map(self):
        ''' Print empty map. '''
        input_data = {}
        expected_output = '{\n}'
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_map_1(self):
        ''' Print map with one field. '''
        input_data = {'field': 1}
        expected_output = (
            '{\n'
            '    field: 1\n'
            '}'
        )
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_map_2(self):
        ''' Print map with two fields. '''
        input_data = {'1': 1, '2': 2}
        expected_output = (
            '{\n'
            '    1: 1\n'
            '    2: 2\n'
            '}'
        )
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_empty_tuple(self):
        ''' Print empty tuple. '''
        input_data = ()
        expected_output = (
            '<TUPLE>(\n'
            ')'
        )
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_simple_tuple(self):
        ''' Print simple tuple. '''
        input_data = (1, 2, 3)
        expected_output = (
            '<TUPLE>(\n'
            '    1,\n'
            '    2,\n'
            '    3,\n'
            ')'
        )
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_string(self):
        ''' Print string. '''
        input_data = 'hi'
        expected_output = '\"hi\"'
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_float(self):
        ''' Print floating point number. '''
        input_data = 1.1
        expected_output = '1.1'
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_empty_object(self):
        ''' Print object wothout fields. '''
        class TestClass:
            def __init__(self):
                pass
        input_data = TestClass()
        expected_output = 'TestClass()'
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_object_with_one_field(self):
        ''' Print object wothout fields. '''
        class TestClass:
            def __init__(self):
                self.field = 0
        input_data = TestClass()
        input_data.field = 1
        expected_output = 'TestClass(field=1)'
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_object_with_two_field(self):
        ''' Print object wothout fields. '''
        class TestClass:
            def __init__(self):
                self.field1 = 0
                self.field2 = 0
        input_data = TestClass()
        input_data.field1 = 1
        input_data.field2 = 'hi'
        expected_output = (
            'TestClass(\n'
            '    field1=1,\n'
            '    field2=\"hi\",\n'
            ')'
        )
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)


class TestCaseMock:

    def __init__(self):
        self.is_ok = True

    def assertEqual(self, expected, real):
        return expected == real

    def fail(self, msg=''):
        self.is_ok = False


class TestAssertEqual(unittest.TestCase):
    ''' Test misc.assert_equal func. '''

    def test_failed(self):
        ''' Test failed. '''
        mock = TestCaseMock()
        misc.assert_equal(mock, 1, 2)
        self.assertEqual(mock.is_ok, False)

    def test_passed(self):
        ''' Test passed. '''
        mock = TestCaseMock()
        misc.assert_equal(mock, 1, 1)
        self.assertEqual(mock.is_ok, True)

    def test_passed_2(self):
        ''' Test passed. '''
        mock = TestCaseMock()
        mock.assertEqual(1, 1)
        self.assertEqual(mock.is_ok, True)


class TestGetCallerFuncName(unittest.TestCase):

    def test_check_caller_name(self):
        def helper_func():
            self.assertEqual(
                'test_check_caller_name',
                misc.get_caller_func_name(),
            )
        helper_func()


class TestFlattenTree(unittest.TestCase):
    ''' TestSuite for misc.flatten_tree() func. '''

    def test_simple(self):
        ''' Basic misc.flatten_tree() test. '''
        input_list = [
            [
                '1',
                '2',
            ],
            [[['3']]],
            '4'
        ]
        real_output = misc.flatten_tree(input_list)
        expected_output = ['1', '2', '3', '4']
        misc.assert_equal(self, expected_output, real_output)

    def test_bad_node_type_error(self):
        input_list = ['1', '2', 3, '4']
        self.assertRaisesRegexp(
            Exception,
            'Bad node type: .*int',
            misc.flatten_tree,
            input_list,
        )


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
