""" Alex Orion's MongoDB loader for IQFeed historical quotes """
import io
import sys
import socket

import logging
import pymongo
import pandas as pd
from tools import retry

LOG = logging.getLogger()
LOGCONSOLE = logging.StreamHandler(sys.stdout)
LOG.setLevel(logging.INFO)
LOGCONSOLE.setLevel(logging.INFO)
LOG.addHandler(LOGCONSOLE)

class Iqfeedhistoricdata:
    """ download historical datat from iqfeed """
    def __init__(self, startdate, enddate, interval=60, mode='Equity'):

        self.startdate = startdate.strftime("%Y%m%d %H%M%S")
        self.enddate = enddate.strftime("%Y%m%d %H%M%S")
        self.begin_time_filter = '092900'
        self.end_time_filter = '155900'
        self.interval = str(interval)
        self.host = "localhost"  # Localhost
        self.port = 9100  # Historical data socket port

        if mode == 'Future':
            self.begin_time_filter = '000000'
            self.end_time_filter = '235900'

    def read_historical_data_socket(self, sock, chunk_size):
        """
        Read the data from iqfeed_socket with the given chunk size.
        The collected data is returned as a string or exception is raised on error
        """
        buffer_ = ""
        chunk = ""
        end_msg = '\n!ENDMSG!,\r\n'

        while not chunk.endswith(end_msg):
            chunk = sock.recv(chunk_size)

            if chunk.startswith('E,'):  # Error condition
                if chunk.startswith('E,!NO_DATA!'):
                    LOG.warn('No data available for the given instrument')
                    print 'No data available for the given instrument'
                    break
                else:
                    raise Exception(chunk)

            buffer_ += chunk

        # Remove the end message string
        buffer_ = buffer_[:-1 * len(end_msg)]
        # Cut off CR
        buffer_ = buffer_.replace('\r', '')
        #print(buffer_)
        return buffer_

    @retry(5, delay=2)
    def download_symbol(self, symbol, timeout=3.677, chunk=4096):
        """ Send HIT request to iqfeed """

        msg = "HIT,{0},'{1}',{2},{3},,{4},{5},1\n".format(symbol,
                                                          self.interval,
                                                          self.startdate,
                                                          self.enddate,
                                                          self.begin_time_filter,
                                                          self.end_time_filter)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((self.host, self.port))

        sock.sendall(msg)
        data = self.read_historical_data_socket(sock, chunk)
        sock.close()

        dframe = pd.read_csv(
            io.BytesIO('''datetime,high,low,open,close,oi,volume,skip'''+
                       data)
            )

        dframe = dframe[:][['datetime', 'open', 'high', 'low', 'close', 'volume', 'oi']]
        dframe["datetime"] = pd.to_datetime(dframe["datetime"])
        dframe.open = pd.to_numeric(dframe.open)
        dframe.high = pd.to_numeric(dframe.high)
        dframe.low = pd.to_numeric(dframe.low)
        dframe.close = pd.to_numeric(dframe.close)
        dframe.volume = pd.to_numeric(dframe.volume)
        dframe.oi = pd.to_numeric(dframe.oi)

        return dframe


    def write_bars_to_mongo(self, bars, symbol, dbase):
        """incert bars from IqFeed directly to MongoDB database """
        client = pymongo.MongoClient()
        mdb = client[dbase]
        collection = mdb[symbol]
        collection.insert_many(bars.to_dict('records'))
