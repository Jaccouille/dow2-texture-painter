from PIL import (
    Image,
)
import tkinter as tk
from pathlib import Path


def get_tem_filenames(path: Path, src_format: list):
    file_suffix = set(["Primary", "Secondary", "Trim", "Weapon"])

    def check_if_tem_exist(files_dict: dict):
        """Check if the 4 files neccessary to construct packed tem files exists

        :param files_dict: a dict containing unit name prefix as a key
            to access a nested dict containing the file path as a value
            an its suffix as key,
            e.g {'space_marine_unit':
                    {
                    'Primary': Path('space_marine_unit_Primary.tga)',
                    'Secondary': Path('space_marine_unit_Secondary.tga)',
                    'Trim': Path('space_marine_unit_Trim.tga)',
                    'Weapon': Path('space_marine_unit_Weapon.tg)a'
                    }
                }
        :raises FileNotFoundError: Missing tem textures
        """
        for v in files_dict.values():
            diff = list(set(v.keys()) - file_suffix)
            if len(diff) > 0:
                filetype_missing = ", ".join(diff)
                raise FileNotFoundError(
                    f"Missing {filetype_missing} tem textures files"
                )

    def find_tem_files(file_paths: list) -> dict:
        files_dict = {}
        """
            Dawn of War 1 team colour texture used for the army painter are named
            with the following pattern :
            {unit_name}_Primary -> First color/Red mask
            {unit_name}_Secondary -> Second color/Blue mask
            {unit_name}_Trim -> Green color/Green mask
            {unit_name}_Weapon -> Fourth color/Alpha mask]

        :return: a dict containing unit name prefix as a key to access a nested
            dict containing the file path as a value an its suffix as key
            e.g {'space_marine_unit':
                    {
                    'Primary': Path('space_marine_unit_Primary.tga'),
                    'Secondary': Path('space_marine_unit_Secondary.tga'),
                    'Trim': Path('space_marine_unit_Trim.tga'),
                    'Weapon': Path('space_marine_unit_Weapon.tga)'
                    }
                }
        :rtype: nested dict
        """
        for file in file_paths:
            # Get the filename suffix, expecting: (Primary | Secondary | Trim | Weapon)
            f_suffix = file.stem.rsplit("_", 1)[-1]
            if f_suffix in file_suffix:
                # Get the filename prefix, expecting a unit name
                f_prefix = file.stem.rsplit("_", 1)[0]

                # Register unit name as a key to a dictionary containing the filename
                # as a value and their suffix as key
                if not f_prefix in files_dict:
                    files_dict[f_prefix] = {}
                files_dict[f_prefix][f_suffix] = file
        check_if_tem_exist(files_dict)
        return files_dict

    file_paths = []
    for format in src_format:
        file_paths.extend(Path(path).glob(f"*.{format}"))
    return find_tem_files(file_paths)


def convert_tem_texture(tem_textures: dict, path: Path):
    # TODO: Find a way to handle icon banner pasted on textures
    # TODO: Check the size of Dawn of War 1 unit textures
    # can the different textures for the same unit differ in size?

    black_pixel_threshold = 25
    bands = []

    if len(tem_textures) != 4:
        print(f"Found only {len(tem_textures)} textures :")

    for k, v in tem_textures.items():
        img = Image.open(path / v)

        # tem textures are grayscaled images, therefore we can convert them
        # to 8 bit pixel format, each image will be used as a band/chan
        # upon Image.merge() function call
        img.convert("L")
        white_chan = img.getchannel(0)

        # Each gray pixel has to be set to 255, this is how dawn of war 2
        # tem textures were made, if not, the blending within texture painter
        # will be darken
        colored_mask = Image.eval(
            white_chan, lambda x: 255 if x >= black_pixel_threshold else 0
        )
        bands.append(colored_mask)

        # Debug
        # colored_mask.save(path / ("test_" + k + ".tga"), "tga")

    mode = "RGBA" if len(bands) == 4 else "RGB"
    return Image.merge(mode=mode, bands=bands)


def exec_convert(path: Path, src_format: list, dest_format: str):
    files_dict = get_tem_filenames(path, src_format)
    for k in files_dict.keys():
        result = convert_tem_texture(files_dict.get(k), path)
        filename = k.replace("default", "tem", 1)
        result.save(path / (f"{filename}.{dest_format}"), dest_format)


def local_test():
    # Put test sample texture in /assets/dow1 directory
    path = Path.cwd() / "assets/dow1"
    exec_convert(path, ["tga"], "tga")


if __name__ == "__main__":
    local_test()
