# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OrgInfoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    name = scrapy.Field()
    logo_url = scrapy.Field()
    description = scrapy.Field()
    organization_types = scrapy.Field()
    staff = scrapy.Field()
    founded = scrapy.Field()
    dev_budget = scrapy.Field()
    headquarters = scrapy.Field()
    website_url = scrapy.Field()
    sectors = scrapy.Field()
    funders = scrapy.Field()
    countries = scrapy.Field()
    skills = scrapy.Field()
    
class ContractItem(scrapy.Item):
    company_name = scrapy.Field()
    contract_name = scrapy.Field()
    contract_fundier = scrapy.Field()
