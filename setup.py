"""
Publish a new version:
$ git tag X.Y.Z -m "Release X.Y.Z"
$ git push --tags
$ pip install --upgrade twine wheel
$ python setup.py sdist bdist_wheel --universal
$ twine upload dist/*
"""
import codecs
from setuptools import setup


def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with codecs.open(filename, 'r', 'utf8') as f:
        return f.read()


setup(
    name='mongodb-statedb',
    packages=['mongodb_statedb'],
    version='1.0.1',
    description='Use MongoDB to track state.',
    long_description=read_file('README.rst'),
    license='MIT',
    author='Audrow Nash',
    author_email='audrow@hey.com',
    url='https://github.com/audrow/mongodb-statedb.git',
    keywords=[
        'MongoDB', 'robotics',
    ],
    install_requires=[
        'pymongo',        # mongodb api
        # testing
        'flake8',         # check code style for pep-8
        'mongomock',      # makes testing mongo easier
        'pep257',         # test the doc strings
        'pytest',         # a testing framework
        'pytest-cov',     # for code coverage
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Natural Language :: English',
    ],
    python_requires='>=3.6',
)