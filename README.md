---

# Web Scraping and Email Notification Script

This Python script is designed to scrape data from a website and send an email with the scraped data as an HTML table. It is specifically tailored for scraping product discount information from [umico.az](https://umico.az/categories/16-noutbuklar) and notifying recipients via email.

## Features

- Asynchronously scrapes product data from multiple pages on the website.
- Constructs a Pandas DataFrame from the scraped data.
- Sends an email containing the data as an HTML table to specified recipients.
- Schedules the scraping job to run daily at a specific time.

## Prerequisites

Before using this script, make sure you have the following dependencies installed:

- Python 3.x
- Required Python packages (install using `pip`):
    - aiohttp==3.8.5
    - beautifulsoup4==4.12.2
    - pandas==2.1.1
    - schedule==1.2.1
    - requests==2.31.0
    - brotli==1.1.0

You can install these packages by running:

```bash
pip install -r requirements.txt
```

## Configuration

Before running the script, you need to configure several parameters in the script itself:

- `MY_EMAIL`: Your Gmail email address from which the notification emails will be sent.
- `MY_PASSWORD`: Your Gmail account password. Be cautious with this information and consider using an app-specific password.
- `TO_EMAIL`: A comma-separated list of recipient email addresses to whom the notifications will be sent.
- `current_date`: The date format for the subject line of the email.
- `schedule.every().day.at("09:00").do(job)`: Schedule the scraping job to run at a specific time. You can adjust the time according to your needs.

## Running the Script

You can run the script using the following command:

```bash
python main.py
```

The script will scrape the data and send notifications to the specified email addresses at the scheduled time.

## Customization

You can customize this script for different websites and data types by modifying the following parts:

- The URL in `fetch_page(session, page_number)` to match the website you want to scrape.
- The scraping logic in `scrape_page(page_content, ...)` to extract the relevant data.
- The DataFrame creation to match the structure of your scraped data.

## Important Notes

- Be cautious with your Gmail email and password. Use app-specific passwords if possible.
- Consider using a dedicated Gmail account for sending notifications.
- Make sure to comply with website terms of service and scraping policies.
---
1.  Deployment to Heroku Instructions (Heroku Git)
2.  Sign up for a free heroku account if you havent already done so
3.  Create app ie. myapp #name of app
4.  Type heroku login --> This will take you to a web based login page
5.  cd to your directory on your local drive
6.  Type 'git init'
7.  Type 'heroku git:remote -a umico'
8.  Type 'git add .'
9.  Type ' git commit -am "version 1"'
10. Type 'git push heroku master'
11. Now you need to allocate a dyno to do the work. Type 'heroku ps:scale worker=1'
12. If you want to check the logs to make sure its working type 'heroku logs --tail'
13. Now your code will continue to run until you stop the dyno. To stop it scale it down using the command 'heroku ps:scale worker=0'