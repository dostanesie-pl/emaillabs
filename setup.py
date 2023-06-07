"""Install packages as defined in this file into the Python environment."""
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

test_requirements = []
with open(path.join(this_directory, 'test_requirements.txt')) as f:
    for line in f:
        require = line.split('#', 1)[0].strip()
        if require:
            test_requirements.append(require)
setup(
    name="emaillabs",
    version='0.0.1',
    author="Behoston",
    author_email="mateusz@dostanesie.pl",
    url="https://github.com/dostanesie-pl/emaillabs",
    description="Emaillabs Python client",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=[
        'requests',
    ],
    extras_require={
        'dev': test_requirements,
    },
    tests_require=test_requirements,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.0",
        'Programming Language :: Python :: 3.11',
        "Topic :: Utilities",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
)
