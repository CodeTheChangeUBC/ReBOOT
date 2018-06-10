# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.result import AsyncResult
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from app.worker.parser import parser
from app.worker.generate_pdf import generate_pdf
from app.models import Donor, Donation, Item
import csv
import simplejson as json


@login_required(login_url="/login")
def new_form(request):
    context = _context("Donation Form")
    return render(request, "app/form.html", context)


@login_required(login_url="/login")
def get_analytics(request):
    context = _context("Analytics")
    return render(request, "app/analytics.html", context)


@login_required(login_url="/login")
def import_csv(request):
    """A view to redirect after task queuing csv parser
    """
    if "job" in request.GET:
        return _poll_state_response(request)
    elif request.POST:
        csv_file = request.FILES.get("my_file", False)
        if (csv_file and csv_file.name.endswith(".csv")):
            job = parser.delay(csv_file)
            return HttpResponseRedirect(
                reverse("import_csv") + "?job=" + job.id)
        else:
            return _error(request)
    else:
        return HttpResponseRedirect("/")


@login_required(login_url="/login")
def export_csv(request):
    """A view to redirect after task queuing csv exporter
    """
    return HttpResponseRedirect("/")
    if "job" in request.GET:
        return _poll_state_response(request)
    elif request.POST:
        csv_file = request.FILES.get("my_file", False)
        if (csv_file and csv_file.name.endswith(".csv")):
            job = parser.delay(csv_file)
            return HttpResponseRedirect(
                reverse("export_csv") + "?job=" + job.id)
        else:
            return _error(request)
    else:
        return HttpResponseRedirect("/")


@login_required(login_url="/login")
def poll_state(request):
    """A view to report the progress to the user
    """
    if request.is_ajax() and request.POST["task_id"]:
        task_id = request.POST["task_id"]
        task = AsyncResult(task_id)
        response = task.result or task.state

    if isinstance(response, dict):
        return JsonResponse(response)
    elif isinstance(response, str):
        return HttpResponse(response)
    elif _is_file(response):
        return HttpResponse("SUCCESS")
    else:
        return response


@login_required(login_url="/login")
def start_pdf_gen(request):
    """Initialize pdf generation from tasks
    Takes request from admin which contains request.queryset
    """
    if "job" in request.GET:
        return _poll_state_response(request)
    elif request.POST:
        job = generate_pdf.delay(request.queryset)
        return HttpResponseRedirect(
            reverse("start_pdf_gen") + "?job=" + job.id)
    else:
        return _error(request)


def download_file(request, task_id=0):
    """Downloads file after task is complete
    """
    try:
        task_id = request.GET["task_id"]
    except BaseException:
        return HttpResponseRedirect('/')
    work = AsyncResult(task_id)

    try:
        if not work.ready():
            raise FileNotFoundError()
        result = work.get(timeout=1)
        work.forget()
        if _is_zip(result):
            return HttpResponse(result, content_type="application/zip")
        elif _is_csv(result):
            return HttpResponse(result, content_type="application/csv")
        else:
            return result
    except BaseException:
        return _error(request)


"""
Private Methods
"""


def _is_file(file):
    content_type_name = file.get("Content-Type")
    file_types = ["zip", "pdf", "csv"]
    return any(file_type in content_type_name for file_type in file_types)


def _is_zip(file):
    content_type_name = file.get("Content-Type")
    return "zip" in content_type_name


def _is_pdf(file):
    content_type_name = file.get("Content-Type")
    return "pdf" in content_type_name


def _is_csv(file):
    content_type_name = file.get("Content-Type")
    return "csv" in content_type_name


def _poll_state_response(request):
    job_id = request.GET["job"]
    job = AsyncResult(job_id)
    data = job.result or job.state
    context = _context("Poll State", {
        "data": data,
        "task_id": job_id
    })
    return render(request, "app/PollState.html", context)


def _context(title, override={}):
    context = {
        "title": title,
        "has_permission": True,
    }
    context.update(override)
    return context


def _error(request):
    context = _context("Something went wrong")
    return render(request, "app/error.html", context)
