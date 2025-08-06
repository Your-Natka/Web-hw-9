BOT_NAME = "quotes_scraper"
SPIDER_MODULES = ["quotes_scraper.spiders"]
NEWSPIDER_MODULE = "quotes_scraper.spiders"

ROBOTSTXT_OBEY = True

FEEDS = {
    'quotes.json': {'format': 'json', 'overwrite': True},
    'authors.json': {'format': 'json', 'overwrite': True},
}