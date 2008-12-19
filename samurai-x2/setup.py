from setuptools import setup, find_packages
import sys, os

setup(name='samurai-x2',
    version="0.1",
    description="A window manager written in pure python",
    long_description="""\
samurai-x is a window manager written in pure python using ctypes, xcb and cairo.
""",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Desktop Environment :: Window Managers',
    ], 
    keywords='window manager xcb cairo X11 wm',
    author='Dunk Fordyce',
    author_email='dunkfordyce@gmail.com',
    url='http://samurai-x.org',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    entry_points="""
    [console_scripts]
    sx-wm = samuraix.main:run
    sx-event = samuraix.tools.sevent:run
    #sx-setroot = samuraix.setroot:run
    """,
)


