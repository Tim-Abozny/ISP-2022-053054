from setuptools import setup, find_packages

setup(
    name='converter',
    version='1.0.0',
    url='https://github.com/Tim-Abozny',
    license='',
    author='Tim-Abozny',
    author_email='tim.obozny@gmail.com',
    description='Module for converting to most popular notations (such as JSON, Toml, Yaml or Pickle)',
    packages=find_packages('.'),
    python_requires='>3.8.0',
    entry_points={
        'console_scripts': [
            'converter=parsers.json.main:main',
        ],
    },
)
