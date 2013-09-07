all: pep8 lint
	python -m unittest discover

lint:
	pylint misery

pep8:
	pep8 --exclude parsetab.py misery
