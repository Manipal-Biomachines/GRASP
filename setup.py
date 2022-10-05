"""
pip setup.py
"""
from setuptools import setup, find_packages

setup(
    name='pep_mod',
    version='0.17.0',
    packages=find_packages(include=['pep_mod.py']),
    description='Peptide sequence mutater using Alanine Scanning',
    author='Ashrith Sagar Yedlapalli',
    author_email='ashrith9sagar@gmail.com',
    url='https://2022.igem.wiki/mit-mahe/software',
    install_requires=[
    'pandas'
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['pep_mod=pep_mod.pep_mod:main']
    }
)
