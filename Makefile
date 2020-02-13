clean:
	rm -rf dist/*

dev:
	pip install -e .

package:
	python setup.py sdist
	python setup.py bdist_wheel

test:
	py.test tests