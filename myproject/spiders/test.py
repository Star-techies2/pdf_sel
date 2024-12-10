from pydispatch import dispatcher
from urllib.parse import urljoin
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import re
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import signals

def create_my_spider(start_url):
    class MySpider(scrapy.Spider):
        name = 'muspider'
 
        def __init__(self, start_url, *args, **kwargs):
            super(MySpider, self).__init__(*args, **kwargs)
            self.start_urls = [start_url]
            self.results = []
 
        custom_settings = {
            'DOWNLOAD_DELAY': 2,  # 2 seconds delay
            'RETRY_ENABLED': True,
            'RETRY_TIMES': 5,  # Retry 5 times
            'DOWNLOAD_TIMEOUT': 15,  # 15 seconds timeout
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
 
        def parse(self, response):
            self.log(f"Parsing response from: {response.url}")
            title = f"Title: {response.url}"
            self.results.append(title)
            elements = response.xpath('//h1 | //h2 | //h3 | //h4 | //h5 | //h6 | //p | //a[not(ancestor::script) and not(ancestor::style)] | //li[a/@href] | //tr[a/@href]')
            content_found = False
            for element in elements:
                if element.root.tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    heading_text = " ".join(element.xpath('.//text()').getall()).strip()
                    self.results.append(heading_text)
                    content_found = True
                elif element.root.tag == 'p':
                    extract_text = " ".join(element.xpath('.//text()').getall()).strip()
                    strip_text = " ".join(extract_text.split())
                    self.results.append(strip_text)
                    content_found = True
                elif element.root.tag == 'a':
                    link_text = element.xpath('.//text()').get()
                    if link_text:
                        link_text = link_text.strip()
                        link_href = element.xpath('.//@href').get()
                        if link_href and link_href != 'javascript:void(0)':
                            full_link = urljoin(response.url, link_href)
                            following_text = element.xpath('following-sibling::text()[1]').get()
                            if following_text:
                                following_text = following_text.strip()
                                self.results.append(f"{link_text}: {full_link} - {following_text}")
                            else:
                                self.results.append(f"{link_text}: {full_link}")
                            content_found = True
                elif element.root.tag in ['li', 'tr']:
                    link_text = element.xpath('.//a/text()').get()
                    link_href = element.xpath('.//a/@href').get()
                    if link_href and link_href != 'javascript:void(0)':
                        full_link = urljoin(response.url, link_href)
                        combined_text = f"{element.xpath('string(.)').get().strip()}: {full_link}"
                        self.results.append(combined_text)
                        content_found = True
            if not content_found:
                self.results.append("No content found")
 
        def errback(self, failure):
            self.log(f"Request failed: {failure.request.url}")
            self.results.append(f"Title: {failure.request.url}")
            self.results.append("No content found")
 
    return MySpider
 
 
start_url = 'https://providers.bcbsla.com/resources/professional-provider-office-manual-24'
print("Starting the crawler...")
process = CrawlerProcess()
results = []
def spider_closed(spider):
    global results
    results = spider.results
    file_name = 'bcbsla_webscraping_links.txt'
    with open(file_name, 'w', encoding='utf-8') as f:
        for item in results:
            f.write(f"{item}\n")
 
   
 
MySpider = create_my_spider(start_url)
dispatcher.connect(spider_closed, signal=signals.spider_closed)
process.crawl(MySpider, start_url=start_url)
process.start()