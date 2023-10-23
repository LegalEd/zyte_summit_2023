import re

from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Identity

from .items import ZquadItem


def filter_empty(s):
    return s or None


def remove_white_space(s):
    return re.sub(r"\s+", " ", s)


def string_strip(s):
    return s.strip()


class ZquadLoader(ItemLoader):
    default_item_class = ZquadItem
    default_input_processor = MapCompose(remove_white_space, string_strip, filter_empty)
    default_output_processor = Join()
