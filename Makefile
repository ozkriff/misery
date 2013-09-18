all: prepare_parsetab pep8 test

test:
	python -B -m unittest discover

prepare_parsetab:
	python -c 'from misery.parse import make_parser; p = make_parser()'

lint:
	pylint misery

pep8:
	pep8 --exclude parsetab.py misery

clean:
	rm -f parser.out parsetab.py *.pyc misery/*.pyc
