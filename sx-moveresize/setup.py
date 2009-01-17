from setuptools import setup, find_packages
import sys, os

setup(name='sx-moveresize',
    description="client moving and resizing handlers for samurai-x2",
    license='BSD',
    packages=['sxmoveresize'],
    entry_points="""
    [samuraix.plugin]
    sxmoveresize = sxmoveresize:SXMoveResize
    """
)


