# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
import re
import ipdb


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [ #'http://books.toscrape.com/catalogue/category/books/default_15/index.html'
                   'http://books.toscrape.com/catalogue/category/books_1/index.html',
                  ]
    products_pod = []
    # categories = []

    # def liste_categorie(self, response):
    #     for categorie in response.css("ul.nav li li"):
    #         # print(categorie)
    #         cat = categorie.css("li a::attr(href)").extract_first()
    #         # print(cat)
    #         if cat is not None:
    #             cat = cat.replace("../", "http://books.toscrape.com/catalogue/category/")
    #             self.categories.append(cat)

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
            'image_url': ((article.css("img::attr(src)").extract_first()).replace("../..",
                                                                                  "http://books.toscrape.com"))
        }

    def parse(self, response):

        # self.liste_categorie(response)
        # print(self.categories)

        self.liste_livres_categorie(response)
        yield from response.follow_all(self.products_pod, self.description_livre)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)




process = CrawlerProcess(settings={
    'FEEDS': {
        "items.csv": {'format': "csv"},
    },
    'ITEM_PIPELINES' : {
        'Projet_2.pipelines.CsvmanagerPipeline': 300
    }
})



process.crawl(ToScrapeCSSSpider)
process.start()


# http://books.toscrape.com/catalogue/category/books/travel_2/index.html
# runner = CrawlerRunner()
#
#
# @defer.inlineCallbacks
# def crawl():
#     yield crawl(ToScrapeCSSSpider, start_urls=['http://books.toscrape.com/catalogue/category/books/default_15/index.html'])
#     yield crawl(ToScrapeCSSSpider, start_urls=['http://books.toscrape.com/catalogue/category/books/travel_2/index.html'])
#     reactor.stop()
#
#
# crawl()
# reactor.run()

# process.crawl(ToScrapeCSSSpider,
#               start_urls=['http://books.toscrape.com/catalogue/category/books/default_15/index.html'])
# process.start(stop_after_crawl=False)
# process = CrawlerProcess(settings={
#     'FEEDS': {
#         'items2.csv': {'format': "csv"},
#     },
# })
# process.crawl(ToScrapeCSSSpider, start_urls=['http://books.toscrape.com/catalogue/category/books/travel_2/index.html'])
# process.start()
