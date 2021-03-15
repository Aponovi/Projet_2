# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class CsvmanagerPipeline(object):
    def process_item(self, item, spider):
        vide = False
        with open(item["category"] + '.csv', 'a', newline='') as file:
            pass

        with open(item["category"] + '.csv', 'r+', newline='') as file:
            line = file.readline()
            if line == '':
               vide = True

        with open(item["category"] + '.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, [
                'product_page_url',
                'universal_product_code (upc)',
                'title',
                'price_including_tax',
                'price_excluding_tax',
                'number_available',
                'product_description',
                'category',
                'review_rating',
                'image_url'])
            if vide:
                writer.writeheader()
            writer.writerow(item)
        return item
