# Cryptocurrency historical data collection script

Requires Python 3

Polls global stats and data on the top 10 cryptocurrencies (by trade-volume), and stores in Firebase for aggregation. I use this with AWS Lambda to collect data every 5-minutes.

You can add this to AWS Lambda and have it execute on a 5-minute schedule. Lambda requires all dependencies be uploaded directly with the script, so get the dependencies into your project with 

`pip3 install --ignore-installed --install-option="--prefix=/Path/To/Project" pyrebase`
`pip3 install --ignore-installed --install-option="--prefix=/Path/To/Project" coinmarketcap`

If they end up in deeply nested site-packages, move them to the top level so they are next to `coin_op.py`.

`Pyrebase` uses native `Crypto` package which isn't allowed to run on Lambda. To get around this, remove references of `Crypto` in `pyrebase.py` and delete the `crypto` and `jwt` since they are large and dead weight at this point.
