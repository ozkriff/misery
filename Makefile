all:
	pep8 --exclude parsetab.py *.py
	python3 -m unittest discover
