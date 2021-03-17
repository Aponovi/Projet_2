# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
import re
import hashlib


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = ['http://books.toscrape.com/catalogue/category/books_1/index.html',
                  ]
    products_pod = []

    def liste_livres_categorie(self, response):
        for liste_livres in response.css("article.product_pod"):
            livre = liste_livres.css("h3 > a::attr(href)").extract_first()
            livre = livre.replace("../../../", "http://books.toscrape.com/catalogue/")
            self.products_pod.append(livre)

    def description_livre(self, response):
        article = response.css("article.product_page")
        yield {
            'product_page_url': response.url,
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
            'image_urls': [((article.css("img::attr(src)").extract_first()).replace("../..",
                                                                                    "http://books.toscrape.com"))],
            'images': hashlib.sha1(((article.css(
                "img::attr(src)").extract_first()).replace("../..", "http://books.toscrape.com")).encode(
                'utf-8')).hexdigest()
        }

    def parse(self, response):
        self.liste_livres_categorie(response)
        yield from response.follow_all(self.products_pod, self.description_livre)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)


process = CrawlerProcess(settings={
    'FEEDS': {
        "books.csv": {'format': "csv"},
    },
    'ITEM_PIPELINES': {
        'Projet_2.pipelines.CsvManagerPipeline': 300,
        'scrapy.pipelines.images.ImagesPipeline': 400,
    },
    'IMAGES_STORE': './Images'
})

process.crawl(ToScrapeCSSSpider)
process.start()
