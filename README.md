---

# Web Scraping with Python and asyncio

## Overview

This Python script demonstrates how to perform web scraping using asyncio, aiohttp, BeautifulSoup, and pandas. It scrapes data from the Umico.az website, specifically the "Noutbuklar" (laptops) category, and extracts information about discounted laptops.

The data extracted includes:

- Discount percentage
- Discounted price
- Real price
- Monthly payment (if available)
- Loan duration (in months, if available)
- Product title
- Product URL (link)

## Dependencies

To run this script, you'll need the following dependencies:

- Python 3.7+
- aiohttp
- BeautifulSoup4 (bs4)
- pandas
- asyncio

You can install these dependencies using pip:

```
pip install aiohttp beautifulsoup4 pandas
```

## How to Run

1. Clone or download this repository to your local machine.

2. Open a terminal or command prompt and navigate to the directory where the script is located.

3. Run the script with the following command:

```
python asynchronous.py
```

4. The script will start scraping data from Umico.az for discounted laptops in the specified category.

5. The extracted data will be saved in an Excel file named "df.xlsx" in the same directory as the script.

## Script Structure

- The `fetch_page` function sends GET requests to the Umico.az website and retrieves the HTML content of a specific page.

- The `scrape_page` function parses the HTML content and extracts the relevant data, including discount percentage, prices, loan conditions, product titles, and URLs. This function is executed asynchronously for each page.

- The `main` function orchestrates the scraping process. It creates multiple tasks to fetch and scrape data from multiple pages concurrently using asyncio.

- Extracted data is stored in lists, and a DataFrame is created using pandas for structured data storage.

- The resulting DataFrame is displayed in the terminal and saved to an Excel file.

## Data Extracted

The script extracts information about discounted laptops, including the discount percentage, discounted price, real price, monthly payment, loan duration, product title, and product URL.

## Disclaimer

Web scraping may be subject to website terms of service and legal regulations. Be sure to review and comply with the terms and policies of the website you are scraping. This script is intended for educational and demonstration purposes.

## License


---
