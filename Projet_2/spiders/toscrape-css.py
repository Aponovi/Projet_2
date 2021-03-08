# -*- coding: utf-8 -*-
import scrapy
import re


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = ['http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html']

    def parse(self, response):
        for article in response.css("article.product_page"):
            yield {
                # 'text': quote.css("span.text::text").extract_first(), 'author': quote.css(
                # "small.author::text").extract_first(), 'tags': quote.css("div.tags > a.tag::text").extract()
                'product_page_url': "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
                'universal_product_code(upc)': article.css("table th:contains('UPC') + td::text").extract_first(),
                'title': article.css("h1::text").extract_first(),
                'price_including_tax': article.css("table th:contains('Price (incl. tax)') + td::text").extract_first(),
                'price_excluding_tax': article.css("table th:contains('Price (excl. tax)') + td::text").extract_first(),
                'number_available': re.search(r"[^\D]+", article.css("table th:contains('Availability') "
                                                                     "+ td::text").extract_first()).group(),
                'product_description': article.css("div#product_description + p::text").extract_first(),
                'category': response.css("ul.breadcrumb > li:nth-child(3) > a::text").extract_first(),
                'review_rating': article.css("table th:contains('Number of reviews') + td::text").extract_first(),
                'image_url': article.css("img::attr(src)").extract_first()
                }

            # next_page_url = response.css("li.next > a::attr(href)").extract_first()
        next_page_url = None
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
