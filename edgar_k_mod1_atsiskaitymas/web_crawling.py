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
        extracted = [
            {
                "name": product.xpath(
                    ".//div[contains(@class, 'product-title')]//a/text()"
                )[0].split(),
                "price1": product.xpath(
                    ".//div[contains(@class, 'price-container')]//div[contains \
                        (@class, 'price-tag')]//div[contains \
                            @class, 'price-mid-section')]//span/span/text()"
                )[0]
                .strip()
                .replace("\xa0", ""),
                "price2": product.xpath(
                    ".//div[contains(@class, 'price-container')]//div[contains \
                        (@class, 'price-tag')]//div[contains \
                            (@class, 'price-mid-section')]//span/sup/text()"
                ),
            }
            for product in titles
        ]

        # Combine price1 and price2
        for item in extracted:
            if item["price1"] and item["price2"]:
                full_price = item["price1"] + item["price2"][0]
                item[
                    "full_price"
                ] = full_price  # Here we add the combined/full proce to the dict

        for item in extracted:
            if "full_price" in item:
                print(
                    f"Product Name: {' '.join(item['name'])}, \
                        Full Price: {item['full_price']}"
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
