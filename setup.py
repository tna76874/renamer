
#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from setuptools import find_packages, setup

import renamer

setup(
    name='renamer',
    version=renamer.__version__,
    description='A simple pattern renamer',
    url='https://github.com/tna76874/renamer.git',
    author='maaaario',
    author_email='',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=[
        "argparse",
        "python-slugify",
        "parse",
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.7',
    ],
    python_requires = ">=3.6",
    entry_points={
        "console_scripts": [
            "renamer = renamer.renamer:main",
        ],
    },
    )