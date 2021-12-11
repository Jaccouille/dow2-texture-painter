import os

APP_DIR = "src"
RES_DIR = "resources"
APP_VERSION = "0.1"
APP_NAME = "dow2-texture-painter"

cmd = (f"pyinstaller --name {APP_NAME}-{APP_VERSION} --windowed --noconfirm "
      f"--add-data \"{APP_DIR}/{RES_DIR};{RES_DIR}\" "
      f"--icon=\"{APP_DIR}/{RES_DIR}/icon_64x64.ico\" "
      "--add-data \"readme.md;.\" --hidden-import='PIL._tkinter_finder' "
      f"{APP_DIR}/frame_main.py"
      )

print(cmd)
os.system(cmd)
