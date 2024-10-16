FROM python:3.12-alpine

RUN apk add --no-cache curl tzdata nodejs npm
# Environment variables to prevent Python from writing .pyc files and to buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# generate tailwindcss styles
RUN npm i
RUN npm run gen:styles

RUN python manage.py collectstatic --noinput
RUN python manage.py compress

EXPOSE 8000
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
