# SneakersBestSizes
Find sizes which profit is above given margin. Sites which are scrapped:
1. StockX (playwright) - prices must be in USD. 
2. Alias (requests) - prices must be in USD.
<br /> 
StockX sometimes ends up blocked by PerimeterX, so the program will notify you when something is wrong and PerimeterX needs to be resolved.<br /> 

## Converters
Converts sizes from US to EU sizes.


## Input
### settings.json - write your credentials on Alias and StockX, your StockX fee and margin.
```{"username": "x", "alias_password": "x", "stockx_password": "x", "stockx_fee": 0.085, "margin": 0.1}```

### sneakers.xlsx
1. Write SKU.
2. Write net price.
3. Optional: write PID (for example Zalando, it is used only for output).
<br />

## Output
### sizes.xslx
Look at StockX and Alias sizes in EU.
<br />

## Sites
stockx.py, alias.py - checks sizes, performs logging in, finds product page, compares to net_price.
<br />

## add.py
Some additional functions.

## main.py
It brings the whole program together. Calls methods based on data in sneakers.xlsx and writes sizes to sizes.xlsx.