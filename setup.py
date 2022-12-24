"""
pip setup.py
"""
from setuptools import setup, find_packages

setup(
    name='grasp',
    version='0.17.13',
    packages=find_packages(include=['grasp.py']),
    description='Generating Random Alanine Scanned Peptides',
    author='Ashrith Sagar Yedlapalli',
    author_email='ashrith9sagar@gmail.com',
    url='https://2022.igem.wiki/mit-mahe/software',
    install_requires=[
    'pandas',
    'cardinality'
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    where='src',
    entry_points={
        'console_scripts': ['grasp=grasp.grasp:main']
    }
)
