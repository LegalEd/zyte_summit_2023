from ..loaders import ZquadLoader
from .base_spider import BasicBaseSpider

import json
import scrapy


class Spider2Spider(BasicBaseSpider):
    name = "spider2"
    allowed_domains = ["run.app"]
    start_urls = ("https://web-5umjfyjn4a-ew.a.run.app/clickhere",)
    listing_urls_css_text = ".gtco-practice-area-item .gtco-copy a::attr(href)"
    next_page_css_text = "a:contains('Next Page')::attr(href)"

    def get_data(self, response):
        recommended_links = response.css(".team-item a")
        yield from response.follow_all(recommended_links, self.get_data)
        item = ZquadLoader(response=response)
        item.add_css("item_id", "#uuid *::text")
        item.add_css("name", "h2.heading-colored::text")
        images = response.css(".img-shadow img::attr(src)").re(r"gen/(.*)\.jpg")
        images = [image for image in images if "thumb" not in image]
        if not images:
            images = response.css("script:contains('/gen')::text").re("(?<=/gen/)(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}).jpg")

        if images:
            item.add_value("image_id", images)
        ratings = response.css("#item-data p:contains('Rating') span *::text").extract_first()
        if "NO RATING" in ratings:
            backend_url = response.css("#item-data p:contains('Rating') span::attr(data-price-url)").extract_first()
            yield scrapy.Request(
                url=response.urljoin(backend_url), callback=self.get_rating, cb_kwargs={"item": item.load_item()}
            )
        else:
            item.add_value("rating", ratings)
            yield item.load_item()

    def get_rating(self, response, item):
        item2 = ZquadLoader(response=response)
        item2.add_value(None, item)
        j_dict = json.loads(response.body)
        item2.add_value("rating", j_dict.get("value"))
        yield item2.load_item()
