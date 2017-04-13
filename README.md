
# IQFeed/DTN Downloader
Python library to access DTN / IQFeed's historical data for Equities and Futures, capable downloading 1 minute historical data from IQFeed client and store it in MongoDB. My modification of the python iqfeed package from https://pypi.python.org/pypi/iqfeed/0.4.3 made to suit my needs.

## Prerequisites
 * Python 2.7, MongoDB, pandas, pymongo, docker
 * IQFeed account
 * IQFeed client (e.g. [quantomatic/iqfeed-latest'](https://github.com/quantmatic/iqfeed-latest))

## Installation
`$ pip install git+https://github.com/Quantmatic/iq2mongo.git`

### Start IQFeed client
`$ docker run -e LOGIN='<username>' -e PASSWORD='<password>' -p 9100:9101 quantomatic/iqfeed-latest`

### Download single instrument (SPY) for 2016
 * Make sure the MongoDB service is running
`$ sudo service mongod restart`
```
import datetime
import time
from iq2mongo import Iqfeedhistoricdata

symbol = 'SPY'
interval = 60 # Makes 1M bars
dateStart = datetime.datetime(2016, 1, 1)
dateEnd = datetime.datetime(2016, 12, 31)
dbname = 'ETF'

iq = Iqfeedhistoricdata(dateStart, dateEnd, interval)

print 'Downloading '+ symbol + ' from IQFeed...'
start = time.time()
ibars = iq.download_symbol(symbol, timeout=11.5, chunk=32768)
elapsed = str(time.time() - start)
print 'Download finished in ' + elapsed + ' seconds.'
print 'Incerting '+ symbol + ' into MongoDB...'
start = time.time()
incert = iq.write_bars_to_mongo(ibars, symbol, dbname)
elapsed = str(time.time() - start)
print 'Incert finished in ' + elapsed + ' seconds.'
```

## License
[Apache License Version 2.0](http://www.apache.org/licenses/)
