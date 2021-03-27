import configparser
from dow2_color import dow2_colors
import pprint

config = configparser.ConfigParser()
config.read("army_pattern.ini")
color_key = [
    "primaryColourName",
    "secondaryColourName",
    "tintColourName",
    "extraColourName",
]

army_color_preset = {}
for army_name, pattern in config.items():
    team_color = []
    if army_name == "DEFAULT":
        continue
    for key in color_key:
        color_name = pattern.get(key)
        team_color.append(dow2_colors.get(color_name).get("team_colour"))
    army_color_preset[army_name] = team_color
