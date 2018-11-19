# cinnamon_roll
Limit Orderbook Replay/Analysis Library

This project serves to provide an easy way to take orderbook/L2 data and rebuild an orderbook from the given data.

It allows for callbacks to be ran every new event so that you can run your own custom calculations on an orderbook at a given time `t`.
More advanced orderbook types will be added in the future in order to maximize the data that can be extracted from generic orderbook delta events.

**N.B.** I built this project with cryptocurrency exchanges in mind, but it might find use in other financial markets.
