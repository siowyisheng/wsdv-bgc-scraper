import scrapy
# scrapy crawl wsdvbgc -o wsdvbgc.csv
# scrapy crawl wsdvbgc -s JOBDIR=crawls/wsdvbgc-1 -o wsdvbgc.csv


class WsdvbgcSpider(scrapy.Spider):
    name = "wsdvbgc"
    url = 'http://play.boardgamecore.net/wsdv/{}'
    start_urls = [WsdvbgcSpider.url.format(n) for n in range(54000)]

    def parse(self, response):
        # follow links to entry pages
        for href in response.xpath('//div[@class="exh-table-col exh-table-col--name"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_exhibitor_entry)  # this is used if the href is a partial href
            # yield scrapy.Request(href,
            #                      callback=self.parse_exhibitor_entry)

        # # follow pagination links
        # next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        # if next_page is not None:
        #     # next_page = response.urljoin(next_page)  #this is used if the href is a partial href
        #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_exhibitor_entry(self, response):
        def extract_with_xpath(query):
            if (response.xpath(query).extract_first() != None):
                return response.xpath(query).extract_first().strip()
            else:
                return None

        # def extract_all_with_xpath(delimiter, query):
        #     my_list = []
        #     for item in response.xpath(query).extract():
        #         if (item != None):
        #             my_list.append(item.strip())
        #     return delimiter.join(my_list)

        yield {
            'exhibitor_name': extract_with_xpath('//h1[@itemprop="name"]/text()'),
            'email': extract_with_xpath('//a[@itemprop="email"]/@href')
        }
