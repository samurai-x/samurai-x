import logging
log = logging.getLogger(__name__)

def testfunc(*args, **kwargs):
    log.debug("testfunc %s %s" % (str(args), str(kwargs)))


