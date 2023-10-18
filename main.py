import smtplib
import time
import os
import asyncio
import aiohttp
import pandas as pd
import base64
from bs4 import BeautifulSoup
from datetime import datetime
from email.mime.text import MIMEText
import io

async def fetch_page(session, page_number):
    max_retries = 3  # Define the maximum number of retries
    retries = 0
    while retries < max_retries:
        try:
            url = f"https://umico.az/categories/16-noutbuklar?page={page_number}&q%5Bs%5D=discount%20desc"
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Failed to retrieve the webpage. Status code: {response.status}")
                    return None
        except aiohttp.client_exceptions.ServerDisconnectedError:
            retries += 1
            print("Retrying request...")
        await asyncio.sleep(5)  # sleep for 5 seconds

    return None  


async def scrape_page(page_content, discount_percentages, discounted_prices, real_prices, monthly_payments, loan_durations, product_titles, product_hrefs):
    if page_content is None:
        return

    soup = BeautifulSoup(page_content, 'html.parser')
    product_items = soup.find_all('div', class_='MPProductItem')
    
    for item in product_items:
        discount_percentage = item.find('div', class_='MPProductItem-Discount')
        if discount_percentage:
            discount_percentage = discount_percentage.text.strip().replace('%', '').replace('-', '')
        else:
            discount_percentage = '0'
        
        discounted_price = item.find('span', class_='MPPrice-RetailPrice')
        if discounted_price:
            discounted_price = discounted_price.text.strip().replace('₼', '').replace(' ', '')
        else:   
            discounted_price = '0'
        
        real_price = item.find('span', class_='MPPrice-OldPrice')
        if real_price:
            real_price = real_price.text.strip().replace('₼', '').replace(' ', '')
        else:
            real_price = '0'
        
        loan_condition_element = item.find('div', class_='MPInstallment')
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

df = None

async def main():
    discount_percentages = []
    discounted_prices = []
    real_prices = []
    monthly_payments = []
    loan_durations = []
    product_titles = []
    product_hrefs = []

    tasks = []
   
    headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7,az;q=0.6',
            'Dnt': '1',
            'Origin': 'https://umico.az',
            'Referer': 'https://umico.az/',
            'Sec-Ch-Ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }
    async with aiohttp.ClientSession(trust_env=True,headers=headers) as session:
        for page_number in range(1, 5):
            task = asyncio.create_task(fetch_page(session, page_number))
            tasks.append(task)

        page_contents = await asyncio.gather(*tasks)

        for page_content in page_contents:
            await scrape_page(page_content, discount_percentages, discounted_prices, real_prices, monthly_payments, loan_durations, product_titles, product_hrefs)

    data = {
        'product_name': product_titles,
        'discount_percentage': discount_percentages,
        'discounted_price': discounted_prices,
        'real_price': real_prices,
        'monthly_payment': monthly_payments,
        'loan_duration': loan_durations,
        'product_link': product_hrefs
    }
    
    global df
    df = pd.DataFrame(data)
    print(df)
    table_html = df.to_html(index=False)
    # Create an email message
    MY_EMAIL = os.environ["EMAIL_USERNAME"]
    MY_PASSWORD = os.environ["EMAIL_PASSWORD"]
    TO_EMAIL = os.environ["EMAIL_TO"]
    EMAIL_PORT = os.environ["EMAIL_PORT"]
    EMAIL_SERVER = os.environ["EMAIL_SERVER"]

    current_date = datetime.now().strftime("%d.%m.%Y")

    subject = "🔥🔥🔥Discounts "  + current_date + "🔥🔥🔥"


    recipient_emails = TO_EMAIL.split(',')

    for recipient_email in recipient_emails:
        try:
            connection = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            msg = MIMEText(f'<html><body>{table_html}</body></html>', 'html', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = MY_EMAIL
            msg['To'] = recipient_email
            msg_str = msg.as_string()
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=recipient_email, msg=msg_str)
            connection.quit()
            print(f"Email sent successfully to {recipient_email}.")
        except Exception as e:
            print(f"An error occurred while sending the email to {recipient_email}: {str(e)}")


if __name__ == '__main__':
    asyncio.run(main())