from setuptools import setup, find_packages
import sys, os

setup(name='sx-allplugins',
    version="0.1",
    description="meta package containing all the official samurai-x plugins",
    long_description="""\
meta package containing all the official samurai-x plugins
""",
    keywords='window manager xcb cairo X11 wm samurai-x',
    author='Dunk Fordyce',
    author_email='dunkfordyce@gmail.com',
    url='http://samurai-x.org',
    license='BSD',
    install_requires=[
        "sx-actions",
        "sx-autoclient",
        "sx-background",
        "sx-bind",
        "sx-cairodeco",
        "sx-clientbuttons",
        "sx-dbus",
        "sx-desktops",
        "sx-focus",
        "sx-gobject",
        "sx-help",
        "sx-layoutmgr",
        "sx-moveresize",
        #"sx-simpledeco",
        #"sx-tiling",
        "sx-web",
        "yahiko",
    ],
)
