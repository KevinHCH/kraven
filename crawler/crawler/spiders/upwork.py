from typing import Iterable
import scrapy
import json
import logging
import re
from urllib.parse import urlparse, urlunparse
from selectolax.parser import HTMLParser
from scrapy.http import JsonRequest
import dateparser
from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class UpworkSpider(scrapy.Spider):
    name = "upwork"
    allowed_domains = ["upwork.com"]
    # start_urls = ["https://upwork.com"]

    docker_endpoint = "http://flaresolverr:8191/v1"

    def __init__(self, target_url=None, topic_name=None, *args, **kwargs):
        super(UpworkSpider, self).__init__(*args, **kwargs)
        self.target_url = target_url
        self.topic_name = topic_name

    def start_requests(self):
        logging.info(f"Starting {self.topic_name} spider")
        logging.info(f"Target URL: {self.target_url}")
        """Send the request to flaresolverr to bypass protections"""
        payload = {
            "cmd": "request.get",
            "url": self.target_url,
            "maxTimeout": 30000,  # 30 seconds (milliseconds)
        }
        # Send the request to the Docker container (flaresolverr)
        yield JsonRequest(
            url=self.docker_endpoint,
            data=payload,
            callback=self.parse,
            method="POST",
            headers={"Content-Type": "application/json"},
            meta={"name": self.topic_name, "target_url": self.target_url},
            dont_filter=True,
        )

    def parse(self, response):
        # response_data = json.loads(response.text)
        try:
            response_data = json.loads(response.text)
        except json.JSONDecodeError:
            # Handle invalid JSON response
            logging.error(f"Failed to decode JSON from FlareSolverr: {response.text}")
            return

        if response_data["status"] != "ok":
            # Handle error, send notification if necessary
            if "Timeout" not in response_data["message"]:
                logging.error(f"Timeout error: {response_data['message']}")
                # notifier.send_notification(response_data["message"])
            raise Exception(f"Error: {response_data['message']}")

        # Get the HTML content from the response
        html = response_data["solution"]["response"]
        if not html:
            # If no HTML content is returned, log the error and stop processing
            logging.error("No HTML content returned by FlareSolverr.")
            return

        dom = HTMLParser(html)
        articles = dom.css("article")
        if not articles:
            logging.info("No articles found in the HTML.")
            return
        for article in articles:
            posted_at = article.css_first(".job-tile-header small").text().strip()
            posted_at_datetime = self.parse_datetime(posted_at)
            title = article.css_first(".job-tile-header h2").text().strip()
            title = self.sanitize(title)
            url = article.css_first(".job-tile-header h2 a").attributes.get("href")
            url = self.complete_url(url)
            job_type = article.css_first("[data-test=job-type-label]").text().strip()
            experience_level = article.css_first("[data-test=experience-level]").text()
            duration = article.css_first("[data-test=duration-label]")
            duration = self.sanitize(duration.text().strip()) if duration else None
            description = article.css_first("p.text-body-sm").text().strip()
            price = article.css_first("[data-test=is-fixed-price]")
            price = price.text() if price else None

            if not self.contains_terms_to_avoid(posted_at):
                yield {
                    "title": title,
                    "url": url,
                    "posted_at": posted_at,
                    "posted_at_datetime": posted_at_datetime,
                    "price": price,
                    "job_type": job_type,
                    "duration": duration,
                    "experience_level": experience_level,
                    "description": description,
                    "topic_name": self.topic_name,
                }

    def sanitize(self, text):
        cleaned_text = re.sub(r"\n|\t", "", text)
        return re.sub(r"\s+", " ", cleaned_text)

    def complete_url(self, url):
        base_url = "https://www.upwork.com"
        parsed_url = urlparse(base_url + url)
        return urlunparse(parsed_url._replace(query=""))

    def contains_terms_to_avoid(self, text):
        terms_to_avoid = ["last week", "days ago", "weeks ago"]
        return any(term in text.lower() for term in terms_to_avoid)

    def parse_datetime(self, text):
        cleaned_text = text.lower().replace("posted", "").strip()
        dt = dateparser.parse(cleaned_text)
        if dt is None:
            return text
        return dt
