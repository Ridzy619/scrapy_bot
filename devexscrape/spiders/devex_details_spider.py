from time import sleep
import scrapy
from math import ceil
import json

from devexscrape.items import OrgInfoItem, ContractItem

DEFAULT_REQUEST_HEADERS = {
    "Referer": "https://google.com/",
    "Accept": "application/xhtml+xml,application/xml",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7",
    "Dnt": "1",
    "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
}


class DevexDetailsSpider(scrapy.Spider):
    name = "devex_details"
    size = 10
    base = "https://www.devex.com/organizations/"

    def start_requests(self):
        start_url = "https://www.devex.com/api/public/search/companies?page[number]=1&page[size]=1"
        yield scrapy.Request(start_url, callback=self.parse)

    def parse(self, response):
        response_json = json.loads(response.text)
        self.total = int(response_json["total"])
        urls = (f'https://www.devex.com/api/public/search/companies?page[size]={self.size}&page[number]={n}' for n in range(
            1, ceil(self.total/self.size)+1))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_urls, headers=DEFAULT_REQUEST_HEADERS)

    def parse_urls(self, response):
        json_data = json.loads(response.text)["data"]

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

    def parse_detail_page(self, response, **cb_kwargs):
        founded = response.xpath(
            '//ul[@class="org-info list-unstyled"]/li[span="Founded"]/strong/text()').get()
        dev_budget = response.xpath(
            '//ul[@class="org-info list-unstyled"]/li[span="Development Budget"]/strong/text()').get()
        headquarters = response.xpath(
            '//ul[@class="org-info list-unstyled"]/li[span="Headquarters"]/strong/a/text()').get()
        website_url = response.xpath(
            '//small[@class="organization-website"]/a/@href').get()
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
                '//h2[text()="Sectors"]//following-sibling::ul/li/span/text()').getall())
            funders = ",".join(org_snapshot.xpath(
                '//h2[text()="Funders"]//following-sibling::ul/li/span/text()').getall())
            countries = ",".join(org_snapshot.xpath(
                '//h2[text()="Countries"]//following-sibling::ul/li/span/text()').getall())
            skills = ",".join(org_snapshot.xpath(
                '//h2[text()="Skills"]//following-sibling::ul/li/span/text()').getall())
            cb_kwargs.update({
                "sectors": sectors,
                "funders": funders,
                "countries": countries,
                "skills": skills
            })

        yield OrgInfoItem(**cb_kwargs)

        contract_names = response.xpath(
            '//div[@class="row margin-top-medium org-awards"]/div/div/h4/a/text()').getall()
        contract_fundiers = response.xpath(
            '//div[@class="row margin-top-medium org-awards"]/div/div/div/em/text()').getall()
        for contract_name, contract_fundier in zip(contract_names, contract_fundiers):
            yield ContractItem({"company_name": cb_kwargs["name"],
                                "contract_name": contract_name,
                                "contract_fundier": contract_fundier})
