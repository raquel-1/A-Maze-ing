VENV        = .venv
PYTHON      = $(VENV)/bin/python
UV          = uv
CONFIG      = config.txt

.PHONY: install run debug clean lint lint-strict build

install:
	uv venv $(VENV)
	uv pip install --python $(PYTHON) -e ".[dev]"

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	rm -rf __pycache__ mazegen/__pycache__ .mypy_cache .pytest_cache dist build
	find . -name "*.pyc" -delete

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

build:
	uv build