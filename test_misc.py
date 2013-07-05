# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


''' Test 'misc' module. '''


import unittest
import misc


# TODO: Add more tests!
class TestDiff(unittest.TestCase):
    ''' Test misc.diff function. '''

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
    ''' Test misc.pretty_print function. '''

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
            pass
        input_data = TestClass()
        expected_output = 'TestClass()'
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_object_with_one_field(self):
        ''' Print object wothout fields. '''
        class TestClass:
            pass
        input_data = TestClass()
        input_data.field1 = 1
        expected_output = 'TestClass(field1=1)'
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)

    def test_object_with_two_field(self):
        ''' Print object wothout fields. '''
        class TestClass:
            pass
        input_data = TestClass()
        input_data.field1 = 1
        input_data.field2 = 'hi'
        expected_output = (
            'TestClass(\n'
            '    field2=\"hi\",\n'
            '    field1=1,\n'
            ')'
        )
        real_output = misc.pretty_print(input_data)
        self.assertEqual(expected_output, real_output)


class TestAssertEqual(unittest.TestCase):
    ''' Test misc.assert_equal function. '''

    class TestCaseMock:

        def __init__(self):
            self.is_ok = True

        def assertEqual(self, expected, real):
            return expected == real

        def fail(self, diff):
            if diff:
                self.is_ok = False

    def test_failed(self):
        ''' Test failed. '''
        mock = self.TestCaseMock()
        misc.assert_equal(mock, 1, 2)
        self.assertEqual(mock.is_ok, False)

    def test_passed(self):
        ''' Test failed. '''
        mock = self.TestCaseMock()
        misc.assert_equal(mock, 1, 1)
        self.assertEqual(mock.is_ok, True)


class TestIsPartOf(unittest.TestCase):

    def test_same_numbers(self):
        self.assertTrue(misc.is_part_of(1, 1))

    def test_different_numbers(self):
        self.assertFalse(misc.is_part_of(1, 2))

    def test_list_3(self):
        self.assertTrue(misc.is_part_of([], []))

    def test_list_4(self):
        self.assertTrue(misc.is_part_of([], [1]))

    def test_list_5(self):
        self.assertTrue(misc.is_part_of([1, 2, 3], [1, 2, 3]))

    def test_list_6(self):
        self.assertTrue(misc.is_part_of(
            [1, 2, 3],
            [1, 1.5, 2, 2.5, 3],
        ))

    def test_list_7(self):
        self.assertFalse(misc.is_part_of(
            [1, 1.5, 2, 2.5, 3],
            [1, 2, 3],
        ))

    def test_map_1(self):
        self.assertTrue(misc.is_part_of({}, {}))

    def test_map_2(self):
        self.assertTrue(misc.is_part_of({'key1': 1}, {'key1': 1}))

    def test_map_3(self):
        self.assertTrue(misc.is_part_of({'key1': 1}, {'key1': 1, 'key2': 2}))

    def test_map_4(self):
        self.assertFalse(misc.is_part_of({'key1': 1, 'key2': 2}, {'key1': 1}))

    def test_map_5(self):
        self.assertTrue(misc.is_part_of(
            {'key1': {'key2': 2}},
            {'key1': {'key2': 2, 'key3': 3}},
        ))

    class SimpleObject:
        pass

    def test_object_1(self):
        a = self.SimpleObject()
        b = self.SimpleObject()
        b.someField = 1
        self.assertTrue(misc.is_part_of(a, b))

    def test_object_2(self):
        a = self.SimpleObject()
        a.someField = 1
        b = self.SimpleObject()
        self.assertFalse(misc.is_part_of(a, b))

    def test_object_3(self):
        a = self.SimpleObject()
        a.someField = [1, 2, 3]
        b = self.SimpleObject()
        b.someField = [1, 2, 3, 4]
        b.someField2 = 1
        self.assertTrue(misc.is_part_of(a, b))


class TestFlattenTree(unittest.TestCase):
    ''' TestSuite for misc.flatten_tree() function. '''

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


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
