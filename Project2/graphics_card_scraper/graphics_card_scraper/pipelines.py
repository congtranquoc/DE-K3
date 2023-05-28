from itemadapter import ItemAdapter
import csv
import json
import mysql.connector
from mysql.connector import Error

class GraphicsCardScraperPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ryantran@7',
            database='newegg_db'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ItemID VARCHAR(255),
                Title VARCHAR(255),
                Branding VARCHAR(255),
                Rating FLOAT,
                NumRatings INT,
                Price FLOAT,
                Shipping VARCHAR(255),
                TotalPrice FLOAT,
                ImageURL VARCHAR(255),
                Details JSON
            )
        """)

    def process_item(self, item, spider):
        self.store_item(item)
        return item

    def store_item(self, item):
        str_price = item['Price']
        if str_price is None:
            price = 0.0
        else:
            price = float(str_price)
        total_price = price + self.calculate_shipping_price(item['Shipping'])
        details = {}
        if 'MaxResolution' in item:
            details['MaxResolution'] = item['MaxResolution']
        if 'DisplayPort' in item:
            details['DisplayPort'] = item['DisplayPort']
        if 'HDMI' in item:
            details['HDMI'] = item['HDMI']
        if 'DirectX' in item:
            details['DirectX'] = item['DirectX']
        if 'Model' in item:
            details['Model'] = item['Model']

        details_json = json.dumps(details)

        query = """
            INSERT INTO products (ItemID, Title, Branding, Rating, NumRatings, Price, Shipping, TotalPrice, ImageURL, Details)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            item['ItemID'],
            item['Title'],
            item['Branding'],
            item['Rating'],
            item['RatingCount'],
            item['Price'],
            item['Shipping'],
            total_price,
            item['ImageURL'],
            details_json
        )
        self.curr.execute(query, values)
        self.conn.commit()

    def calculate_shipping_price(self, shipping):
        try:
            if shipping == 'Free Shipping':
                return 0.0
            elif shipping is None:
                return 0.0
            else:
                price_str = shipping.replace('$', '').replace(' Shipping', '')
                return float(price_str)
        except ValueError:
                return 0.0
        