# DEVEX SCRAPY_BOT

## How to Run

After cloning the project, cd into **scrapy_bot** folder and do the following
- `python -m venv env`
- `source activate env`
- `pip install -r requirements.txt`
- `scrapy crawl devex_details`

## Brief Description

The goal of the project is to extract the following details into separate csv files from devex.com as listed below:

- Organization Information
    - Company Name
    - Company Logo
    - Company Description 
    - Organization Type
    - Staff
    - Development Budget
    - Headquarters
    - Founded
    - website link 

- Sectors Information
    - Funded, comma separated in one column
    - Countries, comma separated in one column 
    - Skills, comma separated in one column 

## Challenges Faced and Solutions Attempted
I faced two major challenges and in attempt to solve them, I faced some others. The two challenges are:

- Captcha preventing scraping by returning 403 error.
    - This challenge was solved by passing some headers which let the scraper bot mimic a regular browser
-  The bug detailed in this [GitHub issue](https://github.com/pyca/pyopenssl/issues/873) which is perculiar to Mac OS.
    - I attempted to solve this by launching a Linux EC2 instance on AWS but soon faced another issue:
        - Due to the instance using a public IP (so I believe), the website was quick to blacklist the IP address of the instance - thus preventing it from scraping much.Error 403 is returned after few scrapes.
            - I attempted to solve this by introducing a 403 error callback which attempts to get the catched version of the webpages from [Google Cache](http://webcache.googleusercontent.com/search?q=cache:) but this was only modestly successful as it was getting blocked by Google intermittently. Also, rather weirdly, the component of the application that writes the Contract information was not getting any values.
    - As the first set of solutions failed, I resorted to finding a Windows PC which I utilized to run the project. I faced no issues running it on Windows. I presume it would also work fine on Linux OS that is not cloud hosted or with proxy rotation.

