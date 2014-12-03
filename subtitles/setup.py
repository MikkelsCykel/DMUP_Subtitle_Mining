# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class ToxTestCommand(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """
        Run all tests
        """
        sys.exit(os.system('tox'))


setup(
    name='Subtitle Miner',
    version='0.1.0',
    author='Andreas Piculell, Mikkel Rømer',
    author_email='andreaspiculell@gmail.com, mikkeloleromer@gmail.com',
    description='This too provides tools for mining and analysing subtitles',
    license='MIT',
    keywords='subtitle mining sentiment analyser',
    url='git@github.com:MikkelsCykel/DMUP_Subtitle_Mining.git',
    py_modules=['sentiment'],
    long_description=open('README.rst').read(),
    install_requires=['docopt>=0.6.0,<0.7.0', 'requests', 'BeautifulSoup',
                      'nltk'],
    cmdclass={'test': ToxTestCommand},
    tests_require=['tox'],
    scripts=['bin/sent'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License'
    ],
)
