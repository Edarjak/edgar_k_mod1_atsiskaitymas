# edgar_k_mod1_atsiskaitymas
The source code for the first module of the Python Crash Course project.

# WebCrawling Package

## Overview

The **WebCrawling** package provides a solution for scraping structured data from two popular Lithuanian e-commerce websites:
- [Varle.lt](https://www.varle.lt/ispardavimas/)
- [Camelia.lt](https://camelia.lt/c/prekiu-medis/nereceptiniai-vaistai/persalimui-1288)

It allows users to extract product names, prices, discounts, and images, and save the extracted data in either `.txt` or `.csv` formats.

---

## Features

- **Scraping**: Extract product details, including names, prices, discounts, and images.
- **Multiple Formats**: Save the scraped data as `.txt` or `.csv` files.
- **Image Downloading**: Automatically download product images and store them in an "images" folder.
- **Pagination Support**: The crawler supports scraping multiple pages of products.
- **Custom Time Limit**: Users can set a time limit for the crawling process to avoid overloading the website.

---

## Installation

You can easily install this package via **PyPI**.

```bash
pip install edgar_k_mod1_atsiskaitymas
```

or you can clone the repository and crawl pages from your local machine:

```bash
git clone https://github.com/Edarjak/edgar_k_mod1_atsiskaitymas.git
cd edgar_k_mod1_atsiskaitymas
touch main.py
```

---

## Usage

After installing the package, you can use the `crawl` function to start scraping data. The `crawl` function allows you to specify the following parameters:


| Parameter       | Description                                                                 | Valid Options                           |
|-----------------|-----------------------------------------------------------------------------|-----------------------------------------|
| **time_limit**  | The time limit (in seconds) for the crawler to run.                         | Any positive integer                    |
| **source**      | The website to scrape.                                                      | `"varle"` - Scrape data from varle.lt<br>`"camelia"` - Scrape data from camelia.lt |
| **return_format** | The format in which to save the scraped data.                               | `"txt"` - Save the data in a .txt file<br>`"csv"` - Save the data in a .csv file |


The example of main.py:

```python
from edgar_k_mod1_atsiskaitymas.web_crawling import crawl

# Start scraping data from Varle.lt with a 5-second time limit and save results in CSV format
crawl(5, "varle", "csv")

# Start scraping data from Camelia.lt with a 10-second time limit and save results in TXT format
crawl(10, "camelia", "txt")
```

---

## Limitations:
Package collects images only from cameliavaistine.lt

## Output

After running the script, the extracted data will be saved to files in the root directory of your project. These include:

- `varle_rezultatas.txt` / `varle_rezultatas.csv`: Data scraped from varle.lt.
- `camelia_rezultatas.txt` / `camelia_rezultatas.csv`: Data scraped from camelia.lt.
- `images/`: A directory containing the product images downloaded from the cameliavaistine.lt during scraping.

## Example Data Files

You can view example output files in the [/examples](./examples/) directory of this repository. These files contain sample scraped data and images for camelia.lt.

## PyPI Link

This package is available for installation from PyPI:

```

```