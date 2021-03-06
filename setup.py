"""Install latexplotlib.

This script (setup.py) will copy the matplotlib styles (*.mplstyle) into the
appropriate directory on your computer (OS dependent).

This code is based on SciencePlots:
https://github.com/garrettj403/SciencePlots/blob/master/setup.py

"""

import atexit
import glob
import os
import re
import shutil

import matplotlib
from setuptools import setup
from setuptools.command.install import install

# read version
with open("src/latexplotlib/_version.py", encoding="utf-8") as fh:
    match = re.search(r'__version__ = "(\d\.\d\.\d)"', fh.read())

if match:
    version = match.group(1)
else:
    raise RuntimeError("Could not parse version number.")


def install_styles():
    # Find all style files
    stylefiles = glob.glob("styles/**/*.mplstyle", recursive=True)
    # Find stylelib directory (where the *.mplstyle files go)
    mpl_stylelib_dir = os.path.join(matplotlib.get_configdir(), "stylelib")
    if not os.path.exists(mpl_stylelib_dir):
        os.makedirs(mpl_stylelib_dir)
    # Copy files over
    print("Installing styles into", mpl_stylelib_dir)
    for stylefile in stylefiles:
        print(os.path.basename(stylefile))
        shutil.copy(
            stylefile, os.path.join(mpl_stylelib_dir, os.path.basename(stylefile))
        )


class PostInstallMoveFile(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(install_styles)


setup(
    version=version,
    cmdclass={
        "install": PostInstallMoveFile,
    },
    package_data={"latexplotlib": ["py.typed"]},
)
