from setuptools import setup, find_packages
import sys, os

setup(name='sx-simpledeco',
    description="simple decoration plugin for samurai-x2",
    license='BSD',
    packages=['sxsimpledeco'],
    entry_points="""
    [samuraix.plugin]
    sxsimpledeco = sxsimpledeco:SXDeco
    """
)


