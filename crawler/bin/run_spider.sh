#!/bin/sh

# Function to check if current time is between 09:00 and 21:00 (CET)
is_time_to_run() {
    current_hour=$(date +%H)
    if [ $current_hour -ge 9 ] && [ $current_hour -lt 21 ]; then
        return 0  
    else
        return 1  
    fi
}


if is_time_to_run; then
    # curl http://localhost:6800/schedule.json -d project=default -d spider=upwork
    jq -c '.[]' ./data/urls.json | while read -r url; do
        name=$(echo $url | jq -r '.name')
        url=$(echo $url | jq -r '.url')
        curl http://localhost:6800/schedule.json -d project=default -d spider=upwork -d target_url="$url" -d topic_name="$name"
    done
else
    echo "[$(date +%H:%M:%S)]Not running spider - outside of scheduled hours"
fi