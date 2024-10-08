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

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class UpworkSpider(scrapy.Spider):
    name = "upwork"
    allowed_domains = ["upwork.com"]
    start_urls = ["https://upwork.com"]

    docker_endpoint = "http://127.0.0.1:8191/v1"

    def start_requests(self):
        file_path = BASE_DIR / "data" / "urls.json"
        with open(file_path, "r") as f:
            urls = json.load(f)
        for search_item in urls:
            name = search_item["name"]
            target_url = search_item["url"]
            logging.info(
                f"Sending POST request to Docker service for {name}: {target_url}"
            )

            payload = {
                "cmd": "request.get",
                "url": target_url,
                "maxTimeout": 30000,  # 30 seconds (milliseconds)
            }
            # Send the request to the Docker container (flaresolver)
            yield JsonRequest(
                url=self.docker_endpoint,
                data=payload,
                callback=self.parse,
                method="POST",
                headers={"Content-Type": "application/json"},
                meta={"name": name, "target_url": target_url},
                dont_filter=True,
            )

    def parse(self, response):
        response_data = json.loads(response.text)

        if response_data["status"] != "ok":
            # Handle error, send notification if necessary
            if "Timeout" not in response_data["message"]:
                logging.error(f"Timeout error: {response_data['message']}")
                # notifier.send_notification(response_data["message"])
            raise Exception(f"Error: {response_data['message']}")

        # Get the HTML content from the response
        html = response_data["solution"]["response"]

        dom = HTMLParser(html)
        articles = dom.css("article")
        for article in articles:
            posted_at = article.css_first(".job-tile-header small").text().strip()
            parsed_posted_at = self.parse_datetime(posted_at)
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
                    "posted_at": parsed_posted_at,
                    "price": price,
                    "job_type": job_type,
                    "duration": duration,
                    "experience_level": experience_level,
                    "description": description,
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
        dt = dateparser.parse(text)
        if dt is None:
            return text

        return dt.astimezone()
