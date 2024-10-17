# KRAVEN

## Overview

This is a personal project designed to showcase skills in both **Scrapy** (for web crawling) and **Django** (for web development). The project is divided into three main components:
- **Crawler**: A Scrapy project that scrapes job listings from Upwork and stores them in a SQLite database.
- **Data**: A folder where the `urls.json` file (containing URLs to scrape) is located, as well as where the SQLite database will be stored.
- **Web**: A Django web application that connects to the SQLite database and displays relevant job listings based on user search criteria.

The entire project runs using Docker to make local deployment easy and manageable.

## Project Structure

- **crawler/**: The Scrapy project responsible for scraping Upwork job listings.
- **data/**: Contains the `urls.json` file and the SQLite database where the scraped job data will be stored.
- **web/**: The Django application that displays jobs and allows filtering based on custom searches.

## Getting Started

### Prerequisites

Make sure you have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setting Up Locally

1. **Add the URLs to Scrape**:
   - Create a `urls.json` file inside the `data/` folder with the list of URLs you want to scrape. The format should be as follows:
     ```json
     [
       {
         "name": "example-job",
         "url": "https://www.upwork.com/job-url"
       }
     ]
     ```

2. **Build and Run Docker Containers**:
   - Run the following commands to build and run the project in the background:
     ```bash
     docker-compose build
     docker-compose up -d
     ```

3. **Access the Web Application**:
   - Open your browser and navigate to `http://localhost:8000`. Here, you can search and filter through the scraped job data.

## Usage

### Scraping Jobs

To start the Scrapy crawler for Upwork jobs, ensure that the `urls.json` file is properly configured with the URLs you want to scrape, and then run the Docker container as explained in the setup.

The Scrapy spider will scrape the jobs and store the data into a SQLite database located inside the `data/` folder.

### Viewing Jobs in Django

Once the jobs are scraped, you can visit the Django web app on `http://localhost:8000` to view and search the available jobs.

## Disclaimer

This project was created to **showcase my skills as a freelancer** and demonstrate what I can accomplish with web scraping and web development. I'm not responsible for any misuse of this project. Please ensure that you comply with Upwork’s terms of service if you intend to scrape data from their site.

