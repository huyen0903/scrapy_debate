import scrapy
from ..items import DebateCrawlerItem
import datetime

class DebateSpiderSpider(scrapy.Spider):
    name = "debate_spider"
    allowed_domains = ["idebate.net"]
    start_urls = ["https://idebate.net/resources/debatabase"]
    url_page2 = ""

    def __init__(self, start_page=1, end_page=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page = int(start_page)
        self.end_page = int(end_page) if end_page is not None else None
        self.current_page = self.start_page

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse1)

    def parse1(self, response):
        # Lấy danh sách các liên kết chi tiết
        detail_links = response.xpath(
            "//div[@class='card-tools card-tools--denim-blue']/a/@href").getall()
        for link in detail_links:
            yield response.follow(link, self.parse_card)

    def parse_card(self, response):
        last_page_ar = response.xpath("//div[@class='pagination']/a").getall()
        last_page = 1
        if (len(last_page_ar) > 2):
            last_page = last_page_ar[-2]
        now_page = response.xpath(
            "//a[@class='pagination__item pagination__item--active']/text()").getall()[0]

        last_page_number = int(''.join(filter(str.isdigit, last_page)))
        now_page_number = int(''.join(filter(str.isdigit, now_page)))

        detail_links = response.xpath(
            "//div[@class='card-horizontal__container']/a/@href").getall()
        for link in detail_links:
            yield response.follow(link, self.parse_detail)

        if last_page_number > now_page_number:
            next_page = f'{self.url_page2}?page={now_page_number+1}'
            yield response.follow(next_page, self.parse_card)

    def parse_detail(self, response):
        item = {
            # 'post_date': response.xpath('//div[@class="blog-post__date"]/text()').get(),
            # 'topic_name': response.xpath('//a[@class="breadcrumbs__item"]/text()').get(),
            # 'motion': response.xpath('//h1[@class="blog-post__title"]/text()').getall(),
            # 'points_for': response.xpath('//div[@id="accordion-3"]/text()').getall(),
            # 'points_against': response.xpath('//div[@id="accordion-5"]/text()').getall(),
            # 'bibliography': response.xpath('//div[@class="bibliography"]/text()').getall(),
            # 'describe': response.xpath('//div[@class="wysiwyg"]/text()').getall(),
            'topic_name': response.xpath('//div[@class="col-12 col-md-7 order-0"]/ul[@class="breadcrumbs"]/li[2]/a/text()').get(),
            'motion': response.xpath('//h1[@class="blog-post__title"]/text()').get(),
            "describe": response.xpath('//div[@class="col-12 col-md-7 order-0"]/div/p/text()').get(),
            'points_for': response.xpath('//div[@id="accordion-3"]/div[@class="accordion__item"]/div[@class="accordion__head"]/h4/text()').getall(),
            'points_against': response.xpath('//div[@id="accordion-5"]/div[@class="accordion__item"]/div[@class="accordion__head"]/h4/text()').getall(),
            'bibliography': response.xpath('//div[@class="bibliography"]/div[@class="bibliography__text"]/p/text()').getall(),
            'post_type': response.xpath('//div[@class="blog-post__type text-regal-blue"]/text()').get(),
            'post_date': response.xpath('//div[@class="blog-post__date"]/text()').get(),
        }

        yield item
