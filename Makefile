all: README.rst

README.rst: README.md
	pandoc -f markdown -t rst -o README.rst README.md
