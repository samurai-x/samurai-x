from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='samurai-x',
    version=version,
    description="a simple window manager written in python",
    long_description="""\
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='dunk fordyce',
    author_email='dunkfordyce@gmail.com',
    url='http://code.google.com/p/samurai-x',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      # -*- Extra requirements: -*-
    ],
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    samurai-x = samuraix.main:run
    sx-runner = samuraix.simplexapp:run_runner
    sx-clock = samuraix.simplexapp:run_clock
    sx-setroot = samuraix.setroot:run
    """,
)


