# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import copy
import textwrap
from misery import (
    ast,
    datatype,
)


def func_signature_to_mangled_name(func_name, func_signature):
    out = ''
    out += func_name
    for param in func_signature.param_list:
        out += '_'
        out += param.datatype.name
    return out


def _is_constructor(func_name):
    first_letter = func_name[0]
    return first_letter.istitle()


class Generator(object):

    prefix = '''
        #include <stdio.h>

        typedef int Int;
        typedef char* String;

        void Int_Int_init(Int* __result, Int* n) {
          *__result = *n;
        }

        void print_Int(Int* n) {
          printf("%d", *n);
        }

        void print_String(String* s) {
          printf("%s", *s);
        }

        void printNewLine() {
          printf("\\n");
        }

        void isLess_Int_Int(Int* __result, Int* a, Int* b) {
          *__result = (*a < *b);
        }

        void isGreater_Int_Int(Int* __result, Int* a, Int* b) {
          *__result = (*a < *b);
        }

        void isEqual_Int_Int(Int* __result, Int* a, Int* b) {
          *__result = (*a == *b);
        }

        void minus_Int_Int(Int* __result, Int* a, Int* b) {
          *__result = (*a - *b);
        }

        void plus_Int_Int(Int* __result, Int* a, Int* b) {
          *__result = (*a + *b);
        }

        void multiply_Int_Int(Int* __result, Int* a, Int* b) {
          *__result = (*a * *b);
        }

        void allocInt(Int** __result) {
          *__result = (Int*)calloc(1, sizeof(Int));
        }
    '''

    postfix = '''
        Int main(void) {
          start();
          return 0;
        }

    '''

    def __init__(self, ast_):
        self._ast = ast_
        self._indent_level = 0
        self._func_decl = None

    def _indent(self):
        return self._indent_level * '  '

    def _increnent_indent(self):
        self._indent_level += 1

    def _decrenent_indent(self):
        self._indent_level -= 1

    def _generate_func_header(self, name, signature):

        def generate_func_params(param_list):
            out = ''
            is_first = True
            for param in param_list:
                if is_first:
                    is_first = False
                else:
                    out += ', '
                out += param.datatype.name + '*' + ' ' + param.name
            return out

        out = ''
        out += 'void '
        out += func_signature_to_mangled_name(
            func_name=name,
            func_signature=signature,
        )
        out += '('
        if signature.return_type:
            out += signature.return_type.name + '*' + ' ' + '__result'
        if len(signature.param_list) != 0:
            if signature.return_type:
                out += ', '
            out += generate_func_params(signature.param_list)
        elif not signature.return_type:
            out += 'void'
        out += ')'
        return out

    def _generate_expr_dependencies(self, func_call_expr):
        out = ''
        for arg in func_call_expr.arg_list:
            if isinstance(arg, ast.FuncCall):
                out += self._generate_expr(arg)
        return out

    def _is_correct_ident(self, name):
        ''' Check if this is correct ident '''
        fd = self._func_decl  # shortcut
        if datatype.find_var_datatype(fd, name):
            return True
        return False

    def _generate_arg(self, arg):
        out = ''
        if isinstance(arg, (ast.Number, ast.String)):
            out += '&' + arg.binded_var_name
        elif isinstance(arg, ast.Ident):
            assert self._is_correct_ident(arg.name)
            out += arg.name
        elif isinstance(arg, ast.FuncCall):
            out += '&' + arg.binded_var_name
        else:
            raise Exception('Wrong arg type: ' + str(type(arg)))
        return out

    def _generate_func_call_expr_args(
        self,
        func_call_expr,
    ):
        out = ''
        is_first = True
        assert isinstance(
            func_call_expr.called_expr,
            ast.Ident,
        )
        called_func_name = func_call_expr.called_expr.name
        return_type = datatype.find_func_signature(
            self._ast.ident_list,
            self._func_decl,
            func_call_expr
        ).return_type
        if return_type:
            prefix_list = return_type.prefix_list
            if prefix_list and 'R' in prefix_list:
                out += '&' + func_call_expr.binded_var_name
            else:
                out += '&' + func_call_expr.binded_var_name
            is_first = False
        for arg in func_call_expr.arg_list:
            if is_first:
                is_first = False
            else:
                out += ', '
            out += self._generate_arg(arg)
        return out

    def _generate_func_call_expr(self, func_call_expr):
        out = ''
        # TODO: implement other exprs
        assert isinstance(
            func_call_expr.called_expr,
            ast.Ident,
        )
        func_signature = datatype.find_func_signature(
            self._ast.ident_list,
            self._func_decl,
            func_call_expr
        )
        called_func_name = func_signature_to_mangled_name(
            func_name=func_call_expr.called_expr.name,
            func_signature=func_signature,
        )
        out += self._generate_expr_dependencies(
            func_call_expr=func_call_expr,
        )
        out += self._indent()
        if _is_constructor(called_func_name):
            out += called_func_name + '_init'
        else:
            out += called_func_name
        out += '('
        out += self._generate_func_call_expr_args(
            func_call_expr,
        )
        out += ');\n'
        return out

    def _generate_expr(self, expr):
        ''' Generate evaluation code. '''
        out = ''
        if isinstance(expr, ast.FuncCall):
            out += self._generate_func_call_expr(expr)
        elif isinstance(expr, ast.Ident):
            pass  # ok
        else:
            raise Exception('Bad expr type: ' + str(type(expr)))
        return out

    def _generate_assign_stmt(self, assign_stmt):
        out = ''
        rvalue_expr = assign_stmt.rvalue_expr
        if isinstance(rvalue_expr, (ast.Number, ast.String)):
            out += self._indent()
            out += '*' + assign_stmt.name
            out += ' = '
            out += rvalue_expr.binded_var_name
            out += ';\n'
        elif isinstance(rvalue_expr, ast.FuncCall):
            out += self._generate_expr(rvalue_expr)
            out += self._indent()
            out += '*' + assign_stmt.name
            out += ' = '
            out += rvalue_expr.binded_var_name
            out += ';\n'
        else:
            raise Exception(
                'Bad expr type: ' + str(type(rvalue_expr)),
            )
        return out

    def _generate_func_call_stmt(self, stmt):
        out = ''
        out += self._generate_expr(stmt)
        return out

    def _generate_if_stmt(self, stmt):
        out = ''
        assert isinstance(stmt.condition, ast.FuncCall)
        out += self._generate_expr(stmt.condition)
        out += self._indent() + 'if ('
        var_name = stmt.condition.binded_var_name
        out += var_name
        out += ') {\n'
        self._increnent_indent()
        out += self._generate_block(block=stmt.branch_if)
        self._decrenent_indent()
        out += self._indent() + '}'
        if stmt.branch_else:
            out += ' else {\n'
            self._increnent_indent()
            out += self._generate_block(block=stmt.branch_else)
            self._decrenent_indent()
            out += self._indent() + '}'
        out += '\n'
        return out

    def _generate_for_stmt(self, stmt):
        out = ''
        assert isinstance(stmt.condition, ast.FuncCall)
        out += self._indent() + 'while (1) {\n'
        self._increnent_indent()
        out += self._generate_expr(stmt.condition)
        var_name = stmt.condition.binded_var_name
        out += self._indent() + 'if (' + '!' + var_name + ') {\n'
        self._increnent_indent()
        out += self._indent() + 'break;\n'
        self._decrenent_indent()
        out += self._indent() + '}'
        out += '\n'
        out += self._generate_block(block=stmt.branch)
        self._decrenent_indent()
        out += self._indent() + '}'
        out += '\n'
        return out

    def _generate_return_stmt(self, stmt):
        def gen_expr(expr):
            out = ''
            if isinstance(expr, (ast.Number, ast.String)):
                out += expr.binded_var_name
            elif isinstance(expr, ast.Ident):
                out = '*' + expr.name
            elif isinstance(expr, ast.FuncCall):
                out += expr.binded_var_name
            else:
                raise Exception(
                    'Wrong expr type: ' + str(type(expr)),
                )
            return out

        out = ''
        if isinstance(stmt.expr, ast.FuncCall):
            out += self._generate_expr(stmt.expr)
        out += self._indent() + '*__result = '
        out += gen_expr(expr=stmt.expr)
        out += ';\n'
        out += self._indent() + 'return;\n'
        return out

    def _generate_stmt(self, stmt):
        out = ''
        if isinstance(stmt, ast.FuncCall):
            out += self._generate_func_call_stmt(stmt)
        elif isinstance(stmt, ast.VarDecl):
            if stmt.allocate_memory_on_stack:
                out += self._indent()
                out += stmt.name
                out += ' = '
                out += '&' + stmt.binded_var_name
                out += ';\n'
                out += self._generate_assign_stmt(stmt)
            else:
                out += self._generate_expr(stmt.rvalue_expr)
                out += self._indent()
                out += stmt.name
                out += ' = '
                if isinstance(stmt.rvalue_expr, ast.Ident):
                    out += stmt.rvalue_expr.name
                else:
                    prefix_list = stmt.datatype.prefix_list
                    if prefix_list and 'R' in prefix_list:
                        out += stmt.rvalue_expr.binded_var_name
                    else:
                        out += '&' + stmt.rvalue_expr.binded_var_name
                out += ';\n'
        elif isinstance(stmt, ast.Assign):
            out += self._generate_assign_stmt(stmt)
        elif isinstance(stmt, ast.If):
            out += self._generate_if_stmt(stmt)
        elif isinstance(stmt, ast.For):
            out += self._generate_for_stmt(stmt)
        elif isinstance(stmt, ast.Return):
            out += self._generate_return_stmt(stmt)
        else:
            raise Exception('Bad stmt type: ' + str(type(stmt)))
        return out

    def _generate_block(self, block):
        out = ''
        for stmt in block:
            out += self._generate_stmt(stmt)
        return out

    def _generate_local_vars(self):
        fd = self._func_decl  # shortcut
        out = ''
        for name, datatype_ in sorted(fd.vars.items()):
            out += self._indent()
            out += datatype_.name
            out += '*'
            out += ' '
            out += name
            out += ';' + '\n'
        for name, datatype_ in sorted(fd.tmp_vars.items()):
            out += self._indent()
            out += datatype_.name
            prefix_list = datatype_.prefix_list
            if prefix_list and 'R' in prefix_list:
                out += '*'
            out += ' '
            out += name
            out += ';' + '\n'
        for name, expr in sorted(fd.constants.items()):
            out += self._indent()
            out += datatype.get_expr_datatype(
                self._ast.ident_list,
                fd,
                expr,
            ).name
            out += ' '
            out += name
            out += ';' + '\n'
        return out

    def _generate_constants_initialization_code(self):
        fd = self._func_decl  # shortcut
        out = ''
        for name, expr in sorted(fd.constants.items()):
            out += self._indent()
            out += name
            out += ' = '
            if isinstance(expr, ast.String):
                out += '\"' + str(expr.value) + '\"'
            elif isinstance(expr, ast.Number):
                out += str(expr.value)
            else:
                raise Exception('Bad type: ' + str(type(expr)))
            out += ';' + '\n'
        return out

    def _generate_func(self, func_decl):
        fd = func_decl  # shortcut
        self._func_decl = fd
        out = ''
        out += self._generate_func_header(
            name=func_decl.name,
            signature=func_decl.signature,
        )
        out += ' {\n'
        self._increnent_indent()
        if fd.vars or fd.tmp_vars or fd.constants:
            out += self._generate_local_vars()
            out += '\n'
            if func_decl.constants:
                out += self._generate_constants_initialization_code()
                out += '\n'
        out += self._generate_block(func_decl.body)
        self._decrenent_indent()
        out += '}\n'
        return out

    def _generate_struct(self, struct_decl):
        name = struct_decl.name  # shortcut
        out = ''
        out += 'struct ' + name + ' {\n'
        self._increnent_indent()
        for field in struct_decl.field_list:
            out += self._indent()
            out += field.datatype.name + ' ' + field.name + ';\n'
        self._decrenent_indent()
        out += '};\n'
        out += '\n'
        out += 'void ' + name + '_init(' + name + '* __result' + ') {\n'
        out += '  /* todo */\n'
        out += '}\n'
        return out

    def _generate_forward_decls(self):
        out = ''
        for decl in self._ast.decl_list:
            if isinstance(decl, ast.FuncDecl):
                out += self._generate_func_header(
                    name=decl.name,
                    signature=decl.signature,
                )
                out += ';\n'
            elif isinstance(decl, ast.StructDecl):
                out += 'typedef struct '
                out += decl.name
                out += ' '
                out += decl.name
                out += ';\n'
            else:
                raise Exception('Bad type: ' + str(type(decl)))
        return out

    def _generate_imports(self):
        if not self._ast.import_list:
            return ''
        out = ''
        out += '\n'
        for import_node in self._ast.import_list:
            out += '// import: ' + import_node + '\n'
        return out

    def _generate_decl(self, decl):
        out = ''
        if isinstance(decl, ast.FuncDecl):
            out += self._generate_func(decl)
        elif isinstance(decl, ast.StructDecl):
            out += self._generate_struct(decl)
        else:
            raise Exception('Bad decl type: ' + str(type(decl)))
        return out

    def _generate_decls(self):
        out = ''
        for decl in self._ast.decl_list:
            out += self._generate_decl(decl)
            out += '\n'
        return out

    def generate(self):
        out = ''
        out += self._generate_imports()
        out += '\n'
        out += self._generate_forward_decls()
        out += '\n'
        out += self._generate_decls()
        return out

    def generate_full(self):
        out = ''
        out += textwrap.dedent(Generator.prefix)
        out += self.generate()
        out += textwrap.dedent(Generator.postfix)
        return out


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
