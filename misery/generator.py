# -*- coding: utf-8 -*-
# See LICENSE file for copyright and license details


import copy
import textwrap
from misery import (
    ast,
)


class Generator(object):

    prefix = '''
        #include <stdio.h>

        typedef int Int;
        typedef char* String;

        void Int_init(Int* __result, Int* n) {
          *__result = *n;
        }

        void printInt(Int* n) {
          printf("%d", *n);
        }

        void printString(String* s) {
          printf("%s", *s);
        }

        void printNewLine() {
          printf("\\n");
        }

        void isLessInt(Int* __result, Int* a, Int* b) {
          *__result = (*a < *b);
        }

        void isGreaterInt(Int* __result, Int* a, Int* b) {
          *__result = (*a < *b);
        }

        void isEqualInt(Int* __result, Int* a, Int* b) {
          *__result = (*a == *b);
        }

        void minusInt(Int* __result, Int* a, Int* b) {
          *__result = (*a - *b);
        }

        void plusInt(Int* __result, Int* a, Int* b) {
          *__result = (*a + *b);
        }

        void multiplyInt(Int* __result, Int* a, Int* b) {
          *__result = (*a * *b);
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

    def _generate_func_parameters(self, par_list):
        out = ''
        is_first = True
        for parameter in par_list:
            if is_first:
                is_first = False
            else:
                out += ', '
            out += parameter.datatype.name + '*' + ' ' + parameter.name
        return out

    def _generate_func_header(self, name, signature):
        out = ''
        out += 'void ' + name + '('
        if signature.return_type:
            out += signature.return_type.name + '*' + ' ' + '__result'
        if len(signature.par_list) != 0:
            if signature.return_type:
                out += ', '
            out += self._generate_func_parameters(signature.par_list)
        elif not signature.return_type:
            out += 'void'
        out += ')'
        return out

    def _generate_expr_dependencies(self, func_call_expr):
        out = ''
        for argument in func_call_expr.arg_list:
            if isinstance(argument, ast.FuncCall):
                out += self._generate_expr(argument)
        return out

    def _is_correct_ident(self, name):
        ''' Check if this is correct ident '''
        fd = self._func_decl  # shortcut
        for parameter in fd.signature.par_list:
            if parameter.name == name:
                return True
        for var_name in fd.vars.keys():
            if var_name == name:
                return True
        return False

    def _generate_argument(self, argument):
        out = ''
        if isinstance(argument, (ast.Number, ast.String)):
            out += '&' + argument.binded_var_name
        elif isinstance(argument, ast.Ident):
            assert self._is_correct_ident(argument.name)
            out += argument.name
        elif isinstance(argument, ast.FuncCall):
            out += '&' + argument.binded_var_name
        else:
            raise Exception('Wrong argument type: ' + str(type(argument)))
        return out

    def _generate_func_call_expr_arguments(
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
        ident_list = self._ast.ident_list
        if ident_list[called_func_name].return_type is not None:
            out += '&' + func_call_expr.binded_var_name
            is_first = False
        for argument in func_call_expr.arg_list:
            if is_first:
                is_first = False
            else:
                out += ', '
            out += self._generate_argument(argument)
        return out

    def _generate_func_call_expr(self, func_call_expr):
        out = ''
        # TODO: implement other exprs
        assert isinstance(
            func_call_expr.called_expr,
            ast.Ident,
        )
        called_func_name = func_call_expr.called_expr.name
        out += self._generate_expr_dependencies(
            func_call_expr=func_call_expr,
        )
        out += self._indent()
        # is constructor\initializer? TODO: remove from here, do earlier
        if called_func_name[0].istitle():
            out += called_func_name + '_init'
        else:
            out += called_func_name
        out += '('
        out += self._generate_func_call_expr_arguments(
            func_call_expr,
        )
        out += ');\n'
        return out

    def _generate_expr(self, expr):
        ''' Generate evaluation code. '''
        out = ''
        if isinstance(expr, ast.FuncCall):
            out += self._generate_func_call_expr(expr)
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
                out += self._indent()
                out += stmt.name
                out += ' = '
                out += '&' + stmt.rvalue_expr.binded_var_name
                out += ';\n'
                out += self._generate_expr(stmt.rvalue_expr)
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
            out += ' '
            out += name
            out += ';' + '\n'
        for name, expr in sorted(fd.constants.items()):
            out += self._indent()
            if isinstance(expr, ast.String):
                out += 'String'
            elif isinstance(expr, ast.Number):
                out += 'Int'
            else:
                raise Exception('bad type: ' + str(type(expr)))
            out += ' '
            out += name
            out += ';' + '\n'
        return out

    def _generate_constats_initialization_code(self):
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
                raise Exception('bad type: ...todo...')
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
                out += self._generate_constats_initialization_code()
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
        if self._ast.import_list is None:
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


def scan_vars(ast_):
    ''' Add information about local vars allocation on stack into AST '''

    def scan_expr_vars(func_decl, expr):
        fd = func_decl  # shortcut
        if isinstance(expr, ast.FuncCall):
            for argument in expr.arg_list:
                scan_expr_vars(fd, argument)
            assert isinstance(expr.called_expr, ast.Ident)
            called_func_name = expr.called_expr.name
            ident_list = ast_.ident_list
            return_type = ident_list[called_func_name].return_type
            if return_type is not None:
                var_name = 'tmp_' + str(len(fd.tmp_vars))
                fd.tmp_vars[var_name] = return_type
                expr.binded_var_name = var_name
        elif isinstance(expr, ast.Number):
            var_name = 'const_' + str(len(fd.constants))
            fd.constants[var_name] = copy.deepcopy(expr)
            expr.binded_var_name = var_name
        elif isinstance(expr, ast.String):
            var_name = 'const_' + str(len(fd.constants))
            fd.constants[var_name] = copy.deepcopy(expr)
            expr.binded_var_name = var_name
        elif isinstance(expr, ast.Ident):
            pass  # ok
        else:
            raise Exception('Bad expr type: ' + str(type(expr)))

    def scan_stmt_vars(ast_, func_decl, stmt):
        fd = func_decl  # shortcut
        if isinstance(stmt, ast.FuncCall):
            scan_expr_vars(fd, stmt)
        elif isinstance(stmt, ast.VarDecl):
            datatype_ = copy.deepcopy(stmt.datatype)
            fd.vars[stmt.name] = datatype_
            if stmt.allocate_memory_on_stack:
                var_name = 'tmp_' + str(len(fd.tmp_vars))
                fd.tmp_vars[var_name] = copy.deepcopy(stmt.datatype)
                stmt.binded_var_name = var_name
            scan_expr_vars(fd, stmt.rvalue_expr)
        elif isinstance(stmt, ast.Return):
            scan_expr_vars(fd, stmt.expr)
        elif isinstance(stmt, ast.Assign):
            scan_expr_vars(fd, stmt.rvalue_expr)
        elif isinstance(stmt, ast.If):
            scan_expr_vars(fd, stmt.condition)
            scan_block_vars(ast_, fd, stmt.branch_if)
            if stmt.branch_else:
                scan_block_vars(ast_, fd, stmt.branch_else)
        elif isinstance(stmt, ast.For):
            scan_expr_vars(fd, stmt.condition)
            scan_block_vars(ast_, fd, stmt.branch)
        else:
            raise Exception('Bad stmt type: ' + str(type(stmt)))

    def scan_block_vars(ast_, func_decl, block):
        for stmt in block:
            scan_stmt_vars(ast_, func_decl, stmt)

    for decl in ast_.decl_list:
        if isinstance(decl, ast.FuncDecl):
            scan_block_vars(
                ast_=ast_,
                func_decl=decl,
                block=decl.body,
            )


# vim: set tabstop=4 shiftwidth=4 softtabstop=4 expandtab:
