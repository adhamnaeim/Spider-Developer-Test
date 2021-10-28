import scrapy
from scrapy import Request
# from scrapy.loader import ItemLoader
# from property import Property
from ..items import TimedtestItem


class LondonrelocationSpider(scrapy.Spider):
    page_number = 1
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):

        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):

        item = TimedtestItem()
        # Write your code here and remove `pass` in the following line
        PropertyBoxes = response.css(".test-box")
        for box in PropertyBoxes:
            PropertyTitle = box.css(".h4-space a::text").extract()
            PropertyURL = box.css(".h4-space a::attr(href)").extract()
            PropertyFullURL = self.name+".com" + PropertyURL[0]
            PropertyPrice = box.css("h5::text").extract()
            PropertyPriceOnly= [int(s) for s in PropertyPrice[0].split() if s.isdigit()]

            item['title'] = PropertyTitle
            item['url'] = PropertyFullURL
            item['price'] = PropertyPriceOnly
            yield item
        next_page = response.css(".pagination li:nth-child(3) a::attr(href)").get()
        if next_page is not None and LondonrelocationSpider.page_number !=2:
            LondonrelocationSpider.page_number = LondonrelocationSpider.page_number +1
            yield response.follow(next_page,callback=self.parse_area_pages)
        # an example for adding a property to the json list:
        # property = ItemLoader(item=Property())
        # property.add_value('title', '2 bedroom flat for rental')
        # property.add_value('price', '1680') # 420 per week
        # property.add_value('url', 'https://londonrelocation.com/properties-to-rent/properties/property-london/534465-2-bed-frognal-hampstead-nw3/')
        # return property.load_item()import scrapy
        # from scrapy import Request
        # from scrapy.loader import ItemLoader
        # from property import Property
        #
        #
        # class LondonrelocationSpider(scrapy.Spider):
        #     name = 'londonrelocation'
        #     allowed_domains = ['londonrelocation.com']
        #     start_urls = ['https://londonrelocation.com/properties-to-rent/']
        #
        #     def parse(self, response):
        #         for start_url in self.start_urls:
        #             yield Request(url=start_url,
        #                           callback=self.parse_area)
        #
        #     def parse_area(self, response):
        #         area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        #         for area_url in area_urls:
        #             yield Request(url=area_url,
        #                           callback=self.parse_area_pages)
        #
        #     def parse_area_pages(self, response):
        #         # Write your code here and remove `pass` in the following line
        #         pass
        #
        #         # an example for adding a property to the json list:
        #         # property = ItemLoader(item=Property())
        #         # property.add_value('title', '2 bedroom flat for rental')
        #         # property.add_value('price', '1680') # 420 per week
        #         # property.add_value('url', 'https://londonrelocation.com/properties-to-rent/properties/property-london/534465-2-bed-frognal-hampstead-nw3/')
        #         # return property.load_item()
