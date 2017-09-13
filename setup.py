from distutils.core import setup
from cx_Freeze import setup, Executable

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
