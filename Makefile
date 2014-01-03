all: README.rst

README.rst: README.md
	@pandoc -f markdown -t rst -o README.rst README.md

test:
	@nosetests tests/*-test.py

test3:
	@nosetests3 tests/*-test.py
