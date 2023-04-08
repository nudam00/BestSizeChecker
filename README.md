# SneakersBestSizes

Find sizes where profit is above given margin. Scrapped sites:

1. StockX (playwright) - prices must be in USD.
2. Alias (requests) - prices must be in USD.
   <br />
   StockX sometimes ends up blocked by PerimeterX, so the program will notify you when something is wrong and PerimeterX needs to be resolved.<br />

## Converters

Converts sizes from US to EU sizes.

## Input

### settings.json - write your credentials on Alias and StockX, your StockX fee and margin.

`{"email": "x", "alias_username": "x", "alias_password": "x", "stockx_password": "x", "stockx_fee": 0.x, "margin": x, "adidas_margin": x, "usd_rate": x, "proxy": "http://username:passw@ip:port"}`

### sneakers.xlsx

1. Write SKU.
2. Write net price.
3. Optional: write PID (for example Zalando, it is used for output only).
   <br />

## Output

### sizes.xslx

Look at best sizes in EU.
<br />

## Sites

stockx.py, alias.py - checks sizes, performs logging in, finds product page, compares to net_price.
<br />

## add.py

Some additional functions.

## main.py

It brings the whole program together. Calls methods based on data in sneakers.xlsx and writes sizes to sizes.xlsx.
