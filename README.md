# Dawn of War 2 texture painter

This is a GUI desktop application that allows the user to recolor Dawn of War 2 grayscale diffuse texture using the default army color pattern from the game.

Dawn of War 2 engine uses shader & pre-defined color pattern to colorize their texture. Those textures are grayscaled by default.

The goal is to reproduce the engine coloring to export those textures with their color pattern.

Users can also make their custom army pattern and save it. Batch editing is supported, you can set a pattern to apply it to every texture in a folder.


![](https://i.imgur.com/VXFjzkh.jpg)
_dow2 texture painter application loaded with the hormagaunt grayscale diffuse texture._

## How to use

This tool was made to precisely work with Dawn of War 2 textures to reduce
editing time.

Dawn of War 2 unit textures are composed of the following files:
* {unit_name}_dif.dds -> diffuse
* {unit_name}_tem.dds -> team color mask
* {unit_name}_drt.dds -> dirt
* {unit_name}_spec.dds -> specular
* {unit_name}_emi.dds -> emissive
* {unit_name}_ocl.dds -> oclusion
* {unit_name}_nrm.dds -> normal map

This tool assumes that the textures are located in the unit folder, e.g a folder
named "space marine" contains all textures for a space marine model.
Emissive, oclusion and normal map textures are not useful to color the diffuse texture.

Click on `File -> Open` and select a diffuse texture, it will load the
{unit_name}_tem.dds texture located in the same folder, the team color file
contains RGBA color masks which are necessary for mapping the colored part of the
diffuse texture. Can open following format: DDS, PNG, JPG, BMP, TGA and BLP.

Click on the top left boxes to pick a color that correspond to the following mask of the
team color texture:
* Color 1 -> red mask
* Color 2 -> green mask
* Color 3 -> blue mask
* Color 4 -> alpha mask

Once you're done, you can save your edit by clicking on `File -> Save`, can save
with the following format: PNG, JPG, BMP and TGA.

The application loads the default color pattern from Dawn of War 2, you can
select them on the list located bottom right.

You can save your current color pattern by clicking on `Save pattern`.

You can apply dirt & specular texture by clicking on `Edit -> Apply dirt/specular`,
those textures must be in the same folder as the diffuse ones.

You can replace color by transparency with selecting the color mask in the list
and checking the  `Apply alpha` box.

You can color multiple diffuse textures by using the batch edit tool, select the source
directory where your textures are located, input format, output format and the
destination directory, the name of the colored files will be the same as the
original one, if input & output file have the same format, the output will overwrite
the original diffuse texture. Batch edit tool does not process subfolder.
Batch edit only works for diffuse texture ending with "_dif", such as {unit_name}_dif.dds,
because it's the name format for Dawn of War 2 diffuse texture.

## Developing
From the root directory:

Run `make venv` to generate the virtual env

`texture-painter` is the defined entry point to start the GUI app

Run the following command to generate an EXE/binary file with pyinstaller:

`make build-bin-folder` for an executable and its required library files
in the same folder
`make build-bin-file` for an one file executable
