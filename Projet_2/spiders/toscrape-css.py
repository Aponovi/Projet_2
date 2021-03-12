# -*- coding: utf-8 -*-
import scrapy
import re
import ipdb


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = ['http://books.toscrape.com/catalogue/category/books/poetry_23/index.html']
    # start_urls = ['http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html']
    url = "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html"
    products_pod = []
    # numero = 0

    def lecture_categorie(self, response):
        for categorie in response.css("article.product_pod"):
            cat = categorie.css("h3 > a::attr(href)").extract_first()
            cat = cat.replace("../../../", "http://books.toscrape.com/catalogue/")
            return (re(url, callback=self.lecture_livre) for url in response.css.extract())

    def lecture_livre(self, response):
        article = response.css("article.product_page")
        yield {
            'product_page_url': "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
            'universal_product_code (upc)': article.css("table th:contains('UPC') + td::text").extract_first(),
            'title': article.css("h1::text").extract_first(),
            'price_including_tax': article.css("table th:contains('Price (incl. tax)') + td::text").extract_first(),
            'price_excluding_tax': article.css("table th:contains('Price (excl. tax)') + td::text").extract_first(),
            'number_available': re.search(r"[^\D]+", article.css("table th:contains('Availability') "
                                                                 "+ td::text").extract_first()).group(),
            'product_description': article.css("div#product_description + p::text").extract_first(),
            'category': response.css("ul.breadcrumb > li:nth-child(3) > a::text").extract_first(),
            'review_rating': article.css(
                "p.star-rating::attr(class)").extract_first().replace("star-rating ", "").replace(
                "One", "1").replace("Two", "2").replace("Three", "3").replace("Four", "4").replace("Five", "5"),
            'image_url': ((article.css("img::attr(src)").extract_first()).replace("../..",
                                                                                  "http://books.toscrape.com"))
             }
        # yield {'test': "test"}

    def parse(self, response):
        # ipdb.set_trace(context=6)
        if self is not None:
            if self.url is not None:
                if self.url.find('/catalogue/category/') == -1:
                    self.lecture_livre(response)
                    # yield {'test': "test"}
                else:
                    self.lecture_categorie(response)


        # next_page_url = response.css("li.next > a::attr(href)").extract_first()
        #         if self.numero < len(self.products_pod):
        #             next_page_url = self.products_pod[self.numero]
        #             self.numero += 1
        #             self.url = next_page_url
        #         else:
        #             next_page_url = None
        #         if next_page_url is not None:
        #             yield scrapy.Request(response.urljoin(next_page_url))
