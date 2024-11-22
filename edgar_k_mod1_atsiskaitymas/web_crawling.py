"""
Module providing a web crawling method/function
that allows to return structured different type data
from varle.lt/ispardavimas
"""

import time
from datetime import datetime, timedelta

from lxml import html
from requests import get


class WebCrawling:
    """Class allows to return structured different type data"""

    def __init__(self, time_limit: int, source: str, return_format: str):
        self.time_limit = time_limit
        self.source = source
        self.return_format = return_format
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=self.time_limit)

    def check_time(self):
        """Check if the current time is within the allowed time limit."""
        return datetime.now() < self.end_time

    def scrape_page_varle(self, url):
        response = get(url)
        tree = html.fromstring(response.content)

        titles = tree.xpath('//div[contains(@class, "GRID_ITEM")]')
        extracted = []

        for product in titles:
            try:
                name = product.xpath(
                    ".//div[contains(@class, 'product-title')]//a/text()"
                )
                price1 = product.xpath(
                    ".//div[contains(@class, 'price-container')]"
                    "//div[contains(@class, 'price-tag')]"
                    "//div[contains(@class, 'price-mid-section')]"
                    "//span/span/text()"
                )
                price2 = product.xpath(
                    ".//div[contains(@class, 'price-container')]"
                    "//div[contains(@class, 'price-tag')]"
                    "//div[contains(@class, 'price-mid-section')]"
                    "//span/sup/text()"
                )

                name = name[0].strip() if name else "Unknown"
                price1 = price1[0].strip().replace("\xa0", "") if price1 else None
                price2 = price2[0].strip().replace("\xa0", "") if price2 else None

                full_price = f"{price1}{price2}" if price1 and price2 else price1

                extracted.append(
                    {
                        "name": name,
                        "price1": price1,
                        "price2": price2,
                        "full_price": full_price,
                    }
                )
            except IndexError:
                print(f"Failed to parse product: {product}")

        for item in extracted:
            if self.return_format == "txt":
                with open("varle_rezultatas.txt", "a", encoding="utf-8") as failas:
                    failas.write(
                        f"Product Name: {item['name']}, "
                        f"Full Price: {item['full_price']}\n"
                    )
            if self.return_format == "csv":
                with open("varle_rezultatas.csv", "a", encoding="utf-8") as failas:
                    failas.write(
                        f"Product Name: {item['name']}, "
                        f"Full Price: {item['full_price']}\n"
                    )

    def get_next_page_varle(self, tree):
        next_page = tree.xpath('//li[@class="wide "]/a[@class="for-desktop"]/@href')
        return next_page[0] if next_page else None

    def crawl(self):
        """Add description"""
        start_page = 1
        base_url = "https://www.varle.lt/ispardavimas/"
        current_page = start_page

        while self.check_time():
            if self.source == "varle":
                url = f"{base_url}?p={current_page}"
                print(f"Scraping page {current_page} from URL: {url}")

                self.scrape_page_varle(url)

                response = get(url)
                tree = html.fromstring(response.content)
                next_page_url = self.get_next_page_varle(tree)

                if not next_page_url:
                    print("No more pages found.")
                    break

                current_page += 1

            time.sleep(2)


def crawl(time_limit: int, source: str, return_format: str):
    """
    A functions that calls a crawl() method form the WebCrawling class
    """
    crawler = WebCrawling(time_limit, source, return_format)
    crawler.crawl()
