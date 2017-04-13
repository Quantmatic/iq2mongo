# -*- coding: utf-8 -*-
"""
    Load futures data to MongoDB
"""
import datetime
import time
import logging
from iq2mongo import Iqfeedhistoricdata
LOG = logging.getLogger()

symbols = ['@EU#', '@BP#', '@CD#', '@AD#', '@SF#']
interval = 60
dateStart = datetime.datetime(2007, 1, 1)
dateEnd = datetime.datetime(2016, 12, 31)
dbname = 'Future'

iq = Iqfeedhistoricdata(dateStart, dateEnd, interval, 'Future')

pstart = time.time()
for symbol in symbols:
    try:
        print 'Downloading '+ symbol + ' from IQFeed...'
        start = time.time()
        ibars = iq.download_symbol(symbol, timeout=11.5, chunk=32768)
        done = time.time()
        elapsed = str(done - start)
        print 'Download finished in ' + elapsed + ' seconds.'
        if len(ibars):
            print 'Incerting '+ symbol + ' into MongoDB...'
            start = time.time()
            #incert_arctic = iq.arctic_store(ibars, symbol, 'ETF')
            incert = iq.write_bars_to_mongo(ibars, symbol, dbname)
            done = time.time()
            elapsed = str(done - start)
            print 'Incert finished in ' + elapsed + ' seconds.'
        else:
            print 'No bars for ' + symbol + ' downloaded'
    except Exception as err:
        LOG.error('Exception during download, continuing', exc_info=err)

pdone = time.time()
_elapsed = str(pdone - pstart)
print 'Program finished in ' + _elapsed + ' seconds.'
