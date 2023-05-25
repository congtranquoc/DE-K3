from itemadapter import ItemAdapter
import csv
import mysql.connector
import json

class GraphicsCardScraperPipeline:
    def process_item(self, item, spider):
        return item