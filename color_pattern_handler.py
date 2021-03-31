import configparser
from collections import OrderedDict
from dow2_materials import dow2_materials
import json
import os

config = configparser.ConfigParser()
config.read("default_pattern.ini")
color_key = [
    "primary_colour_name",
    "secondary_colour_name",
    "tint_colour_name",
    "extra_colour_name",
]

army_color_pattern = {}

def rgb_to_hex(rgb):
    return '#' + '%02x%02x%02x' % rgb

def get_pattern_dict():
    default_pattern_dict = {}
    for army_name, pattern in config.items():
        team_color = []
        if army_name == "DEFAULT":
            continue
        for key in color_key:
            color_name = pattern.get(key)
            team_color.append(dow2_materials.get(color_name).get("team_colour"))
        default_pattern_dict[army_name] = team_color
    return default_pattern_dict

def dump_default_pattern():
    default_pattern_dict = get_pattern_dict()
    for k, v in default_pattern_dict.items():
        pattern_dict = {}
        for _, (key, value) in enumerate(zip(color_key, v)):
            pattern_dict[key] = rgb_to_hex(value)
        default_pattern_dict[k] = pattern_dict

    with open("army_pattern.json", 'w') as fp:
        json.dump(army_color_pattern, fp, indent=2, ensure_ascii=False)

def save(name: str, colors: list):
    if army_color_pattern.get(str) is not None:
        raise ValueError
    pattern_dict = {}
    for _, (key, value) in enumerate(zip(color_key, colors)):
        pattern_dict[key] = value
    army_color_pattern[name] = pattern_dict
    with open("army_pattern.json", 'w') as fp:
        json.dump(army_color_pattern, fp, indent=2, ensure_ascii=False)

def delete(name: str):
    army_color_pattern.pop(name)
    with open("army_pattern.json", 'w') as fp:
        json.dump(army_color_pattern, fp, indent=2, ensure_ascii=False)

if not os.path.isfile(os.curdir + "/army_pattern.json"):
    dump_default_pattern()

with open("army_pattern.json", 'r') as fp:
    army_color_pattern = json.load(fp, object_pairs_hook=OrderedDict)
