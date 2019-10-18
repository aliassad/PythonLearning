# -*- coding: utf-8 -*-
import scrapy


class ProductsSpider(scrapy.Spider):
    name = 'products_trail'
    allowed_domains = ['www.boutique1.com']
    start_urls = ['https://www.boutique1.com']

    def parse(self, response):
        # getting level 0 categories list
        for level_zero_main_categories in response.css('li.level0.level-top.parent'):
            main_categories_level_zero_link = level_zero_main_categories.css('a.level-top').get()
            main_categories_level_zero_name = level_zero_main_categories.css('a.level-top span::text').get()
            # getting level 1 categories menu items
            for level_one_category_menu in level_zero_main_categories.css('li.category-menu-item'):
                level_one_category_menu_name = level_one_category_menu.css('a:first-child::text').get()
                level_one_category_menu_link = level_zero_main_categories.css('a:first-child::attr(href)').get()
                # getting level 2 sub-categories menu items
                for level_two_category_menu in level_zero_main_categories.css('li.subcategory-menu-item'):
                    level_two_category_menu_name = level_two_category_menu.css('a::text').get()
                    level_two_category_menu_link = level_two_category_menu.css('a::attr(href)').get()
                    yield {
                        'urls': level_two_category_menu_link
                    }
