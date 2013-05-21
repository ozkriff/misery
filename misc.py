# -*- coding: utf-8 -*-


def pretty_print(node, indent=0, shiftwidth=4):
    def print_dict(dict, indent=0, shiftwidth=4):
        out = ''
        out += '{\n'
        for key in dict.keys():
            value = dict[key]
            out += i2 + key + ': ' + pretty_print(
                    value, indent + 1, shiftwidth) + '\n'
        out += i + '}'
        return out

    def print_list(list, indent=0, shiftwidth=4):
        out = ''
        if len(list) > 0:
            out += '[\n'
            for value in list:
                pp = pretty_print(value, indent + 1, shiftwidth)
                out += i2 + pp + ',' + '\n'
            out += i + ']'
        else:
            out += '[]'
        return out

    def print_tuple(tuple, indent=0, shiftwidth=4):
        out = ''
        out += '<TUPLE>(\n'
        for value in tuple:
            pp = pretty_print(value, indent + 1, shiftwidth)
            out += i2 + pp + ',' + '\n'
        out += i + ')'
        return out

    def print_object(object, indent=0, shiftwidth=4):
        out = ''
        out += str(object.__class__.__name__) + '('
        if len(object.__dict__) == 0:
            out += ')'
        elif len(object.__dict__) > 1:
            out += '\n'
            for key in object.__dict__.keys():
                value = object.__dict__[key]
                out += i2 + key + '='
                out += pretty_print(value, indent + 1, shiftwidth)
                out += ',' + '\n'
            out += i + ')'
        else:
            for key in object.__dict__.keys():
                value = object.__dict__[key]
                out += key + '='
                out += pretty_print(value, indent + 1, shiftwidth) + ')'
        return out

    out = ''
    i = (' ' * shiftwidth) * indent
    i2 = (' ' * shiftwidth) * (indent + 1)
    if isinstance(node, dict):
        out += print_dict(node, indent, shiftwidth)
    elif isinstance(node, list):
        out += print_list(node, indent, shiftwidth)
    elif isinstance(node, tuple):
        out += print_tuple(node, indent, shiftwidth)
    elif isinstance(node, str):
        out += '"' + node + '"'
    elif isinstance(node, int):
        out += str(node)
    elif isinstance(node, float):
        out += str(node)
    elif node is None:
        out = '<None>'
    else:
        out += print_object(node, indent, shiftwidth)
    return out


def diff(expected, real):
    import difflib
    expected_s = pretty_print(expected).split('\n')
    real_s = pretty_print(real).split('\n')
    # d = difflib.Differ()
    # result = list(d.compare(expected_s, real_s))
    # for out in result: print(out)
    diff = difflib.unified_diff(expected_s, real_s, lineterm='')
    out = '\n'.join(diff)
    return out


def assert_equal(test_case, expected_ast, real_ast):
    # print('\n' + pretty_print(expected_ast))
    d = diff(expected_ast, real_ast)
    if d:
        test_case.fail('\n' + d)
    else:
        test_case.assertEqual(expected_ast, real_ast)

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
