from setuptools import setup, find_packages
import sys, os

setup(name='sx-desktops',
    description="Desktops plugin for samurai-x2",
    license='BSD',
    packages=['sxdesktops'],
    entry_points="""
    [samuraix.plugin]
    sxdesktops = sxdesktops:SXDesktops
    """
)


