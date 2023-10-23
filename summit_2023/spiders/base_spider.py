from abc import ABCMeta, abstractmethod
import scrapy


class BasicBaseSpider(scrapy.Spider, metaclass=ABCMeta):
    name = None  # spider name
    allowed_domains = ["domains to be allowed"]
    start_urls = ("urls to visit",)
    next_page_xpath_text = ".//a[@class='page-next']/@href"
    next_page_css_text = ""
    listing_urls_xpath_text = ""
    listing_urls_css_text = ""

    def start_requests(self):
        """overriding default request module to create separate session (cookies) for each start urls"""
        for i, url in enumerate(self.start_urls):
            yield scrapy.Request(url=url, callback=self.parse, meta={"cookiejar": i})

    def build_page_request(self, response, url, callback, meta=None, cb_kwargs=None):
        meta = meta if meta else self.build_meta(response)
        return scrapy.Request(url=response.urljoin(url), callback=callback, meta=meta, cb_kwargs=cb_kwargs)

    def build_meta(self, response):
        return {"cookiejar": response.meta.get("cookiejar")}

    def visit_next_page(self, response, xpath_text="", css_text=""):
        if xpath_text:
            next_page = response.xpath(xpath_text).extract_first()
        elif css_text:
            next_page = response.css(css_text).extract_first()
        else:
            return None
        next_page_request = None
        if next_page:
            next_page_request = self.build_page_request(response, next_page, self.parse)
        return next_page_request

    def get_urls(self, response):
        if self.listing_urls_xpath_text:
            listing_urls = response.xpath(self.listing_urls_xpath_text).extract()
        elif self.listing_urls_css_text:
            listing_urls = response.css(self.listing_urls_css_text).extract()
        else:
            listing_urls = []
        return listing_urls

    def parse(self, response, **kwargs):
        """this method will visit listing url from search result page"""
        listing_urls = self.get_urls(response)
        for listing_url in listing_urls:
            if not listing_url:
                continue
            yield self.build_page_request(response, listing_url, self.get_data)
        if self.next_page_css_text:
            yield self.visit_next_page(response, css_text=self.next_page_css_text)
        elif self.next_page_xpath_text:
            yield self.visit_next_page(response, xpath_text=self.next_page_xpath_text)

    @abstractmethod
    def get_data(self, response):
        """override this method"""
