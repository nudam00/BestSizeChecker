import json
import time

import cloudscraper

from add import get_settings


class Alias:
    def __init__(self, username, password, margin):
        self.url = "https://sell-api.goat.com/api/v1"
        self.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pl-PL,pl;q=0.9",
            "User-Agent": "alias/1.28.0 (iPhone; iOS 17; Scale/3.00) Locale/en",
            "x-emb-id": "2389040D96C04834A761C65276AC5564",
            "x-emb-st": str(int(time.time() * 1000)),
            "X-PX-AUTHORIZATION": "3",
            "X-PX-ORIGINAL-TOKEN": "3:87ec12c5b4c34832b42e88735f4da9949538cc013cb7ac2c48d8504371518d81:tT/X5LIfW0h1Ymfegj0v4hZx9Oj13sLWXGbw2+PCtg96IiaUfvn0SG5e/GH+QJPIphQY4u6NziXV+nQypGVLhQ==:1000:f9OqYPvRS2ATdeQYm+cskkymJJlSpyDHB++F566kPebKaJwCf2Y4nxse8wunIYMPytrJCPEOm6dZ8rD19SE/JpJH5cWswIgF7i2DQvMEyP+hVIDae1eUTuZViSvGiPlf2hjvkc8kAUbVDx4I72mqHCx6jzH1+F/2qsnWjdxL5lu7s/b+sdA035/eOeXBihKOcOTT08GYQ1EAkgqiFTMQPg==",
            "Connection": "keep-alive",
            "Host": "sell-api.goat.com",
        }
        self.proxy = get_settings("proxy")
        self.scraper = self.__log_in(username, password)
        self.usd = get_settings("usd_rate")
        self.margin = margin

    def __log_in(self, username, password):
        # Logs into alias account

        scraper = cloudscraper.create_scraper()
        data = {"grantType": "password", "username": username, "password": password}

        while True:
            try:
                # r = scraper.post(data=json.dumps(
                #     data), headers=self.headers, url=self.url+'/unstable/users/login', proxies={"https": self.proxy})
                r = scraper.post(
                    data=json.dumps(data),
                    headers=self.headers,
                    url=self.url + "/unstable/users/login",
                )
                access = json.loads(r.text)["auth_token"]["access_token"]
                self.headers["Authorization"] = "Bearer {}".format(access)
                print("Logged into Alias account")
                return scraper
            except:
                continue

    def __get_product(self, sku):
        # Gets product id

        url = "https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2?analyticsTags=%5B%22platform%3Aios%22%2C%22channel%3Aalias%22%5D&distinct=1&facetingAfterDistinct=1&facets=%5B%22product_category%22%5D&filters=%28product_category%3Aclothing%20OR%20product_category%3Ashoes%20OR%20product_category%3Aaccessories%20OR%20product_category%3Abags%29&page=0&query={}".format(
            sku
        )
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
            "Accept-Language": "pl-PL;q=1.0, en-PL;q=0.9",
            "User-Agent": "alias/1.20.1 (com.goat.OneSell.ios; build:763; iOS 16.2.0) Alamofire/5.6.2",
            "x-emb-id": "2389040D96C04834A761C65276AC5564",
            "x-emb-st": str(int(time.time() * 1000)),
            "X-Algolia-API-Key": "838ecd564b6aedc176ff73b67087ff43",
            "X-Algolia-Application-Id": "2FWOTDVM2O",
            "Connection": "keep-alive",
            "Host": "2fwotdvm2o-dsn.algolia.net",
        }
        # r = self.scraper.get(headers=headers, url=url,
        #                      proxies={"https": self.proxy})
        r = self.scraper.get(headers=headers, url=url)
        try:
            return str([x["slug"] for x in json.loads(r.text)["hits"]][0])
        except IndexError:
            print("Alias: No product found")
            return False

    def get_sizes(self, sku, net_price):
        # Gets sizes
        product = self.__get_product(sku)

        if product == False:
            return None
        data = {
            "variant": {
                "id": product,
                "packagingCondition": "1",
                "consigned": "false",
                "regionId": "2",
            }
        }
        # rows = json.loads(self.scraper.post(data=json.dumps(
        #     data), headers=self.headers, url=self.url+'/analytics/list-variant-availabilities', proxies={"https": self.proxy}).text)
        rows = json.loads(
            self.scraper.post(
                data=json.dumps(data),
                headers=self.headers,
                url=self.url + "/analytics/list-variant-availabilities",
            ).text
        )
        sizes = []
        for row in rows["availability"]:
            if row["variant"]["product_condition"] == "PRODUCT_CONDITION_NEW":
                try:
                    size = row["variant"]["size"]
                except:
                    continue

                # If less than 10 sales then pass
                if "." not in str(size):
                    s = str(size) + ".0"
                else:
                    s = str(size)
                data = {
                    "count": "10",
                    "variant": {
                        "id": product,
                        "size": s,
                        "productCondition": "1",
                        "packagingCondition": "1",
                        "consigned": "false",
                        "regionId": "2",
                    },
                }
                # sales = json.loads(self.scraper.post(data=json.dumps(
                #     data), headers=self.headers, url=self.url+'/analytics/orders/recent', proxies={"https": self.proxy}).text)
                time.sleep(1)
                sales = json.loads(
                    self.scraper.post(
                        data=json.dumps(data),
                        headers=self.headers,
                        url=self.url + "/analytics/orders/recent",
                    ).text
                )
                try:
                    if len(sales["recent_sales"]) < 10:
                        continue
                except:
                    # If empty
                    continue

                try:
                    price = int(row["lowest_price_cents"][:-2]) - 1
                    if self.__get_price(net_price, price):
                        sizes.append(size)
                except:
                    pass
        return sizes

    def __get_price(self, net_price, price):
        # Compares self.margin from settings to margin based on alias price in USD and net price in PLN

        try:
            price = (price * 0.905 - 6) * self.usd * 0.971
            if (price - net_price) / net_price >= self.margin:
                return True
            else:
                return False
        except (TypeError, ValueError):
            return False
