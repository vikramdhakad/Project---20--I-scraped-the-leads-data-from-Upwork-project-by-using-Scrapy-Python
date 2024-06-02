import scrapy
from time import sleep

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.bbb.org"]
    start_urls = ["https://www.bbb.org/search?find_country=USA&find_text=search&page=1"]

    def parse(self, response):
        for name in response.xpath("//a[@class='text-blue-medium css-1jw2l11 eou9tt70']"):
            urls = name.xpath("@href").get()
            yield response.follow(url=urls,callback=self.data_parser)
            sleep(2)

        for page in range(1,16):
            nxt = response.xpath("//a[@rel='next']/@href").get()
            yield response.follow(url=nxt,callback=self.parse)

    def data_parser(self, response):
        yield{
            "Company Name": response.xpath("//span[@class='bds-h2 font-normal text-black']/text()").get(),
            "Address": response.xpath("//div[@class='dtm-address stack']/dd/text()").get(),
            "Location URL": response.xpath("//a[@class='dtm-url']/@href").get(),
            "Phone": response.xpath("//a[@class='dtm-phone']/text()").get()
        }