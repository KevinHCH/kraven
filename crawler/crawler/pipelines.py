# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# BASE_DIR = Path(__file__).resolve().parent.parent


class SQLitePipeline:
    def __init__(self):
        # Set up database connection parameters
        self.db_path = BASE_DIR / "data" / "jobs.db"
        self.conn = None
        self.cursor = None
        self.open_connection()

    def open_connection(self):
        """Open a database connection with a thread-safe configuration."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=10)
        self.conn.row_factory = sqlite3.Row  # Enables row-based access
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the jobs table if it doesn't exist."""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                url TEXT,
                posted_at TEXT,
                posted_at_datetime TIMESTAMP,
                job_type TEXT,
                experience_level TEXT,
                description TEXT,
                created_at TIMESTAMP NOT NULL,
                price TEXT,
                sended_at TIMESTAMP,
                topic_name TEXT
            )
            """
        )
        self.conn.commit()

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def open_spider(self, spider):
        """Reopen the database connection at the start of the spider run."""
        if self.conn is None:
            self.open_connection()

    def close_spider(self, spider):
        """Close the database connection when the spider finishes."""
        self.close_connection()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("SELECT 1 FROM jobs WHERE url = ?", (item["url"],))
            result = self.cursor.fetchone()
            if not result:
                print(f"Saving new job: {item['title']}")
                self.cursor.execute(
                    """
                    INSERT INTO jobs (title, url, posted_at, posted_at_datetime, job_type, experience_level, description, price, created_at, topic_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                        datetime.now(),
                        item["topic_name"],
                    ),
                )
                self.conn.commit()
            else:
                print(f"Job already exists: {item['title']}")
        except sqlite3.OperationalError as e:
            # Handle database error with a retry mechanism
            print(f"Database error: {e}")
            self.close_connection()
            self.open_connection()  # Reconnect and retry
        return item
