# -*- coding: utf-8 -*-


import unittest
import misc


class TestDiff(unittest.TestCase):

    def test_1(self):
        pass

class TestPrettyPrinter(unittest.TestCase):

    def test_none(self):
        input = None
        expected_output = '<None>'
        real_output = misc.pretty_print(input)
        self.assertEqual(expected_output, real_output)

    def test_empty_list(self):
        input = []
        expected_output = '[]'
        real_output = misc.pretty_print(input)
        self.assertEqual(expected_output, real_output)
        
    def test_empty_map(self):
        input = {}
        expected_output = '{\n}'
        real_output = misc.pretty_print(input)
        self.assertEqual(expected_output, real_output)


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
