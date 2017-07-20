.PHONY: init test clean

init:
	pip install -r requirements.txt

test:
	python -m tests.test

clean:
	rm -rf build
