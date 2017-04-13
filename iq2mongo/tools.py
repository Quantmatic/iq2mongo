# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 19:23:10 2017

@author: adminuser
"""
from functools import wraps
import logging
import time
LOG = logging.getLogger() #__name__

def retry(tries, exceptions=None, delay=0):
    """
    Decorator for retrying a function if exception occurs
    Source: https://gist.github.com/treo/728327

    tries -- num tries
    exceptions -- exceptions to catch
    delay -- wait between retries
    """
    exceptions_ = exceptions or (Exception, )

    def _retry(fnc):
        @wraps(fnc)
        def __retry(*args, **kwargs):
            for _ in xrange(tries+1):
                try:
                    return fnc(*args, **kwargs)
                except exceptions_, err:
                    LOG.warning("Exception, retrying...", exc_info=err)
                    time.sleep(delay)
            raise Exception(" - Symbol download timed out , last exception, \
                            moving on to next symbol...")
        return __retry

    return _retry
