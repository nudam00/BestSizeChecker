from sites.alias import Alias
from sites.stockx import StockX
from add import get_settings
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import os
from openpyxl import Workbook
import pandas as pd


if __name__ == "__main__":
    print('sneakers.xlsx:\n'
          '1. Write sku\n'
          "2. Write net price in PLN\n"
          "3. Optional: Write PID from Zalando\n"
          '\n'
          'Write anything when you would like to start\n')
    input()

    # Preparing
    try:
        os.remove("output/sizes.xlsx")
    except FileNotFoundError:
        pass
    wb = Workbook()
    wb.save(filename='output/sizes.xlsx')
    sheets = pd.ExcelFile('input/sneakers.xlsx').sheet_names

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=300)
        page = browser.new_page()
        stealth_sync(page)

        # Logging in
        alias = Alias(get_settings('username'), get_settings(
            'alias_password'), get_settings('margin'))
        stockx = StockX(get_settings('username'), get_settings(
            'stockx_password'), get_settings('margin'), page, get_settings('stockx_fee'))

        df = pd.DataFrame(
            columns=['Product_name', 'SKU', 'StockX_sizes', 'Alias_sizes', 'PID'])
        excel = pd.read_excel('input/sneakers.xlsx')

        for index, row in excel.iterrows():
            # Per each row - find best sizes
            sku = row['sku']
            price = float(str(row['price_net']).replace(',', '.'))
            try:
                pid = row['pid']
            except:
                pid = ''

            alias_sizes = alias.get_sizes(sku, price)
            stockx_data = stockx.get_sizes(sku, price)
            product_name = stockx_data[0]
            stockx_sizes = stockx_data[1]

            new_row = {'Product_name': product_name, 'SKU': sku,
                       'StockX_sizes': stockx_sizes, 'Alias_sizes': alias_sizes, 'PID': pid}

            df = df.append(new_row, ignore_index=True)
            print('\n'+product_name)
            print(sku)
            print(
                {'StockX_sizes: ': stockx_sizes, 'Alias_sizes': alias_sizes})

    with pd.ExcelWriter('output/sizes.xlsx', engine='openpyxl', mode='a') as writer:
        df.to_excel(writer)
