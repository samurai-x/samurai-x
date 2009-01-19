from setuptools import setup, find_packages
import sys, os

setup(name='sx-tiling',
    description="tiling window manager plugin",
    license='BSD',
    packages=['sxtiling'],
    entry_points="""
    [samuraix.plugin]
    sxtiling = sxtiling:SXTiling
    """
)


