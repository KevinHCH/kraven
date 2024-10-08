# Notes

### Scrapy
- create a scrapy project: `scrapy startproject <project_name>`
- move to the project directory: `cd <project_name>`
- create a new spider: `scrapy genspider spider_name spider_url`

### Django
- create a new project: `django-admin startproject <project_name>`
- create a new app: `python manage.py startapp <app_name>`
- install tailwindcss: [click here](https://medium.com/@josemiguel.sandoval20/como-usar-tailwind-css-en-una-app-de-django-5b7eafafae21)
- To load the models from an existing database in django use this command: `python manage.py inspectdb > <app_name>/models.py`

## Deploy Django to prod
- It's very important to use the gunicorn package to have the server running in the background and whitenoise package for the static files