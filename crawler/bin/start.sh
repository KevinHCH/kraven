#!/bin/sh
# Start the cron daemon and the Scrapyd server
crond
exec scrapyd