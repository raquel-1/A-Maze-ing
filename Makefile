VENV        = .venv
# path to the Python executable inside the venv
PYTHON      = $(VENV)/bin/python
# fast package manager for Python
CONFIG      = config.txt
OUTPUT      = output_maze.txt

# these names are commands, not files
.PHONY: install run debug clean lint lint-strict build validate

# set up the environment and install dependencies
install:
	uv venv $(VENV)
	uv pip install --python $(PYTHON) mlx-2.2-py3-none-any.whl
	uv pip install --python $(PYTHON) -e ".[dev]"

# .venv/bin/python a_maze_ing.py config.txt
run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

validate:
	@echo "Running the output validator"
	$(PYTHON) output_validator.py $(OUTPUT)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

# Clear temporary files (añadido que borre el TXT de salida al limpiar)
clean:
	rm -rf __pycache__ mazegen/__pycache__ .mypy_cache .pytest_cache dist build
	find . -name "*.pyc" -delete
	rm -f $(OUTPUT)

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-stmarict:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

# Build package
build:
	uv build