import scrapy


class GraphicsCardSpider(scrapy.Spider):
    name = "graphics-card-spider"
    allowed_domains = ["www.newegg.com"]
    start_urls = ["https://www.newegg.com/GPUs-Video-Graphics-Cards/SubCategory/ID-48/Page-{page}?Tid=7709".format(page=i) for i in range(1, 2)]

    def parse(self, response):
        products = response.css('.item-cell')

        for product in products:
            item_id = product.css('.item-container::attr(id)').get()

            item = {
                'ItemID': item_id,
                'Title': product.css('.item-title::text').get(),
                'Branding': product.css('.item-branding::text').get(),
                'Rating': product.css('.rating::text').get(),
                'RatingCount': product.css('.item-rating-num::text').get(),
                'Price': float(product.css('.price-current strong::text').get().replace(',', '')),
                'Shipping': product.css('.shipping .price-ship::text').get(),
                'ImageURL': product.css('.item-cell .item-img img::attr(src)').get(),
            }

            details_url = product.css('.item-title a::attr(href)').get()
            yield response.follow(details_url, callback=self.parse_details, meta={'item': item})

    def parse_details(self, response):
        item = response.meta['item']
        specifications = response.css('.item-specifications .list-group .list-group-item')

        for spec in specifications:
            key = spec.css('.specification-key::text').get()
            value = spec.css('.specification-value::text').get()

            if key == 'Max Resolution':
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

