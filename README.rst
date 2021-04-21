=========
Dawn of War 2 texture painter
=========

This is a GUI desktop application which allow the user to recolor Dawn of War 2
gray scale diffuse texture using the default army color pattern from the game.

Dawn of War 2 engine uses shader & pre-defined color pattern to colorize
their texture. Those textures are gray scaled by default.

The goal is to reproduce the engine coloring in order to export those textures
with their color pattern.

User can also make his custom army pattern and save it.
Batch edit is supported, you can set a pattern apply it to every texture in a
folder.

Only tested with python 3.7 on linux environment

Contributing
============
From the root directory:

Run `make venv` to generate the virtual env

`texture-painter` is the defined entry point to start the GUI app

Run following command to generate an EXE file with pyinstaller:

`make build-bin-folder` for an executable and its the required library files
in the same folder
`make build-bin-file` for an one file executable
