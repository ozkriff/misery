all:
	pep8 --exclude parsetab.py misery
	python -m unittest discover
