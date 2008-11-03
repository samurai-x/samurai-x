import logging
log = logging.getLogger(__name__)

import samuraix

from .logformatter import FDFormatter

def configure_logging(file_level=logging.DEBUG, console_level=logging.DEBUG):
    '''Set up the logging for the client.

    @param file_level: level of logging for files, defaults to logging.DEBUG
    @param console_level: level of logging for the console, defaults to DEBUG
    '''

    console = logging.StreamHandler()
    console.setLevel(console_level)
    formatter_class = FDFormatter
    formatter = formatter_class('[%(asctime)s %(levelname)s %(name)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.root.setLevel(logging.DEBUG)
    logfile = 'lastrun.log'
    lastlog = logging.FileHandler(logfile, 'w')
    lastlog.setLevel(file_level)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s %(name)s %(lineno)d] %(message)s')
    lastlog.setFormatter(formatter)
    logging.getLogger('').addHandler(lastlog)

    log.info('logging everything to %s' % logfile)


def load_config(config=None):
    if config is None:
        from samuraix.defaultconfig import config
    if callable(config):
        config = config()
    samuraix.config = config


def run(app_func=None):
    configure_logging()
    load_config()

    if app_func is None:
        from samuraix.appl import App
        app_func = App

    samuraix.app = app = app_func()

    try:
        app.init()
        app.run()
    except Exception:
        import traceback
        log.error(traceback.format_exc())


