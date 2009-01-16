from setuptools import setup, find_packages
import sys, os

setup(name='sx-bind',
    description="key/button binding plugin for samurai-x2",
    license='BSD',
    packages=['sxbind'],
    entry_points="""
    [samuraix.plugin]
    sxbind = sxbind:SXBind
    """
)


