.PHONY: clean clean-build clean-pyc lint test setup help

SHELL := /bin/zsh
.DEFAULT_GOAL := help

APP_DIR = dow2_texture_painter

test:
	. venv/bin/activate

venv:
	python3 -m venv venv && source venv/bin/activate
	venv/bin/pip install --upgrade pip wheel
	venv/bin/pip install --upgrade -r requirements.txt
	venv/bin/pip install -e .

run-dev: ## launch main frame entry point
	texture-painter

build-bin-folder: ## build binary folder for linux
	pyinstaller --noconfirm --add-data "$(APP_DIR)/data:data" --hidden-import='PIL._tkinter_finder' dow2_texture_painter/frame_main.py

build-bin-file: ## build binary file for linux
	pyinstaller --onefile --windowed --noconfirm --add-data "$(APP_DIR)/data:data" --hidden-import='PIL._tkinter_finder' dow2_texture_painter/frame_main.py

clean: clean-build clean-pyc ## remove all build, test, coverage and Python artifacts

clean-venv:
	rm -rf venv

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint: ## check style with flake8
	flake8 $(APP_DIR)

black: ## Apply Black autoformatting style
	black $(APP_DIR) --line-length 79
