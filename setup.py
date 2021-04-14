from setuptools import setup, find_packages

setup(name="dow2-texture-painter",
      version='0.1',
      packages=find_packages(),
      description=("a GUI application to recolor texture from the "
                   "Dawn of War 2 game"),
      entry_points={'console_scripts': [
          'texture-painter = dow2_texture_painter.frame_main:main']},
      )
