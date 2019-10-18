# -*- coding: utf-8 -*-
import scrapy
import re


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['www.boutique1.com']
    start_urls = ['https://www.boutique1.com']
    price_adjustment = 100
    download_delay = 1

    def parse(self, response):
        """ getting the form submit url for changing the shipping and currency """
        shipping_url = 'https://www.boutique1.com/storeswitcher/store/switch/'
        data = {
            'shipping_code': 'AL',
            'currency': 'EUR',
            '___store': 'en_eur'
        }

        yield scrapy.FormRequest(url=shipping_url, formdata=data, callback=self.parse_site)

    def parse_site(self, response):
        """ crawling site for products pages urls """
        for level_two_category_menu in response.css('li.subcategory-menu-item'):
            level_two_category_menu_link = level_two_category_menu.css('a::attr(href)').get()
            yield response.follow(url=level_two_category_menu_link, callback=self.parse_products)

    def parse_products(self, response):
        """ parsing the products pages """
        for product in response.css('li.product-item a::attr(href)'):
            yield scrapy.Request(url=product.get(), callback=self.parse_product)

        # looping on next product pages
        for next_page in response.css('li.current + .item a::attr(href)'):
            yield response.follow(url=next_page.get(), callback=self.parse_products)

    def parse_product(self, response):
        """ parsing the product  """
        def extract_from_css(query):
            return response.css(query)
        # getting product Image URLs from page inline script
        parse_scripts = response.css('body').get()
        image_urls = re.findall('"img":"(.+?)",', parse_scripts)
        sku_list = re.findall('"optionStockStatuses":(.+?)}}},', parse_scripts)

        yield {
            'retailer_sku': extract_from_css('.product-info-main .price-final_price::attr(data-product-id)').get(),
            'name': extract_from_css('.product-info-main .page-title-wrapper h1 span::text').get(),
            'price': float(extract_from_css('[itemprop=price]::attr(content)').get())*self.price_adjustment,
            'market': extract_from_css('#change-destination strong span::attr(data-value)').get(),
            'currency': extract_from_css('[itemprop=priceCurrency]::attr(content)').get(),
            'url': response.url,
            'description': extract_from_css('.product.attribute.detail p::text').getall(),
            'image_urls':   image_urls,
            'sku_list':   sku_list
                }

