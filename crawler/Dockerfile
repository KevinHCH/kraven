FROM python:3.12-alpine

RUN apk add --no-cache curl tzdata dcron jq
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Expose Scrapyd port
EXPOSE 6800

# Deploy Scrapy project as egg
RUN pip install scrapyd-client && scrapyd-deploy --build-egg /app/crawler.egg

# Set up Scrapyd configuration file
RUN echo "[scrapyd]" > /app/scrapyd.conf && \
  echo "bind_address = 0.0.0.0" >> /app/scrapyd.conf && \
  echo "eggs_dir = /app/eggs" >> /app/scrapyd.conf && \
  echo "dbs_dir = /app/dbs" >> /app/scrapyd.conf

# setup the cron job
COPY crontab /etc/crontabs/root

# Ensure scripts are executable
RUN chmod +x /app/bin/start.sh
RUN chmod +x /app/bin/run_spider.sh

# Start cron daemon and Scrapyd server
CMD ["./bin/start.sh"]
