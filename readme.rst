
MISERY
======

Misery is a statically typed, imperative programming language.

Misery compiler generates native code via compilation to ANSI C.

Misery compiler is implemented in Python.


Test source with pep8 and run all unit tests::

    make

Test coverage::

    clear old data: python -m coverage erase
    generate info: python -m coverage run -m unittest discover
    simple report: python -m coverage report -m
    html report: python -m coverage html -d coverage_html


See LICENSE file for copyright and license details.

