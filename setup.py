import logging
import platform
import os
from distutils.core import setup


from cx_Freeze import setup, Executable


print(platform.system())


if platform.system() == 'Windows':
    os.environ['TCL_LIBRARY'] = "C:\\Users\\sylvie\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
    os.environ['TK_LIBRARY'] = "C:\\Users\\sylvie\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"


setup(
    name='macgyver',
    version='0.1',
    packages=['game'],
    url='https://github.com/tomlemeuch/macgyver',
    license='GNU GPLv3',
    author='Tom Gabrièle',
    author_email='',
    description='A single level labyrinth game.',
    options={"build_exe": {"packages": ["pygame"], "include_files": ["game/maps", "game/media"]}},
    executables=[Executable("game/main.py")]
)
