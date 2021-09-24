.PHONY: clean clean-build clean-pyc lint test setup help

SHELL := /bin/zsh
.DEFAULT_GOAL := help

APP_DIR = src
RES_DIR = resources
APP_VERSION := 0.1
APP_NAME := dow2-texture-painter

test:
	. venv/bin/activate

venv:
	python3 -m venv venv && source venv/bin/activate
	venv/bin/pip install --upgrade pip wheel
	venv/bin/pip install --upgrade -r requirements.txt
	venv/bin/pip install -e .

run-dev: ## launch main frame
	python setup.py install
	python src/frame_main.py

# On windows, use ";" separator instead of ":" for the --add-data args
# --icon option isn't working alongisde --name option
build-bin-folder-win: ## build binary folder for windows
	pyinstaller --name $(APP_NAME)-$(APP_VERSION) --windowed --noconfirm  \
	--add-data "$(APP_DIR)/data;data" \
	--add-data "$(APP_DIR)/assets;assets" \ 
	--add-data "readme.md;." --hidden-import='PIL._tkinter_finder' \
	$(APP_DIR)/frame_main.py/

build-bin-folder: ## build binary folder
	pyinstaller --name $(APP_NAME)-$(APP_VERSION) --windowed --noconfirm \
	--add-data "$(APP_DIR)/data:data" \
	--add-data "$(APP_DIR)/assets:assets" \
	--hidden-import='PIL._tkinter_finder' $(APP_DIR)/frame_main.py/

build-bin-file: ## build binary
	pyinstaller --name $(APP_NAME)-$(APP_VERSION) --onefile --windowed \
	--noconfirm --add-data "$(APP_DIR)/$(RES_DIR):$(RES_DIR)" \
	--add-data "$(APP_DIR)/$(RES_DIR):$(RES_DIR)" \
	--hidden-import='PIL._tkinter_finder' $(APP_DIR)/frame_main.py

# build-spec:
# 	docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux "pyinstaller --onefile --windowed --noconfirm --add-data '$(APP_DIR)/data:data' --hidden-import='PIL._tkinter_finder' src/frame_main.py"

clean: clean-build clean-pyc ## remove all build, test, coverage and Python artifacts

clean-venv:
	rm -rf venv

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint: ## check style with flake8
	flake8 $(APP_DIR)

black: ## Apply Black autoformatting style
	black $(APP_DIR) --line-length 79
