# -*- coding: utf-8 -*-


'''
Miscellaneous classes and functions.
'''


def pretty_print(node, indent_level=0, shiftwidth=4):
    '''
    Pretty print some variable
    '''
    indent = (' ' * shiftwidth) * indent_level
    next_indent = (' ' * shiftwidth) * (indent_level + 1)

    def print_dict(node, indent_level=0, shiftwidth=4):
        out = ''
        out += '{\n'
        for key in node.keys():
            value = node[key]
            out += next_indent + key + ': ' + pretty_print(
                    value, indent_level + 1, shiftwidth) + '\n'
        out += indent + '}'
        return out

    def print_list(node, indent_level=0, shiftwidth=4):
        out = ''
        if len(node) > 0:
            out += '[\n'
            for value in node:
                out += next_indent
                out += pretty_print(value, indent_level + 1, shiftwidth)
                out += ',' + '\n'
            out += indent + ']'
        else:
            out += '[]'
        return out

    def print_tuple(node, indent_level=0, shiftwidth=4):
        out = ''
        out += '<TUPLE>(\n'
        for value in node:
            out += next_indent
            out += pretty_print(value, indent_level + 1, shiftwidth)
            out += ',' + '\n'
        out += indent + ')'
        return out

    def print_object(obj, indent_level=0, shiftwidth=4):
        out = ''
        out += str(obj.__class__.__name__) + '('
        if len(obj.__dict__) == 0:
            out += ')'
        elif len(obj.__dict__) > 1:
            out += '\n'
            for key in obj.__dict__.keys():
                value = obj.__dict__[key]
                out += next_indent + key + '='
                out += pretty_print(value, indent_level + 1, shiftwidth)
                out += ',' + '\n'
            out += indent + ')'
        else:
            for key in obj.__dict__.keys():
                value = obj.__dict__[key]
                out += key + '='
                out += pretty_print(value, indent_level + 1, shiftwidth) + ')'
        return out

    out = ''
    if isinstance(node, dict):
        out += print_dict(node, indent_level, shiftwidth)
    elif isinstance(node, list):
        out += print_list(node, indent_level, shiftwidth)
    elif isinstance(node, tuple):
        out += print_tuple(node, indent_level, shiftwidth)
    elif isinstance(node, str):
        out += '"' + node + '"'
    elif isinstance(node, int):
        out += str(node)
    elif isinstance(node, float):
        out += str(node)
    elif node is None:
        out = '<None>'
    else:
        out += print_object(node, indent_level, shiftwidth)
    return out


def diff(expected, real):
    '''Returns string difference'''
    import difflib
    expected_s = pretty_print(expected).split('\n')
    real_s = pretty_print(real).split('\n')
    unified_diff = difflib.unified_diff(expected_s, real_s, lineterm='')
    return '\n'.join(unified_diff)


def assert_equal(test_case, expected_ast, real_ast):
    # print('\n' + pretty_print(expected_ast))
    difference = diff(expected_ast, real_ast)
    if difference:
        test_case.fail('\n' + difference)
    else:
        test_case.assertEqual(expected_ast, real_ast)

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
