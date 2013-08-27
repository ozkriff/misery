
MISERY
======

Misery is a statically typed, imperative programming language.

Misery compiler generates native code via compilation to ANSI C.

Misery compiler is implemented in Python.


Run all unit tests::

    python -m unittest discover -v

Test coverage::

    clear old data: python -m coverage erase
    generate info: python -m coverage run -m unittest discover
    simple report: python -m coverage report -m
    html report: python -m coverage html -d coverage_html


TODO
----

- qualifiedIdentifier: module.submodule.Class.Subclass
- generics
- varargs
- var testArray Array[Int](1, 2, 3)
- qualifiedIdentifier: x.a.c
- switch expr { case dfgd {} }
- var myClosure = func() { killAllHumans() }
- nested funcs
- pep8, pylint, pyflakes
- implement pointer as special kind of templates
- do not implement NULL pointer!

See LICENSE file for copyright and license details.

