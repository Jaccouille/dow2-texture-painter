from PIL import (
    Image,
)
import tkinter as tk
from pathlib import Path
import os


def get_tem_filenames(path: Path, src_format: str):
    file_suffix = set(["Primary", "Secondary", "Trim", "Weapon"])

    def check_if_tem_exist(files_dict: dict):
        """Check if the 4 files neccessary to construct packed tem files exists

        :param files_dict: a dict containing unit name prefix as a key
            to access a nested dict containing the file path as a value
            an its suffix as key,
            e.g {'space_marine_unit':
                    {
                    'Primary': 'space_marine_unit_Primary.tga',
                    'Secondary': 'space_marine_unit_Secondary.tga',
                    'Trim': 'space_marine_unit_Trim.tga',
                    'Weapon': 'space_marine_unit_Weapon.tga'
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

    def find_tem_files(filenames: list) -> dict:
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
                    'Primary': 'space_marine_unit_Primary.tga',
                    'Secondary': 'space_marine_unit_Secondary.tga',
                    'Trim': 'space_marine_unit_Trim.tga',
                    'Weapon': 'space_marine_unit_Weapon.tga'
                    }
                }
        :rtype: nested dict
        """
        for file in filenames:
            # removing the extension from the string
            f_no_ext = file.rsplit(".", 1)[0]
            # Get the filename suffix, expecting: (Primary | Secondary | Trim | Weapon)
            f_suffix = f_no_ext.rsplit("_", 1)[-1]
            if f_suffix in file_suffix:

                # Get the filename prefix, expecting a unit name
                f_prefix = f_no_ext.rsplit("_", 1)[0]

                # Register unit name as a key to a dictionary containing the filename
                # as a value and their suffix as key
                if not f_prefix in files_dict:
                    files_dict[f_prefix] = {}
                files_dict[f_prefix][f_suffix] = file
        check_if_tem_exist(files_dict)
        return files_dict

    filenames = [
        filename for filename
        in os.listdir(path)
        if filename.endswith(src_format)
    ]
    return find_tem_files(filenames)


def convert_tem_texture(tem_textures: dict, path: Path):
    # TODO: Find a way to handle icon banner pasted on textures
    # TODO: Check the size of Dawn of War 1 unit textures
    # can the different textures for the same unit differ in size?

    black_pixel_threshold = 25
    bands = []
    assert len(tem_textures) == 4, \
        f"There should be 4 tem textures, found only {len(tem_textures)}"

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

    return Image.merge(mode="RGBA", bands=bands)


def exec_convert(path: Path, src_format: str, dest_format: str):
    files_dict = get_tem_filenames(path, src_format)
    for k in files_dict.keys():
        result = convert_tem_texture(files_dict.get(k), path)
        filename = k.replace("default", "tem", 1)
        result.save(path / (f"{filename}.{dest_format}"), dest_format)


def local_test():
    # Put test sample texture in /assets/dow1 directory
    path = Path.cwd() / "assets/dow1"
    exec_convert(path, ".tga", "tga")


if __name__ == "__main__":
    local_test()
