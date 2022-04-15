from time import sleep
import scrapy
from math import ceil

from devexscrape.items import OrgInfoItem

DEFAULT_REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
class DevexDetailsSpider(scrapy.Spider):
    name = "devex_details"
    size = 100
    total = 20
    base = "https://www.devex.com/organizations/"

    def start_requests(self):
        start_url = "https://www.devex.com/api/public/search/companies?page[number]=1&page[size]=1"
        scrapy.Request(start_url, callback=self.parse, headers=DEFAULT_REQUEST_HEADERS)
        sleep(2)
        urls = (f'https://www.devex.com/api/public/search/companies?page[size]={self.size}&page[number]={n}' for n in range(
            1, ceil(self.total/self.size)+1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_urls, headers=DEFAULT_REQUEST_HEADERS)

    def parse(self, response):
        self.total = 20 or int(response.json()["total"])
        print(self.total)

    def parse_urls(self, response):
        json_data = response.json()["data"]

        for org in json_data:
            url = self.base + org["slug_and_id"]
            name = org["name"]
            logo_url = org["logo_url"]
            description = org["description"]
            organization_types = org["organization_types"]
            staff = org["organization_size"]
            kwargs = {
                "name": name,
                "logo_url": logo_url,
                "description": description,
                "organization_types": organization_types,
                "staff": staff,
            }
            yield scrapy.Request(url, callback=self.parse_detail_page, cb_kwargs=kwargs, headers=DEFAULT_REQUEST_HEADERS)

    def parse_detail_page(self, response, cb_kwargs):
        founded = response.xpath(
            '//ul[@class="org-info list-unstyled"]/li[span="Founded"]/strong/text()').get()
        dev_budget = response.xpath(
            '//ul[@class="org-info list-unstyled"]/li[span="Development Budget"]/strong/text()').get()
        headquarters = response.xpath(
            '//ul[@class="org-info list-unstyled"]/li[span="Headquarters"]/strong/a/text()').get()
        website_url = response.xpath(
            '//small[@class="organization-website"]/a/@href')
        cb_kwargs.update({
            "founded": founded,
            "dev_budget": dev_budget,
            "headquarters": headquarters,
            "website_url": website_url,
        })
        org_snapshot = response.xpath(
            '//div[@class="org-snapshot clearfix relative"]/div')
        if org_snapshot:
            org_snapshot = org_snapshot[0]
            sectors = ",".join(org_snapshot.xpath(
                '//h2[text()="Sectors"]//following-sibling::ul/li/span/text()').get_all())
            funders = ",".join(org_snapshot.xpath(
                '//h2[text()="Funders"]//following-sibling::ul/li/span/text()').get_all())
            countries = ",".join(org_snapshot.xpath(
                '//h2[text()="Countries"]//following-sibling::ul/li/span/text()').get_all())
            skills = ",".join(org_snapshot.xpath(
                '//h2[text()="Skills"]//following-sibling::ul/li/span/text()').get_all())
            cb_kwargs.update({
                "sectors": sectors,
                "funders": funders,
                "countries": countries,
                "skills": skills
            })

        yield OrgInfoItem(**cb_kwargs)

#  Use the Company Name as the unique identifier
# - Contract Name,
# - Contract Fundier, e.g. Bill and Melinda Gates Foundation


# Company Name
# - Company Logo
# - Company Description
# - Organization Type
# - Staff
# - Development Budget
# - Headquarters
# - Founded
# - website link

# Sectors, comma separated in one column
# Funded, comma separated in one column
# Countries, comma separated in one column
# Skills, comma separated in one column
