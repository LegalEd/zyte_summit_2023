# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Summit2023Pipeline:
    def process_item(self, item, spider):
        if "image_id" not in item:
            item["image_id"] = None
        return item
