from itemadapter import ItemAdapter
import csv
import mysql.connector
import json

class GraphicsCardScraperPipeline:
    def __init__(self):
        self.file = None
        self.writer = None
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        self.file = open('data.csv', 'a', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=['ItemID', 'Title', 'Branding', 'Rating', 'RatingCount', 'Price', 'Shipping', 'ImageURL'])
        self.writer.writeheader()

        self.connection = mysql.connector.connect(
            host='your_host',
            user='your_user',
            password='your_password',
            database='your_database'
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.file.close()
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        # Ghi dữ liệu vào file CSV
        self.writer.writerow(item)

        # Tính toán total_price dựa trên giá shipping
        shipping = item['Shipping']
        price = item['Price']
        total_price = price + shipping

        # Chuyển đổi thông tin chi tiết sản phẩm thành định dạng JSON
        details = json.dumps(item.get('Details', {}))

        # Insert thông tin vào cơ sở dữ liệu MySQL
        query = """
        INSERT INTO your_table (ItemID, Title, Branding, Rating, RatingCount, Price, Shipping, TotalPrice, Details)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            item['ItemID'],
            item['Title'],
            item['Branding'],
            item['Rating'],
            item['RatingCount'],
            item['Price'],
            shipping,
            total_price,
            details
        )
        self.cursor.execute(query, values)
        self.connection.commit()

        return item
