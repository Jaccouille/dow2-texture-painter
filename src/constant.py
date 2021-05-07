from enum import Enum


class ColorOps(Enum):
    OVERLAY = "Overlay"
    SCREEN = "Screen"
    MULTIPLY = "Multiply"


OPEN_FILETYPES = (
    ("all", (".dds", ".png", ".jpg", ".bmp", ".tga", ".blp")),
    ("Direct Draw Surface", ".dds"),
    ("Portable Network Graphics", ".png"),
    ("JPEG Image", ".jpg"),
    ("Bitmap", ".bmp"),
    ("True Vision Targa", ".tga"),
    ("Blizzard Texture", ".blp"),
)
SAVE_FILETYPES = (
    ("Portable Network Graphics", ".png"),
    ("JPEG Image", ".jpg"),
    ("Bitmap", ".bmp"),
    ("True Vision Targa", ".tga"),
)
OPEN_EXT_LIST = [fmt[1][1:] for fmt in OPEN_FILETYPES[1:]]
SAVE_EXT_LIST = [fmt[1][1:] for fmt in SAVE_FILETYPES]
COLOR_BOX_SIZE = 90
COLOR_BTN_HEIGHT = 26
FRAME_TOOL_HEIGHT = COLOR_BOX_SIZE + COLOR_BTN_HEIGHT + 90

DEFAULT_IMG_SIZE = 256


# Dawn of War 2 original materials data
DOW2_MATERIALS = {
    "Chaos Black": {
        "team_colour": (10, 10, 10),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Coal Black": {
        "team_colour": (25, 25, 25),
        "team_specular": (1, 1, 1),
        "team_gloss": 0,
    },
    "Boltgun Metal": {
        "team_colour": (50, 50, 50),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Charadon Granite": {
        "team_colour": (75, 75, 75),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Adeptus Battlegrey": {
        "team_colour": (100, 100, 100),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.0,
    },
    "Codex Grey": {
        "team_colour": (125, 125, 125),
        "team_specular": (1, 1, 1),
        "team_gloss": 0,
    },
    "Astronomican Grey": {
        "team_colour": (150, 150, 150),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Fortress Grey": {
        "team_colour": (175, 175, 175),
        "team_specular": (1, 1, 0),
        "team_gloss": 0,
    },
    "Light Grey": {
        "team_colour": (200, 200, 200),
        "team_specular": (1, 1, 0),
        "team_gloss": 0,
    },
    "Skull White": {
        "team_colour": (255, 255, 255),
        "team_specular": (3, 3, 1),
        "team_gloss": 0,
    },
    "Dheneb Stone": {
        "team_colour": (189, 173, 157),
        "team_specular": (3, 2, 0),
        "team_gloss": 0,
    },
    "Bleached Bone": {
        "team_colour": (236, 214, 158),
        "team_specular": (2, 2, 1),
        "team_gloss": 0,
    },
    "Bone": {
        "team_colour": (170, 150, 115),
        "team_specular": (1, 1, 0),
        "team_gloss": 0,
    },
    "Kommando Khaki": {
        "team_colour": (145, 121, 99),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Khemri Brown": {
        "team_colour": (110, 79, 63),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Tin Bitz": {
        "team_colour": (57, 48, 39),
        "team_specular": (5, 3, 2),
        "team_gloss": 0,
    },
    "Ork Leather": {
        "team_colour": (50, 40, 28),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Graveyard Earth": {
        "team_colour": (81, 56, 32),
        "team_specular": (1, 0, 0),
        "team_gloss": 0,
    },
    "Dried Blood": {
        "team_colour": (74, 45, 28),
        "team_specular": (3, 0, 0),
        "team_gloss": 0,
    },
    "Scorched Brown": {
        "team_colour": (68, 34, 25),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Calthan Brown": {
        "team_colour": (106, 50, 34),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Snakebite Leather": {
        "team_colour": (153, 83, 33),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Iyanden Darksun": {
        "team_colour": (192, 132, 51),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Flesh Wash": {
        "team_colour": (202, 143, 71),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Elf Flesh": {
        "team_colour": (240, 163, 88),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Tau Sept Ochre": {
        "team_colour": (167, 89, 39),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Tanned Flesh": {
        "team_colour": (162, 68, 38),
        "team_specular": (16, 6, 3),
        "team_gloss": 0,
    },
    "Vermin Brown": {
        "team_colour": (127, 45, 16),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Terracotta": {
        "team_colour": (102, 32, 22),
        "team_specular": (5, 2, 2),
        "team_gloss": 0,
    },
    "Bestial Brown": {
        "team_colour": (90, 26, 18),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Dark Flesh": {
        "team_colour": (70, 15, 15),
        "team_specular": (5, 1, 1),
        "team_gloss": 0,
    },
    "Blood Raven Red": {
        "team_colour": (100, 20, 0),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Red Gore": {
        "team_colour": (149, 16, 35),
        "team_specular": (7, 1, 1),
        "team_gloss": 0,
    },
    "Scab Red": {
        "team_colour": (130, 14, 33),
        "team_specular": (7, 1, 1),
        "team_gloss": 0,
    },
    "Mechrite Red": {
        "team_colour": (168, 30, 20),
        "team_specular": (3, 1, 1),
        "team_gloss": 0,
    },
    "Khorne Red": {
        "team_colour": (106, 32, 32),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Macharious Solar Orange": {
        "team_colour": (189, 50, 25),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Blood Red": {
        "team_colour": (203, 0, 26),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Red Ink": {
        "team_colour": (250, 0, 15),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Blazing Orange": {
        "team_colour": (242, 50, 13),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Fiery Orange": {
        "team_colour": (255, 89, 10),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Chestnut Ink": {
        "team_colour": (204, 102, 6),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Vomit Brown": {
        "team_colour": (204, 116, 30),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Bronzed Flesh": {
        "team_colour": (242, 137, 27),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Golden Yellow": {
        "team_colour": (255, 190, 5),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Sunburst Yellow": {
        "team_colour": (255, 217, 2),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Bad Moon Yellow": {
        "team_colour": (255, 255, 0),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Desert Yellow": {
        "team_colour": (141, 112, 53),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.0,
    },
    "Gretchin Green": {
        "team_colour": (107, 91, 32),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Camo Green": {
        "team_colour": (116, 125, 58),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Scorpion Green": {
        "team_colour": (90, 168, 35),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Goblin Green": {
        "team_colour": (52, 121, 52),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Snot Green": {
        "team_colour": (20, 111, 37),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Dark Angels Green": {
        "team_colour": (31, 75, 39),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Knarloc Green": {
        "team_colour": (61, 68, 47),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Catachan Green": {
        "team_colour": (36, 42, 34),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Nurgle Green": {
        "team_colour": (102, 119, 73),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Orkhide Shade": {
        "team_colour": (35, 47, 43),
        "team_specular": (3, 4, 3),
        "team_gloss": 0.00,
    },
    "Swamp Green": {
        "team_colour": (29, 87, 78),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Dark Green Ink": {
        "team_colour": (22, 128, 114),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Scale Turquoise": {
        "team_colour": (13, 91, 92),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Hawk Turquoise": {
        "team_colour": (5, 98, 120),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Space Wolves Grey": {
        "team_colour": (117, 153, 168),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Ice Blue": {
        "team_colour": (141, 212, 219),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Glacier Blue": {
        "team_colour": (75, 148, 188),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Shadow Grey": {
        "team_colour": (44, 90, 124),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.00,
    },
    "Enchanted Blue": {
        "team_colour": (9, 84, 157),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Ultramarines Blue": {
        "team_colour": (12, 65, 154),
        "team_specular": (1, 3, 7),
        "team_gloss": 0,
    },
    "Void Blue": {
        "team_colour": (25, 40, 250),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Mordian Blue": {
        "team_colour": (31, 49, 131),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Midnight Blue": {
        "team_colour": (8, 17, 70),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Necron Abyss": {
        "team_colour": (18, 26, 52),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Regal Blue": {
        "team_colour": (5, 44, 82),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Fenris Blue": {
        "team_colour": (35, 55, 90),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Hormagaunt Purple": {
        "team_colour": (67, 51, 97),
        "team_specular": (7, 5, 10),
        "team_gloss": 0.00,
    },
    "Leviathan Black": {
        "team_colour": (33, 16, 50),
        "team_specular": (2, 1, 3),
        "team_gloss": 0,
    },
    "Leviathan Purple": {
        "team_colour": (172, 146, 211),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.0,
    },
    "Purple Ink": {
        "team_colour": (129, 44, 146),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Warlock Purple": {
        "team_colour": (152, 24, 124),
        "team_specular": (0, 0, 0),
        "team_gloss": 0,
    },
    "Liche Purple": {
        "team_colour": (90, 2, 88),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.0,
    },
    "Magenta Ink": {
        "team_colour": (217, 4, 126),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.0,
    },
    "Tenticle Pink": {
        "team_colour": (224, 137, 194),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.0,
    },
    "Dwarf Flesh": {
        "team_colour": (222, 129, 112),
        "team_specular": (22, 13, 11),
        "team_gloss": 0.0,
    },
    "Tallarn Flesh": {
        "team_colour": (205, 170, 158),
        "team_specular": (0, 0, 0),
        "team_gloss": 0.0,
    },
    "Metallic Gold": {
        "team_colour": (110, 104, 53),
        "team_specular": (85, 95, 40),
        "team_gloss": 0.01,
    },
    "Metallic Silver": {
        "team_colour": (167, 165, 176),
        "team_specular": (140, 134, 138),
        "team_gloss": 0.01,
    },
    "Scaly Green": {
        "team_colour": (5, 55, 70),
        "team_specular": (1, 5, 7),
        "team_gloss": 0.1,
    },
    "Platinum": {
        "team_colour": (100, 100, 95),
        "team_specular": (100, 100, 100),
        "team_gloss": 0.01,
    },
    "Golden Purple": {
        "team_colour": (42, 36, 89),
        "team_specular": (25, 15, 4),
        "team_gloss": 0.2,
    },
    "Metallic Red": {
        "team_colour": (128, 0, 0),
        "team_specular": (128, 0, 0),
        "team_gloss": 0.1,
    },
    "Shining Gold": {
        "team_colour": (217, 170, 34),
        "team_specular": (41, 34, 7),
        "team_gloss": 0.1,
    },
    "Gold": {
        "team_colour": (200, 145, 71),
        "team_specular": (31, 22, 7),
        "team_gloss": 0.1,
    },
    "Mithril Silver": {
        "team_colour": (97, 95, 93),
        "team_specular": (27, 25, 23),
        "team_gloss": 0.1,
    },
    "Abyss Purple": {
        "team_colour": (10, 10, 10),
        "team_specular": (12, 5, 50),
        "team_gloss": 0.1,
    },
    "Insect Green": {
        "team_colour": (41, 71, 46),
        "team_specular": (5, 46, 23),
        "team_gloss": 0.1,
    },
    "Iron": {
        "team_colour": (30, 30, 40),
        "team_specular": (75, 75, 95),
        "team_gloss": 0.05,
    },
    "Abyss Orange": {
        "team_colour": (10, 10, 10),
        "team_specular": (74, 55, 14),
        "team_gloss": 0.1,
    },
    "Brazen Brass": {
        "team_colour": (133, 115, 62),
        "team_specular": (73, 64, 33),
        "team_gloss": 0.05,
    },
    "Metallic Blue": {
        "team_colour": (0, 0, 128),
        "team_specular": (0, 0, 128),
        "team_gloss": 0.1,
    },
    "Burnished Gold": {
        "team_colour": (228, 190, 98),
        "team_specular": (182, 136, 31),
        "team_gloss": 0.1,
    },
    "Abyss Red": {
        "team_colour": (15, 3, 3),
        "team_specular": (30, 2, 2),
        "team_gloss": 0.2,
    },
    "Metallic Green": {
        "team_colour": (0, 80, 0),
        "team_specular": (0, 80, 0),
        "team_gloss": 0.1,
    },
    "Crystal Blue": {
        "team_colour": (76, 91, 166),
        "team_specular": (145, 92, 162),
        "team_gloss": 0.1,
    },
    "Dwarf Bronze": {
        "team_colour": (167, 116, 65),
        "team_specular": (78, 53, 29),
        "team_gloss": 0.01,
    },
    "Abyss Blue": {
        "team_colour": (3, 3, 15),
        "team_specular": (2, 2, 30),
        "team_gloss": 0.2,
    },
    "Abyss Magenta": {
        "team_colour": (10, 10, 10),
        "team_specular": (50, 5, 12),
        "team_gloss": 0.1,
    },
    "Bubonic Brown": {
        "team_colour": (228, 128, 35),
        "team_specular": (10, 5, 1),
        "team_gloss": 0.1,
    },
    "Abyss yellow": {
        "team_colour": (10, 10, 10),
        "team_specular": (130, 120, 0),
        "team_gloss": 0.1,
    },
    "Chainmail": {
        "team_colour": (102, 102, 111),
        "team_specular": (49, 54, 57),
        "team_gloss": 0.05,
    },
    "Abyss Green": {
        "team_colour": (3, 15, 3),
        "team_specular": (2, 30, 2),
        "team_gloss": 0.2,
    },
    "Rotting Flesh": {
        "team_colour": (182, 196, 136),
        "team_specular": (18, 19, 13),
        "team_gloss": 0.02,
    },
    "Bronze": {
        "team_colour": (71, 46, 41),
        "team_specular": (64, 25, 5),
        "team_gloss": 0.2,
    },
    "Metallic Yellow": {
        "team_colour": (255, 190, 5),
        "team_specular": (135, 150, 10),
        "team_gloss": 0.2,
    },
    "Metallic Orange": {
        "team_colour": (100, 20, 0),
        "team_specular": (100, 20, 0),
        "team_gloss": 0.2,
    },
    "Spectral Blue": {
        "team_colour": (41, 71, 246),
        "team_specular": (115, 46, 3),
        "team_gloss": 0.1,
    },
}
