# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


from ply import (
    yacc,
    lex,
)
from misery import (
    ast,
    misc,
    datatype,
)


reserved = {
    'func': 'FUNC',
    'if': 'IF',
    'else': 'ELSE',
    'import': 'IMPORT',
    'const': 'CONST',
    'struct': 'STRUCT',
    'for': 'FOR',
    'return': 'RETURN',
}


tokens = [
    'IDENT',
    'STRING',
    'NUMBER',
    'ASSIGN',
    'COLONASSIGN',
    'DOUBLECOLONASSIGN',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    'LT',
    'GT',
    'COMMA',
    # 'COLON',
    'ARROW',
    # 'DOT',
] + list(reserved.values())


def find_column(input_string, lexpos):
    '''Compute column.

    input_string is the input text string
    lexpos is a lexem position
    '''
    last_cr = input_string.rfind('\n', 0, lexpos)
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
    t_DOUBLECOLONASSIGN = r'::='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_LT = r'<'
    t_GT = r'>'
    t_COMMA = r','
    # t_COLON = r':'
    # t_DOT = r'\.'
    t_STRING = r'"[^"]*"'

    def t_IDENTIFIER(t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = reserved.get(t.value, 'IDENT')
        return t

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
        message = (
            '\n' +
            (
                'filename:[%(lineno)d:%(column)d: '
                'Lexer error: Illegal character...'
            ) % {
                'lineno': t.lineno - 1,
                'column': column - 1,
            } +
            '\n' +
            '  ' + t.lexer.lexdata.split('\n')[t.lineno - 1] + '\n' +
            '  ' + (' ' * (column)) + '^' + '\n'
        )
        raise Exception(message)

    # Build the lexer from my environment and return it
    return lex.lex()


def make_parser():

    def p_module(p):
        'module : import_section decl_list'
        p[0] = ast.Module(import_list=p[1], decl_list=p[2])

    def p_import_section_empty(p):
        'import_section :'
        p[0] = None

    def p_import_section(p):
        'import_section : IMPORT LCURLY import_list RCURLY'
        p[0] = p[3]

    def p_import_list_empty(p):
        'import_list :'
        p[0] = []

    def p_import_list(p):
        'import_list : import_list IDENT'
        p[1].append(p[2])
        p[0] = p[1]

    def p_decl_list_empty(p):
        'decl_list :'
        p[0] = []

    def p_decl_list(p):
        'decl_list : decl_list decl'
        p[1].append(p[2])
        p[0] = p[1]

    def p_block(p):
        'block : LCURLY stmt_list RCURLY'
        p[0] = p[2]

    def p_block_2(p):
        'block : LCURLY stmt_list RETURN RCURLY'
        p[2].append(ast.Return(expr=None))
        p[0] = p[2]

    def p_block_3(p):
        'block : LCURLY stmt_list RETURN expr RCURLY'
        p[2].append(ast.Return(expr=p[4]))
        p[0] = p[2]

    def p_generic_empty(p):
        'generic :'
        p[0] = None

    def p_generic(p):
        'generic : LT IDENT GT'
        p[0] = [p[2]]

    def p_func_signature(p):
        'func_signature : generic LPAREN param_list RPAREN ARROW type'
        p[0] = ast.FuncSignature(
            param_list=p[3],
            return_type=p[6],
            generic_param_list=p[1],
        )

    def p_func_signature_without_return_type(p):
        'func_signature : generic LPAREN param_list RPAREN'
        p[0] = ast.FuncSignature(
            param_list=p[3],
            generic_param_list=p[1],
        )

    def p_func_decl(p):
        'decl : FUNC IDENT func_signature block'
        p[0] = ast.FuncDecl(
            name=p[2],
            signature=p[3],
            body=p[4],
        )

    def p_struct_decl(p):
        'decl : STRUCT IDENT LCURLY field_list RCURLY'
        p[0] = ast.StructDecl(name=p[2], field_list=p[4])

    def p_const_decl(p):
        'decl : CONST IDENT type COLONASSIGN expr'
        p[0] = ast.ConstDecl(
            name=p[2], datatype=p[3], expr=p[5])

    def p_type_ident(p):
        'type : IDENT'
        p[0] = datatype.SimpleDataType(name=p[1])

    def p_field_list_1(p):
        'field_list : field'
        p[0] = [p[1]]

    def p_field_list_2(p):
        'field_list : field_list field'
        p[1].append(p[2])
        p[0] = p[1]

    def p_field(p):
        'field : IDENT type'
        p[0] = ast.Field(name=p[1], datatype=p[2])

    def p_param_list_1(p):
        'param_list :'
        p[0] = []

    def p_param_list_2(p):
        'param_list : param'
        p[0] = [p[1]]

    def p_param_list_3(p):
        'param_list : param_list COMMA param'
        p[1].append(p[3])
        p[0] = p[1]

    def p_param(p):
        'param : IDENT type'
        p[0] = ast.Param(name=p[1], datatype=p[2])

    def p_stmt_list_empty(p):
        'stmt_list :'
        p[0] = []

    def p_stmt_list(p):
        'stmt_list : stmt_list stmt'
        p[1].append(p[2])
        p[0] = p[1]

    def p_stmt_block(p):
        'stmt : block'
        p[0] = p[1]

    def p_stmt_func_call(p):
        'stmt : func_call'
        p[0] = p[1]

    def p_stmt_var_decl_1(p):
        'stmt : IDENT COLONASSIGN expr'
        p[0] = ast.VarDecl(name=p[1], expr=p[3])

    def p_stmt_var_decl_2(p):
        'stmt : IDENT DOUBLECOLONASSIGN expr'
        p[0] = ast.VarDecl(
            name=p[1],
            expr=p[3],
            allocate_memory_on_stack=True,
        )

    def p_stmt_assignment(p):
        'stmt : IDENT ASSIGN expr'
        p[0] = ast.Assign(name=p[1], expr=p[3])

    def p_stmt_if(p):
        'stmt : IF expr block'
        p[0] = ast.If(condition=p[2], branch_if=p[3])

    def p_stmt_for(p):
        'stmt : FOR expr block'
        p[0] = ast.For(condition=p[2], branch=p[3])

    def p_stmt_if_else(p):
        'stmt : IF expr block ELSE block'
        p[0] = ast.If(condition=p[2], branch_if=p[3], branch_else=p[5])

    def p_expr_list_1(p):
        'expr_list :'
        p[0] = []

    def p_expr_list_2(p):
        'expr_list : expr_list expr'
        p[1].append(p[2])
        p[0] = p[1]

    def p_func_call(p):
        'func_call : expr LPAREN expr_list RPAREN'
        p[0] = ast.FuncCall(expr=p[1], arg_list=p[3])

    def p_expr_string(p):
        'expr : STRING'
        p[0] = ast.String(value=misc.remove_quotation_marks(p[1]))

    def p_expr_ident(p):
        'expr : IDENT'
        p[0] = ast.Ident(name=p[1])

    def p_expr_number(p):
        'expr : NUMBER'
        p[0] = ast.Number(value=p[1])

    def p_expr_func_call(p):
        'expr : func_call'
        p[0] = p[1]

    def p_error(p):
        toklen = len(str(p.value))
        column = find_column(p.lexer.lexdata, p.lexpos)
        message = (
            '\n' +
            (
                'filename:%(lineno)d:%(column)d: '
                'Parser error: unexpected token '
            ) % {
                'lineno': p.lineno - 1,
                'column': column - 1,
            } +
            '\n' +
            '  ' + p.lexer.lexdata.split('\n')[p.lineno - 1] + '\n' +
            '  ' + (' ' * column) + ('^' * toklen) + '\n'
        )
        raise Exception(message)

    parser = yacc.yacc()
    return parser

# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
