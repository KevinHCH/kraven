#!/bin/sh

# Function to check if current time is between 09:00 and 21:00
is_time_to_run() {
    current_hour=$(date +%H)
    if [ $current_hour -ge 9 ] && [ $current_hour -lt 21 ]; then
        return 0  # True, it's time to run
    else
        return 1  # False, it's not time to run
    fi
}

# Check if it's time to run
if is_time_to_run; then
    # Run the spider
    curl http://localhost:6800/schedule.json -d project=your_project_name -d spider=your_spider_name
else
    echo "Not running spider - outside of scheduled hours"
fi