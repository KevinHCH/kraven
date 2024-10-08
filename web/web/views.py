from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Jobs
import json, time


def index(request):
    jobs_list = Jobs.objects.all().order_by("-posted_at_datetime")
    paginator = Paginator(jobs_list, 20)
    page_number = request.GET.get("page", 1)
    jobs = paginator.get_page(page_number)
    return render(request, "index.html", {"jobs": jobs, "paginator": paginator})


def stream(request):
    def generator():

        try:
            while True:
                now = timezone.now()
                two_minutes_ago = now - timedelta(minutes=2)
                jobs = Jobs.objects.filter(created_at__gte=two_minutes_ago).order_by(
                    "-created_at"
                )
                if jobs.exists():
                    # Convert job data to a list of dictionaries
                    json_jobs = [
                        {
                            "id": job.id,
                            "title": job.title,
                            "url": job.url,
                            "posted_at": job.posted_at,
                            "job_type": job.job_type,
                            "experience_level": job.experience_level,
                            "description": job.description,
                            "price": job.price,
                        }
                        for job in jobs
                    ]

                    # Send the new jobs as SSE data
                    yield f"data: {json.dumps(json_jobs)}\n\n"
                else:
                    yield f"event: keep-alive\ndata: NO_NEW_JOBS\n\n"

                time.sleep(10)

        except GeneratorExit:
            print("Generator exited")
            pass

    return StreamingHttpResponse(generator(), content_type="text/event-stream")


def json_test(request):
    # jobs = Jobs.objects.all().order_by("-created_at")[0:3]
    now = timezone.now()
    two_minutes_ago = now - timedelta(minutes=2)
    jobs = Jobs.objects.filter(created_at__gte=two_minutes_ago).order_by("-created_at")

    json_jobs = [
        {
            "title": job.title,
            "created_at": timezone.datetime.strftime(
                job.created_at, "%Y-%m-%d %H:%M:%S"
            ),
        }
        for job in jobs
    ]
    return JsonResponse(json_jobs, safe=False)
