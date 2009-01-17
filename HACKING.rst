Hacking on samurai-x
====================

Installing plugins
------------------

The most convenient way to install and develop plugins:

::
    
    mkdir -p ~/.samuraix/plugins
    cd plugin-dir/
    PYTHONPATH=~/.samuraix/plugins python setup.py develop -d ~/.samuraix/plugins

Don't forget to load the plugin in the defaultconfig.py or ~/.samuraix/config!

