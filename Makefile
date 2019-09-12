clean:
	rm -f dist/*
test:
	tox
build: clean
	@python setup.py sdist bdist_wheel
release: build
	@twine upload dist/*

.PHONY: release
