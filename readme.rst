Run all unit tests::

    python -m unittest discover -v

Test coverage::

    clear old data: python -m coverage erase
    generate info: python -m coverage run -m unittest discover
    simple report: python -m coverage report -m
    html report: python -m coverage html -d coverage_html


TODO:

- Rename: 'type' -> '???'
- return_type=ast.NodeIdentifier('Integer') ??? NodeType!
- Table.current_indent_level
- qualifiedIdentifier: module.submodule.Class.Subclass
- generics
- varargs
- var testArray Array[Int](1, 2, 3)
- qualifiedIdentifier: x.a.c
- switch expr { case dfgd {} }
- var myClosure = func() { killAllHumans() }
- nested funcs
- pep8, pylint, pyflakes

- try to use verbose test names::

    def test_that_a_player_cannot_move_into_an_already_occupied_board_cell(self): pass
    def test_corectness_of_verify_win_combinations_3(self): pass
    def test_that_parsed_response_contains_status_key(self): pass

Notes:

Print lexems::

    lexer.input(input_string);
    for tok in lexer:
        my_pretty_print.my_pretty_print(tok)