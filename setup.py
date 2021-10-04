import setuptools
import os
from os.path import join, dirname

def get_file_contents(filename):
    package_directory = dirname(__file__)
    with open(join(package_directory, filename), 'r', encoding='utf-8') as file:
        contents = file.read()
    return contents

long_description = get_file_contents('README.md')
requirements = [
    'pandas==1.3.2',
    'python-igraph==0.9.6',
]
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
    scripts=[
        'scripts/coincidence-clustering',
        'scripts/coincidencetest-plot',
        'scripts/coincidencetest-distribution-plot',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research',
    ],
    package_data={'coincidencetest': ['version.txt']},
    python_requires='>=3.8',
    install_requires=requirements,
    project_urls = {
        'Documentation': 'https://github.com/nadeemlab/coincidencetest',
        'Source code': 'https://github.com/nadeemlab/coincidencetest',
    },
    url = 'https://github.com/nadeemlab/coincidencetest',
)
