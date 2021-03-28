import configparser
from dow2_color import dow2_colors
import pprint
import json

config = configparser.ConfigParser()
config.read("army_pattern.ini")
color_key = [
    "primaryColourName",
    "secondaryColourName",
    "tintColourName",
    "extraColourName",
]


def rgb_to_hex(rgb):
    return '#' + '%02x%02x%02x' % rgb


army_color_preset = {}
for army_name, pattern in config.items():
    team_color = []
    if army_name == "DEFAULT":
        continue
    for key in color_key:
        color_name = pattern.get(key)
        team_color.append(dow2_colors.get(color_name).get("team_colour"))
    army_color_preset[army_name] = team_color

for k, v in army_color_preset.items():
    pattern_dict = {}
    for _, (key, value) in enumerate(zip(color_key, v)):
        pattern_dict[key] = rgb_to_hex(value)
    army_color_preset[k] = pattern_dict
with open("dump.json", 'w') as fp:
    json.dump(army_color_preset, fp, indent=2)
