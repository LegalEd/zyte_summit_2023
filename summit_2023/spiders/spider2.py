from ..loaders import ZquadLoader
from .base_spider import BasicBaseSpider
import scrapy
from word2number import w2n


class Spider2Spider(BasicBaseSpider):
    name = "spider2"
    allowed_domains = ["run.app"]
    start_urls = ("https://ducqocgbcrqftlrn-5umjfyjn4a-ew.a.run.app/items",)
    listing_urls_css_text = ".gtco-practice-area-item .gtco-copy a::attr(href)"
    next_page_css_text = "a:contains('→')::attr(href)"

    def get_data(self, response):
        # recommended_links = response.css(".team-item a")
        # yield from response.follow_all(recommended_links, self.get_data)
        item = ZquadLoader(response=response)
        item.add_css("item_id", "#uuid *::text")
        item.add_css("text", "h2.heading-colored::text")
        stock = response.css(".stock *::text").extract_first()
        stock = w2n.word_to_num(stock)
        item.add_value("stock", stock)
        yield item.load_item()
