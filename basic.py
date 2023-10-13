import bs4
import pandas as pd
import requests

discount_percentages = []
discounted_prices = []
real_prices = []
monthly_payments = []
loan_durations = []
product_titles = []
product_hrefs = []
for page_number in range(1, 110):
    page = f"https://umico.az/categories/16-noutbuklar?page={page_number}&q%5Bs%5D=discount%20desc"
    response = requests.get(page)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        product_items = soup.find_all('div', class_='MPProductItem')
        for item in product_items:
            discount_percentage = item.find('div', class_='MPProductItem-Discount').text.strip().replace('%','').replace('-', '')
            discounted_price = item.find('span', class_='MPPrice-RetailPrice').text.strip().replace('₼', '').replace(' ', '')
            real_price = item.find('span', class_='MPPrice-OldPrice').text.strip().replace('₼', '').replace(' ', '')
            loan_condition_element = item.find('div', class_='MPInstallment')
            if loan_condition_element:
                loan_condition = loan_condition_element.text.strip()
                monthly_payment, loan_duration = loan_condition.split(' ₼ x ')
                loan_duration = loan_duration.replace(' ay', '')
            else:
                monthly_payment = '0'
                loan_duration = '0'
            product_title = item.find('span', class_='MPTitle').text.strip()
            product_href = item.find('a', href=True)['href']
            discount_percentages.append(float(discount_percentage))
            discounted_prices.append(float(discounted_price))
            real_prices.append(float(real_price))
            monthly_payments.append(float(monthly_payment))
            loan_durations.append(int(loan_duration))
            product_titles.append(product_title)
            product_hrefs.append(f"umico.az{product_href}")
    else:
        print(f"Failed to retrieve the webpage. Status code:", response.status_code)
data = {
    'Discount_Percentage': discount_percentages,
    'Discounted_Price': discounted_prices,
    'Real_Price': real_prices,
    'Monthly_Payment': monthly_payments,
    'Loan_Duration': loan_durations,
    'Product_Title': product_titles,
    'Product_Href': product_hrefs
}
df = pd.DataFrame(data)
print(df)
df.to_excel('df3.xlsx', index=False)
