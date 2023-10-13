import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup


async def fetch_page(session, page_number):
    url = f"https://umico.az/categories/16-noutbuklar?page={page_number}&q%5Bs%5D=discount%20desc"
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            print(f"Failed to retrieve the webpage. Status code:",
                  response.status)
            return None


async def scrape_page(page_content,
                      discount_percentages,
                      discounted_prices,
                      real_prices,
                      monthly_payments,
                      loan_durations,
                      product_titles,
                      product_hrefs):
    if page_content is None:
        return

    soup = BeautifulSoup(page_content, 'html.parser')
    product_items = soup.find_all('div',
                                  class_='MPProductItem')
    for item in product_items:
        discount_percentage = item.find('div',
                                        class_='MPProductItem-Discount')
        if discount_percentage:
            discount_percentage = discount_percentage.text.strip().replace('%', '').replace('-', '')
        else:
            discount_percentage = '0'
        discounted_price = item.find('span',
                                     class_='MPPrice-RetailPrice')
        if discounted_price:
            discounted_price = discounted_price.text.strip().replace('₼', '').replace(' ', '')
        else:
            discounted_price = '0'
        real_price = item.find('span',
                               class_='MPPrice-OldPrice')
        if real_price:
            real_price = real_price.text.strip().replace('₼', '').replace(' ', '')
        else:
            real_price = '0'
        loan_condition_element = item.find('div',
                                           class_='MPInstallment')
        if loan_condition_element:
            loan_condition = loan_condition_element.text.strip()
            monthly_payment, loan_duration = loan_condition.split(' ₼ x ')
            loan_duration = loan_duration.replace(' ay', '')
        else:
            monthly_payment = '0'
            loan_duration = '0'
        product_title = item.find('span', class_='MPTitle')
        if product_title:
            product_title = product_title.text.strip()
        product_href = item.find('a', href=True)['href']

        discount_percentages.append(float(discount_percentage))
        discounted_prices.append(float(discounted_price))
        real_prices.append(float(real_price))
        monthly_payments.append(float(monthly_payment))
        loan_durations.append(int(loan_duration))
        product_titles.append(product_title)
        product_hrefs.append(f"umico.az{product_href}")


async def main():
    discount_percentages = []
    discounted_prices = []
    real_prices = []
    monthly_payments = []
    loan_durations = []
    product_titles = []
    product_hrefs = []

    tasks = []

    async with aiohttp.ClientSession() as session:
        for page_number in range(1, 110):
            task = asyncio.create_task(fetch_page(session, page_number))
            tasks.append(task)

        page_contents = await asyncio.gather(*tasks)

        for page_content in page_contents:
            await scrape_page(page_content,
                              discount_percentages,
                              discounted_prices,
                              real_prices,
                              monthly_payments,
                              loan_durations,
                              product_titles,
                              product_hrefs)

    data = {
        'product_name': product_titles,
        'discount_percentage': discount_percentages,
        'discounted_price': discounted_prices,
        'real_price': real_prices,
        'monthly_payment': monthly_payments,
        'loan_duration': loan_durations,
        'product_link': product_hrefs
    }
    df = pd.DataFrame(data)
    print(df)
    df.to_excel('df.xlsx', index=False)


if __name__ == '__main__':
    asyncio.run(main())
