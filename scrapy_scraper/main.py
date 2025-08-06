from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from quotes_scraper.spiders.quotes_spider import QuotesSpider

def run():
    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotesSpider)
    process.start()

if __name__ == "__main__":
    run()