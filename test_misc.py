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


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
