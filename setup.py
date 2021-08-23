import setuptools
import os
from os.path import join, dirname
import re

def get_file_contents(filename):
    package_directory = dirname(__file__)
    with open(join(package_directory, filename), 'r', encoding='utf-8') as file:
        contents = file.read()
    return contents

long_description = """[Documentation](https://coincidencetest.readthedocs.io/en/stable/readme.html).
"""

requirements = []

version = get_file_contents(join('coincidencetest', 'version.txt'))

setuptools.setup(
    name='coincidencetest',
    version=version,
    author='James Mathews',
    author_email='mathewj2@mskcc.org',
    description='An exact test for coincidence of feature values along a sample set.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'coincidencetest',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    project_urls = {
        'Documentation': 'https://coincidencetest.readthedocs.io/en/stable/readme.html',
        'Source code': 'https://github.com/jimmymathews/coincidencetest',
    },
    url = 'https://github.com/jimmymathews/coincidencetest',
)