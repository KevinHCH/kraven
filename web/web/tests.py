from .models import Jobs
from django.db import connection
from django.utils import timezone


def setup():
    Jobs.objects.create(
        title="Test Job 2",
        url="https://example.com/job2",
        posted_at=timezone.now(),
        job_type="Part-time",
        experience_level="Intermediate",
        description="This is a test description for job 2.",
        created_at=timezone.now(),
        price="200",
        sended_at=None,
    )


def delete_test():
    with connection.cursor() as cursor:
        cursor.execute("delete from jobs where title like '%Test%'")


def get_last_job():
    with connection.cursor() as cursor:
        query = "select id, title, created_at from jobs where title like '%Test%' order by created_at desc limit 5"
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)


delete_test()
setup()
get_last_job()
