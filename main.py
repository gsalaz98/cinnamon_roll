import json

import time

import numpy as np
import pyqtgraph as pg
import pandas as pd
import redis

from datetime import datetime
from OpenGL import GL

app = pg.QtGui.QApplication([])

pg.setConfigOptions(useOpenGL=True, useWeave=True)

r = redis.StrictRedis(host='localhost', port=6379)
p = r.pubsub()

p.subscribe('gdax')

data = []
l2_data_bids = []
l2_data_asks = []
plot = pg.plot(x=[time.time()], y=[0], pen=None, style=None)
timer = pg.QtCore.QTimer()

bid = 1 << 5
ask = 1 << 4
trade = 1 << 3

time_start = time.time()

def realtime_update():
    global data
    global l2_data

    message = True

    while message is not None:
        message = p.get_message()

        if message is None:
            return

        if not isinstance(message['data'], bytes):
            return

        message_json = json.loads(message['data'])

        for tick in message_json:
            if tick['symbol'] == 'ETH-USD':
                if tick['event'] & trade == trade:
                    pass
                    #data.append((tick['ts'] - time_start, np.log(tick['price'])))
                    #plot.plot(np.array(data), pen=pg.mkPen(color=(255, 0, 0), style=pg.QtCore.Qt.SolidLine))
                else:
                    if tick['event'] & ask == ask:
                        plot.plot(x=[tick['ts']], y=[tick['price']], pen=None, symbol='+')
                    else:
                        plot.plot(x=[tick['ts']], y=[tick['price']], pen=None, symbol='o')


#timer.timeout.connect(realtime_update)
#timer.start(10)

def plot_from_csv():
    data = pd.read_csv('gdax_ETH-USD.csv', header=None)
    data.columns = ['ts', 'seq', 'is_trade', 'is_bid', 'price', 'size']

    data['price'] = data['price'].apply(np.log)

    trades = data[data['is_trade'] == True]
    l2_updates = data[data['is_trade'] == False]
    l2_bids = l2_updates[l2_updates['is_bid'] == True]
    l2_asks = l2_updates[l2_updates['is_bid'] == False]

    plot.plot(x=l2_bids['ts'].values - l2_bids['ts'].iloc[0], y=l2_bids['price'].values, pen=None, symbol='+') #symbolSize=l2_bids['size'].apply(np.log).values)
    plot.plot(x=l2_asks['ts'].values - l2_asks['ts'].iloc[0], y=l2_asks['price'].values, pen=None, symbol='o')
    plot.plot(x=trades['ts'].values - trades['ts'].iloc[0], y=trades['price'].values, pen=pg.mkPen(255, 0, 0), style=pg.QtCore.Qt.SolidLine)


plot_from_csv()

app.exec_()
