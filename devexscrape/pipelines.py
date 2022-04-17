# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import CsvItemExporter
from devexscrape.items import OrgInfoItem, ContractItem


class DevexscrapePipeline:
    def process_item(self, item, spider):
        item_name = type(item).__name__
        self.exporters[item_name].export_item(item)

        return item

    def open_spider(self, spider):
        self.files = {
            OrgInfoItem.__name__: open("Organization_info.csv", "w+b"),
            ContractItem.__name__: open("Contract_info.csv", "w+b")
        }

        self.exporters = dict([(name, CsvItemExporter(fileobj))
                              for name, fileobj in self.files.items()])
        [e.start_exporting() for e in self.exporters.values()]

    def close_spider(self, spider):
        [exporter.finish_exporting() for exporter in self.exporters.values()]
        [file.close() for file in self.files.values()]
        