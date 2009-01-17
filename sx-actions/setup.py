from setuptools import setup, find_packages
import sys, os

setup(name='sx-actions',
    description="a simple interface for actions",
    license='BSD',
    packages=['sxactions'],
    entry_points="""
    [samuraix.plugin]
    sxactions = sxactions:SXActions
    """
)


