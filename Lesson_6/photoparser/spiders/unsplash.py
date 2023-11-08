import scrapy
from scrapy.http import HtmlResponse
from photoparser.items import PhotoparserItem

from scrapy.loader import ItemLoader


class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/s/photos/rifle"]
    # start_urls = ["https://unsplash.com/s/photos/gun"]
    

    def parse(self, response: HtmlResponse):
        
        links = response.xpath('//a[@itemprop="contentUrl"]')

        for link in links:
            yield response.follow(link, callback=self.parse_unsplash)
        
    def parse_unsplash(self, response:HtmlResponse):
      
        # name = response.xpath("//h1/text()").get()
        # photos = response.xpath('//div[@class="MorZF"]')
        # url = response.url
        # yield(PhotoparserItem(name=name, url=url, photos=photos))
        photos = response.xpath("//button[@class='ju2Kp jpBZ0 m5u7p aZ5iK']//div[@class='MorZF']//@src | "
                                    "//div[@class='zmDAx']//div[@class='MorZF']/img/@src")
        print ("Photos ", photos)

        loader = ItemLoader(item=PhotoparserItem(), response=response)
        loader.add_xpath ('name', "//h1/text()")
        loader.add_value ('url', response.url)
        loader.add_xpath ('photos', "//button[@class='ju2Kp jpBZ0 m5u7p aZ5iK']//div[@class='MorZF']//@src")
                                    # "//div[@class='zmDAx']//div[@class='MorZF']/img/@src")
        loader.add_xpath('category','//a[@class="IMl2x Ha8Q_"]/text()')
                                    
        # loader.add_xpath ('photos', "//div[@class='MorZF']//@src")
        yield loader.load_item()

    
        


