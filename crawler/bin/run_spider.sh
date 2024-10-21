#!/bin/sh
LOCKFILE=/tmp/spider.lock

if [ -f $LOCKFILE ]; then
    echo "Spider is already running. Exiting."
    exit 1
fi

touch $LOCKFILE
python /app/bin/run_spider.py >> /var/log/cron.log 2>&1
rm $LOCKFILE
