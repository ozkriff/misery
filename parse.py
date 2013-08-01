# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import ast
import ply.yacc
import ply.lex


reserved = {
    'func': 'FUNC',
    'if': 'IF',
    'else': 'ELSE',
    'import': 'IMPORT',
    'const': 'CONST',
    'type': 'TYPE',
    'struct': 'STRUCT',
    'for': 'FOR',
    'return': 'RETURN',
}


tokens = [
    'IDENTIFIER',
    'STRING',
    'NUMBER',
    'ASSIGN',
    'COLONASSIGN',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    # 'COMMA',
    'COLON',
    'ARROW',
    # 'DOT',
] + list(reserved.values())


def find_column(input, lexpos):
    '''Compute column.

    input is the input text string
    lexpos is a lexem position
    '''
    last_cr = input.rfind('\n', 0, lexpos)
    if last_cr < 0:
        last_cr = 0
    else:
        last_cr += 1
    column = (lexpos - last_cr)
    return column


def make_lexer():

    t_ARROW = r'->'
    t_ASSIGN = r'='
    t_COLONASSIGN = r':='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    # t_COMMA = r','
    t_COLON = r':'
    # t_DOT = r'\.'
    t_STRING = r'"[^"]*"'

    def t_IDENTIFIER(t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = reserved.get(t.value, 'IDENTIFIER')
        return t

    # TODO: float?
    def t_NUMBER(t):
        r'-?\d+'
        t.value = int(t.value)
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    t_ignore_COMMENT = r'\#.*'

    def t_error(t):
        column = find_column(t.lexer.lexdata, t.lexpos)
        errormsg = (
            'filename:[%(lineno)d:%(column)d: '
            'Lexer error: Illegal character...'
        )
        print(errormsg % {
            'lineno': t.lineno - 1,
            'column': column - 1,
        })
        print('  ' + t.lexer.lexdata.split('\n')[t.lineno - 1])
        print('  ' + (' ' * (column - 1)) + '^')
        t.lexer.skip(1)

    # Build the lexer from my environment and return it
    return ply.lex.lex()


def make_parser():

    def p_module(p):
        'module : import_list declaration_sequence'
        p[0] = ast.Module(import_list=p[1], declaration_sequence=p[2])

    # def p_qualifiedIdentifier(p):
    #     'qualifiedIdentifier : IDENTIFIER'
    #     p[0] = p[1]
    #     p[0] = {'_type': 'qualifiedIdentifier', 'identifiers': []}

    # def p_qualifiedIdentifier_2(p):
    #     'qualifiedIdentifier : qualifiedIdentifier DOT IDENTIFIER'
    #     p[1]['identifiers'].amy_pretty_printend(p[3])
    #     p[0] = p[1]

    def p_import_list_empty(p):
        'import_list :'
        p[0] = None

    def p_import_list(p):
        'import_list : IMPORT LCURLY import_sequence RCURLY'
        p[0] = p[3]

    def p_import_sequence_empty(p):
        'import_sequence :'
        p[0] = []

    def p_import_sequence(p):
        'import_sequence : import_sequence IDENTIFIER'
        p[1].append(p[2])
        p[0] = p[1]

    def p_declaration_sequence_empty(p):
        'declaration_sequence :'
        p[0] = []

    def p_declaration_sequence(p):
        'declaration_sequence : declaration_sequence declaration'
        p[1].append(p[2])
        p[0] = p[1]

    def p_block(p):
        'block : LCURLY statement_sequence RCURLY'
        p[0] = p[2]

    def p_block_2(p):
        'block : LCURLY statement_sequence RETURN RCURLY'
        p[2].append(ast.Return(expression=None))
        p[0] = p[2]

    def p_block_3(p):
        'block : LCURLY statement_sequence RETURN expression RCURLY'
        p[2].append(ast.Return(expression=p[4]))
        p[0] = p[2]

    def p_function_interface(p):
        'function_interface : LPAREN parameter_list RPAREN ARROW type'
        p[0] = ast.FunctionInterface(parameter_list=p[2], return_type=p[5])

    def p_function_interface_without_return_type(p):
        'function_interface : LPAREN parameter_list RPAREN'
        p[0] = ast.FunctionInterface(parameter_list=p[2])

    def p_function_declaration(p):
        'declaration : IDENTIFIER COLONASSIGN FUNC function_interface block'
        p[0] = ast.FunctionDeclaration(
            name=p[1], interface=p[4], body=p[5])

    def p_type_declaration(p):
        'declaration : IDENTIFIER COLONASSIGN TYPE type'
        p[0] = ast.TypeDeclaration(name=p[1], datatype=p[4])

    def p_const_declaration(p):
        'declaration : CONST IDENTIFIER COLON type COLONASSIGN expression'
        p[0] = ast.ConstDeclaration(
            name=p[2], datatype=p[4], expression=p[6])

    # TODO: ?
    def p_type_identifier(p):
        'type : IDENTIFIER'
        p[0] = ast.Identifier(name=p[1])

    def p_type_struct(p):
        'type : STRUCT LCURLY field_list RCURLY'
        p[0] = ast.TypeStruct(value=p[3])

    def p_field_list_1(p):
        'field_list : field'
        p[0] = [p[1]]

    def p_field_list_2(p):
        'field_list : field_list field'
        p[1].append(p[2])
        p[0] = p[1]

    def p_field(p):
        'field : IDENTIFIER COLON type'
        p[0] = ast.Field(name=p[1], datatype=p[3])

    def p_parameter_list_1(p):
        'parameter_list :'
        p[0] = []

    def p_parameter_list_2(p):
        'parameter_list : parameter_list parameter'
        p[1].append(p[2])
        p[0] = p[1]

    def p_parameter(p):
        'parameter : IDENTIFIER COLON type'
        p[0] = ast.Parameter(name=p[1], datatype=p[3])

    def p_statement_sequence_empty(p):
        'statement_sequence :'
        p[0] = []

    def p_statement_sequence(p):
        'statement_sequence : statement_sequence statement'
        p[1].append(p[2])
        p[0] = p[1]

    def p_statement_block(p):
        'statement : block'
        p[0] = p[1]

    def p_statement_function_call(p):
        'statement : function_call'
        p[0] = p[1]

    def p_statement_variable_declaration_with_init(p):
        'statement : IDENTIFIER COLONASSIGN expression'
        p[0] = ast.VariableDeclaration(name=p[1], expression=p[3])

    def p_statement_assignment(p):
        'statement : IDENTIFIER ASSIGN expression'
        p[0] = ast.Assign(name=p[1], expression=p[3])

    def p_statement_if(p):
        'statement : IF expression block'
        p[0] = ast.If(condition=p[2], branch_if=p[3])

    def p_statement_for(p):
        'statement : FOR expression block'
        p[0] = ast.For(condition=p[2], branch=p[3])

    def p_statement_if_else(p):
        'statement : IF expression block ELSE block'
        p[0] = ast.If(condition=p[2], branch_if=p[3], branch_else=p[5])

    def p_expression_list_1(p):
        'expression_list :'
        p[0] = []

    def p_expression_list_2(p):
        'expression_list : expression_list expression'
        p[1].append(p[2])
        p[0] = p[1]

    def p_function_call(p):
        'function_call : expression LPAREN expression_list RPAREN'
        p[0] = ast.FunctionCall(expression=p[1], argument_list=p[3])

    def p_expression_string(p):
        'expression : STRING'
        value = p[1]
        assert value[0] == '\"' and value[-1] == '\"'
        value = value[1:-1]  # remove quotation marks
        p[0] = ast.String(value=value)

    def p_expression_identifier(p):
        'expression : IDENTIFIER'
        p[0] = ast.Identifier(name=p[1])

    def p_expression_number(p):
        'expression : NUMBER'
        p[0] = ast.Number(value=p[1])

    def p_expression_function_call(p):
        'expression : function_call'
        p[0] = p[1]

    def p_error(p):
        toklen = len(str(p.value))
        column = find_column(p.lexer.lexdata, p.lexpos)
        errmsg = (
            'filename:%(lineno)d:%(column)d: '
            'Parser error: unexpected token '
        )
        print(errmsg % {
            'lineno': p.lineno - 1,
            'column': column - 1,
        })
        print(vars(p))
        print('  ' + p.lexer.lexdata.split('\n')[p.lineno - 1])
        print('  ' + (' ' * column) + ('^' * toklen))

    # TODO: python3 reports some warning about unclosed file here
    parser = ply.yacc.yacc()
    return parser

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
