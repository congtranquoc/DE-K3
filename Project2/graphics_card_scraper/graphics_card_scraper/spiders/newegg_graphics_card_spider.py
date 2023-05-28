import scrapy
import re
import time

class NeweggGraphicsCardSpiderSpider(scrapy.Spider):
    name = "newegg_graphics_card_spider"
    allowed_domains = ["www.newegg.com"]
    start_urls = ["https://www.newegg.com/GPUs-Video-Graphics-Cards/SubCategory/ID-48/Page-{page}?Tid=7709".format(page=i) for i in range(1, 101)]
                
    def parse(self, response):
        products = response.css('.item-cell')

        for product in products:
            item_id = product.css('.item-container::attr(id)').get()
            rating_count = product.css('.item-rating-num::text').get()
            if rating_count is not None:
                rating_count = int(rating_count.strip('()'))
                
            rating_num = product.xpath('.//a[contains(@class, "item-rating")]/@title').get()
            print(rating_num)
            if rating_num:
                rating = re.search(r"(\d+(\.\d+)?)", rating_num).group(1) if rating_num else None
            else:
                rating = None
            branding = product.css('.item-brand img::attr(title)').get()
            price = product.css('.price-current strong::text').get()
            if price:
                price = float(price.replace(',', ''))
            item = {
                'ItemID': item_id,
                'Title': product.css('.item-title::text').get(),
                'Branding': branding,
                'Rating': rating,
                'RatingCount': rating_count,
                'Price': price,
                'Shipping': product.css('.price-ship::text').get(),
                'ImageURL': product.css('.item-cell .item-img img::attr(src)').get()
            }
            #yield item

            details_url = product.css('.item-container a::attr(href)').get()
            yield response.follow(details_url, callback=self.parse_details, meta={'item': item})
    def parse_details(self, response):
        item = response.meta['item']
        product_details = response.css('#product-details')
        tables = product_details.css('table.table-horizontal')
        for table in tables:
            caption = table.css('caption::text').get()
            rows = table.css('tbody tr')
            for row in rows:
                key = row.css('th::text').get()
                value = row.css('td::text').get()

                if key == 'Brand':
                    if item['Branding'] == '' or item['Branding'] is None:
                        item['Branding'] = value
                elif key == 'Max Resolution':
                    item['MaxResolution'] = value
                elif key == 'DisplayPort':
                    item['DisplayPort'] = value
                elif key == 'HDMI':
                    item['HDMI'] = value
                elif key == 'DirectX':
                    item['DirectX'] = value
                elif key == 'Model':
                    item['Model'] = value

        yield item