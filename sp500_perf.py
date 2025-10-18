import scrapy


class Sp500PerfSpider(scrapy.Spider):
    name = "sp500_perf"
    allowed_domains = ["slickcharts.com"]
    start_urls = ["https://slickcharts.com/sp500/performance"]

    def parse(self, response):
        rows = response.xpath('//table[.//th[contains(normalize-space(.), "YTD")]]/tbody/tr')
        for r in rows:
            number = r.xpath('./td[1]/text()').get()
            company = r.xpath('./td[2]//a/text() | ./td[2]/text()').get()
            symbol = r.xpath('./td[3]//a/text() | ./td[3]/text()').get()
            ytd_return = r.xpath('./td[4]//text()').get()

            if number and company and symbol and ytd_return:
                yield {
                    "number": number,
                    "company": company,
                    "symbol": symbol,
                    "ytd_return": ytd_return
                }