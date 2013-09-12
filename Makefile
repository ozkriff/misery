all: pep8 test

test:
	python -B -m unittest discover

lint:
	pylint misery

pep8:
	pep8 --exclude parsetab.py misery
