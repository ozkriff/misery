# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


'''
Miscellaneous classes and functions.
'''


import string


class PrettyPrinter(object):
    ''' Prettyprints values. '''

    def __init__(self, shiftwidth=4):
        self.shiftwidth = shiftwidth

    def pretty_print(self, node, indent_level):
        ''' Pretty print some value. '''

        indent = (' ' * self.shiftwidth) * indent_level
        next_indent = (' ' * self.shiftwidth) * (indent_level + 1)

        def _print_dict(node, indent_level):
            out = ''
            out += '{\n'
            for key in node.keys():
                value = node[key]
                out += next_indent + key + ': '
                out += self.pretty_print(value, indent_level + 1)
                out += '\n'
            out += indent + '}'
            return out

        def _print_list(node, indent_level):
            out = ''
            if len(node) > 0:
                out += '[\n'
                for value in node:
                    out += next_indent
                    out += self.pretty_print(value, indent_level + 1)
                    out += ',' + '\n'
                out += indent + ']'
            else:
                out += '[]'
            return out

        def _print_tuple(node, indent_level):
            out = ''
            out += '<TUPLE>(\n'
            for value in node:
                out += next_indent
                out += self.pretty_print(value, indent_level + 1)
                out += ',' + '\n'
            out += indent + ')'
            return out

        def _print_object(obj, indent_level):
            out = ''
            out += str(obj.__class__.__name__) + '('
            if len(obj.__dict__) == 0:
                out += ')'
            elif len(obj.__dict__) > 1:
                out += '\n'
                for key in obj.__dict__.keys():
                    value = obj.__dict__[key]
                    out += next_indent + key + '='
                    out += self.pretty_print(value, indent_level + 1)
                    out += ',' + '\n'
                out += indent + ')'
            else:
                for key in obj.__dict__.keys():
                    value = obj.__dict__[key]
                    out += key + '='
                    out += self.pretty_print(value, indent_level + 1) + ')'
            return out

        out = ''
        if isinstance(node, dict):
            out += _print_dict(node, indent_level)
        elif isinstance(node, list):
            out += _print_list(node, indent_level)
        elif isinstance(node, tuple):
            out += _print_tuple(node, indent_level)
        elif isinstance(node, str):
            out += '"' + node + '"'
        elif isinstance(node, int):
            out += str(node)
        elif isinstance(node, float):
            out += str(node)
        elif node is None:
            out = '<None>'
        else:
            out += _print_object(node, indent_level)
        return out


def pretty_print(node, shiftwidth=4):
    ''' Wrapper around PrettyPrinter.pretty_print. '''
    printer = PrettyPrinter(shiftwidth=shiftwidth)
    return printer.pretty_print(node, indent_level=0)


def diff(expected, real):
    ''' Returns string difference. '''
    import difflib
    expected_s = pretty_print(expected).split('\n')
    real_s = pretty_print(real).split('\n')
    unified_diff = difflib.unified_diff(expected_s, real_s, lineterm='')
    return '\n'.join(unified_diff)


def assert_equal(test_case, expected, real):
    ''' Wraps around test_case.assertEqual and misc.diff(). '''
    # print('\n' + pretty_print(expected))
    difference = diff(expected, real)
    if difference:
        test_case.fail('\n' + difference)
    # else:
    #     test_case.assertEqual(expected, real)


def assert_is_part_of(test_case, expected, real):
    if not is_part_of(expected, real):
        # test_case.fail('Not part of')
        # TODO: Remove some details from BIG diffs!
        difference = diff(expected, real)
        if difference:
            test_case.fail('Not part of:\n' + difference)


def flatten_tree(tree):
    def _flatten_tree(inlist, outlist):
        for node in inlist:
            if isinstance(node, str):
                outlist.append(node)
            elif isinstance(node, list):
                _flatten_tree(node, outlist)
            else:
                raise RuntimeError('flattenTree: bad type')
    outlist = []
    _flatten_tree(tree, outlist)
    return outlist


def is_part_of(expected, real):
    '''
    Checks if 'real' contains at least everything that 'expected' contains.
    '''
    if isinstance(expected, list):
        for value1 in expected:
            found = False
            for value2 in real:
                if is_part_of(value1, value2):
                    found = True
                    break
            if not found:
                return False
        return True
    elif isinstance(expected, dict):
        for key in expected.keys():
            if key not in real:
                return False
            elif not is_part_of(expected[key], real[key]):
                return False
        return True
    elif isinstance(expected, (str, int, float)):
        return expected == real
    elif expected is None:
        return real is None
    else:
        # some object
        for key in expected.__dict__.keys():
            if not key in real.__dict__.keys():
                return False
            expected_value = expected.__dict__[key]
            real_value = real.__dict__[key]
            if not is_part_of(expected_value, real_value):
                return False
        return True


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
