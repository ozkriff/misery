# -*- coding: utf-8 -*-


''' Test 'misc' module. '''


import unittest
import misc


class TestDiff(unittest.TestCase):
    ''' Test misc.diff function. '''

    def test_1(self):
        ''' Diff two lines. '''
        pass


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

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
