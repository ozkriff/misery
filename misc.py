# -*- coding: utf-8 -*-

def my_pretty_print(node, indent=0, shiftwidth=4):
    out = ''
    i = (' ' * shiftwidth) * indent
    i2 = (' ' * shiftwidth) * (indent + 1)
    if isinstance(node, dict):
        out += '{\n'
        for key in node.keys():
            value = node[key]
            out += i2 + key + ': ' + my_pretty_print(
                    value, indent + 1, shiftwidth) + '\n'
        out += i + '}'
    elif isinstance(node, list):
        if len(node) > 0:
            out += '[\n'
            for value in node:
                pp = my_pretty_print(value, indent + 1, shiftwidth)
                out += i2 + pp + ',' + '\n'
            out += i + ']'
        else:
            out += '[]'
    elif isinstance(node, tuple):
        out += '<TUPLE>(\n'
        for value in node:
            pp = my_pretty_print(value, indent + 1, shiftwidth)
            out += i2 + pp + ',' + '\n'
        out += i + ')'
    elif isinstance(node, str):
        out += '"' + node + '"'
    elif isinstance(node, int):
        out += str(node)
    elif isinstance(node, float):
        out += str(node)
    elif node is None:
        out = '<None>'
    else:
        out += str(node.__class__.__name__) + '('
        if len(node.__dict__) == 0:
            out += ')'
        elif len(node.__dict__) > 1:
            out += '\n'
            for key in node.__dict__.keys():
                value = node.__dict__[key]
                out += i2 + key + '='
                out += my_pretty_print(value, indent + 1, shiftwidth)
                out += ',' + '\n'
            out += i + ')'
        else:
            for key in node.__dict__.keys():
                value = node.__dict__[key]
                out += key + '='
                out += my_pretty_print(value, indent + 1, shiftwidth) + ')'
    return out


def my_diff(expected, real):
    import difflib
    expected_s = my_pretty_print(expected).split('\n')
    real_s = my_pretty_print(real).split('\n')
    # d = difflib.Differ()
    # result = list(d.compare(expected_s, real_s))
    # for out in result: print(out)
    diff = difflib.unified_diff(expected_s, real_s, lineterm='')
    out = '\n'.join(diff)
    return out


# TODO: rename
def my_assert_equal(test_case, expected_ast, real_ast):
    # print('\n' + my_pretty_print(expected_ast))
    diff = my_diff(expected_ast, real_ast)
    if diff:
        test_case.fail('\n' + diff)
    else:
        test_case.assertEqual(expected_ast, real_ast)

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
