FROM python:3.12-alpine

RUN apk add --no-cache curl tzdata dcron
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 6800

RUN chmod +x /app/bin/start.sh
RUN chmod +x /app/bin/run_spider.sh
RUN echo "*/3 * * * * /app/bin/run_spider.sh >> /var/log/cron.log 2>&1" > /etc/crontabs/root

# Create a Scrapyd configuration file, binding this address will allow to access the Scrapyd API from outside the container
RUN echo "[scrapyd]" > /app/scrapyd.conf && \
  echo "bind_address = 0.0.0.0" >> /app/scrapyd.conf

CMD ["./bin/start.sh"]