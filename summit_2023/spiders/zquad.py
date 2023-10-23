from ..loaders import ZquadLoader
from .base_spider import BasicBaseSpider


class ZquadSpider(BasicBaseSpider):
    name = "zquad"
    allowed_domains = ["run.app"]
    start_urls = ("https://web-5umjfyjn4a-ew.a.run.app/clickhere",)
    listing_urls_css_text = "#gtco-practice-areas .gtco-practice-area-item .gtco-copy a::attr(href)"
    next_page_css_text = "a:contains('Next Page >')::attr(href)"

    def get_data(self, response):
        item = ZquadLoader(response=response)
        item.add_css("item_id", "#item-data p > span#uuid *::text")
        item.add_css("name", "#item-data h2 *::text")
        item.add_css("image_id", "#item-data .img-shadow img::attr(src)", re=r"gen/(.*)\.jpg")
        item.add_css("rating", "#item-data p:contains('Rating') span *::text")
        yield item.load_item()
