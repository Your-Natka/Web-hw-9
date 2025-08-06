import scrapy
from quotes_scraper.items import QuoteItem, AuthorItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']
    authors_seen = set()

    def parse(self, response):
        for quote in response.css('div.quote'):
            author_name = quote.css('small.author::text').get()

            yield QuoteItem({
                'quote': quote.css('span.text::text').get().strip('“”'),
                'author': author_name,
                'tags': quote.css('div.tags a.tag::text').getall()
            })

            if author_name not in self.authors_seen:
                self.authors_seen.add(author_name)
                author_url = quote.css('a::attr(href)').get()
                yield response.follow(author_url, callback=self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        yield AuthorItem({
            'fullname': response.css('h3.author-title::text').get().strip(),
            'born_date': response.css('span.author-born-date::text').get().strip(),
            'born_location': response.css('span.author-born-location::text').get().strip(),
            'description': response.css('div.author-description::text').get().strip()
        })