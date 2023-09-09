# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip white spaces from string
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                adapter[field_name] = adapter.get(field_name).strip()

        # Converting to lowercase
        lowercase_keys = ["book_category", "product_type"]
        for lowercase_key in lowercase_keys:
            adapter[lowercase_key] = adapter.get(lowercase_key).lower()

        # Converting price value to float
        price_keys = ["price_excl_tax", "price_incl_tax", "tax", "price"]
        for price_key in price_keys:
            adapter[price_key] = float(adapter.get(price_key).replace("£", ""))

        # Remove unnecessary text in 'availability' values
        availability_string = adapter.get("availability")
        adapter["availability"] = int(availability_string.split("(")[1].split(" ")[0])

        # Reviews: string value to int
        adapter["num_of_reviews"] = int(adapter.get("num_of_reviews"))

        # Average rating value to float
        avg_rating_string = adapter.get("avg_rating").split(" ")[1].lower()
        if avg_rating_string == "zero":
            adapter["avg_rating"] = 0
        elif avg_rating_string == "one":
            adapter["avg_rating"] = 1
        elif avg_rating_string == "two":
            adapter["avg_rating"] = 2
        elif avg_rating_string == "three":
            adapter["avg_rating"] = 3
        elif avg_rating_string == "four":
            adapter["avg_rating"] = 4
        elif avg_rating_string == "five":
            adapter["avg_rating"] = 5

        return item
    

import mysql. connector

class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '4d2mysql14',
        database = 'books'
    )
        ## Cursor used to execute commands
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books( 
                id int NOT NULL auto_increment, 
                url VARCHAR (255),
                book_name text,
                upc VARCHAR (255),
                product_type VARCHAR (255),
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                tax DECIMAL,
                availability INTEGER,
                num_of_reviews INTEGER,
                avg_rating INTEGER,
                book_category VARCHAR (255),
                description text,
                price DECIMAL,
                PRIMARY KEY (id)
        """
        )
    
    def process_item(self, item, spider):

        # Insert statement
        self.cur.execute(""""
            url,
            book_name,
            upc,
            product_type,
            price_excl_tax,
            price_incl_tax,
            tax, 
            availability,
            num_of_reviews,
            avg_rating,
            book_category,
            description,
            price,
            )values(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""",(
                    item["url"],
                    item["book_name"],
                    item["upc"],
                    item["product_type"],
                    item["price_excl_tax"],
                    item["price_incl_tax"],
                    item["tax"],
                    item["availability"],
                    item["num_of_reviews"],
                    item["avg_rating"],
                    item["book_category"],
                    item["description"],
                    item["price"]
                )
                
            )
        self.conn.commit()
        return item

    def close_spider(self, spider):

        # Close cursor and connection with Database after spider finishes
        self.cur.close()
        self.conn.close()
