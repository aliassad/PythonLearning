import scrapy


class AuthorsSpider(scrapy.Spider):
    name = 'authors'

    start_urls = [
        'http://quotes.toscrape.com'
    ]

    def parse(self, response):

        for href in response.css('.author + a::attr(href)'):
            yield response.follow(url=href, callback=self.parse_author)

        for href in response.css('li.next a::attr(href)'):
            yield response.follow(url=href, callback=self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()
        yield {
            'title': extract_with_css('h3.author-title::text'),
            'born': extract_with_css('.author-born-date::text'),
            'description': extract_with_css('.author-description::text')
        }
