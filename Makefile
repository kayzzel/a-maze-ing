#-------------------------------- VARIABLES ----------------------------------#

NAME		=	a_maze_ing.py
CONFIG_FILE	=	config.txt

#-------------------------------- INSTALLS -----------------------------------#

INSTALLS	=	pydantic \
				./lib/mlx-2.2-py3-none-any.whl

#-------------------------------- RULES --------------------------------------#

install: 
	python3 -m pip install $(INSTALLS)

run:
	python3 $(NAME) $(CONFIG_FILE)

debug:
	python3 -m pdb $(NAME) $(CONFIG_FILE)

clean:
	find . -name "__pycache__" -type d -exec rm -rf "{}" +
	find . -name ".mypy_cache" -type d -exec rm -rf "{}" +

lint:
	flake8 . --exclude .venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude .venv

lint-strict:
	flake8 . --exclude .venv
	python3 -m mypy . --strict --exclude .venv
