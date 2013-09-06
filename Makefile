all:
	pep8 --exclude parsetab.py misery
	python3 -m unittest discover
