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
