from setuptools import setup, find_packages
import sys, os

setup(name='pyxcb',
    version="0.1",
    description="A Python Xcb binding using ctypes",
    long_description="pyxcb is a binding to the X C Binding using ctypes.",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ], 
    keywords='xcb X11 binding',
    author='Friedrich Weber',
    author_email='fred.reichbier@googlemail.com',
    url='http://samurai-x.org',
    license='BSD',
    packages=find_packages(),
)


