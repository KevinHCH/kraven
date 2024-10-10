# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from pathlib import Path
from datetime import datetime

# BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent
print("base_dir", BASE_DIR)


class SQLitePipeline:
    def open_spider(self, spider):
        # Connect to the SQLite database
        db_path = BASE_DIR / "data" / "jobs.db"
        print(f"Connecting to database: {db_path}")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        # Create the jobs table if it doesn't exist
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS jobs
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT, 
                                url TEXT, 
                                posted_at TEXT,
                                posted_at_datetime TEXT,
                                job_type TEXT, 
                                experience_level TEXT, 
                                description TEXT,
                                created_at TIMESTAMP NOT NULL,
                                price TEXT,
                                sended_at TIMESTAMP
                               )"""
        )

    def close_spider(self, spider):
        # Close the database connection
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        now = datetime.now()
        self.cursor.execute(
            """
            INSERT INTO jobs (title, url, posted_at, posted_at_datetime, job_type, experience_level, description, price, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
        """,
            (
                item["title"],
                item["url"],
                item["posted_at"],
                item["posted_at_datetime"],
                item["job_type"],
                item["experience_level"],
                item["description"],
                item["price"],
                now,
            ),
        )
        return item
