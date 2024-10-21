import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
import time

class DebatedataSpider(scrapy.Spider):
    name = 'debatedata_spider'
    start_urls = ['https://debatedata.io/tournaments']  

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response)
        # driver = response.meta['driver']
        # last_height = driver.execute_script("return document.body.scrollHeight")  # Chiều cao ban đầu của trang

        # while True:
        #     # Cuộn xuống dưới cùng của trang
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(2)  # Chờ để dữ liệu tải xong

        #     # Tính chiều cao mới của trang sau khi cuộn
        #     new_height = driver.execute_script("return document.body.scrollHeight")

        #     # Kiểm tra xem chiều cao đã thay đổi chưa
        #     if new_height == last_height:
        #         break  # Dừng lại nếu không còn dữ liệu mới
        #     last_height = new_height  # Cập nhật chiều cao

        # # Lấy dữ liệu sau khi cuộn
        # page_source = driver.page_source
        # response = scrapy.Selector(text=page_source)

        # Lấy dữ liệu cụ thể (thay đổi selector theo trang web của bạn)
        items = response.xpath('html').getall()
        print(items)
        for item in items:
            print(item)
        print(99999999)
        print(len(items))