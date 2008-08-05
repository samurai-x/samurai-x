from setuptools import setup, find_packages
import sys, os

setup(name='samurai-x',
    version="0.1",
    description="A window manager written in pure python",
    long_description="""\
samurai-x is a window manager written in pure python. This is acheived through 
use of the ctypes module and xlib.  

Currently no releases have been made. To easy_install the development version use:
    $ easy_install samurai-x==dev

http://samurai-x.googlecode.com/svn/trunk/samurai-x/#egg=samurai-x-dev
""",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Desktop Environment :: Window Managers',
    ], 
    keywords='window manager xlib X11',
    author='Dunk Fordyce',
    author_email='dunkfordyce@gmail.com',
    url='http://code.google.com/p/samurai-x',
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "pyglet>=1.1",
    ],
    entry_points="""
    [console_scripts]
    samurai-x = samuraix.main:run
    #sx-runner = samuraix.simplexapp:run_runner
    #sx-clock = samuraix.simplexapp:run_clock
    sx-setroot = samuraix.setroot:run
    """,
)


