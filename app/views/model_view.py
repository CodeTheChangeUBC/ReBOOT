# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.models import Donor, Donation, Item
from django.http import HttpResponseBadRequest, JsonResponse, QueryDict
from django.views import View
import simplejson as json
import datetime


class DonorView(View):
    """DonorView
    - GET: Return JSON serialized Donor object
    - POST: Insert and return that Donor object
    - PUT: Update and return that Donor object
    - DELETE: Delete and return HTTP status code
    """

    def get(self, request):
        try:
            donor = Donor.objects.get(id=request.GET['id'])
            return JsonResponse(donor.camel_serialize(), status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()

    def post(self, request):
        try:
            donor = Donor.objects.create(
                donor_name=request.POST['donorName'],
                email=request.POST['email'],
                want_receipt='wantReceipt' in request.POST,
                telephone_number=request.POST['telephoneNumber'],
                mobile_number=request.POST['mobileNumber'],
                address_line=request.POST['addressLine'],
                city=request.POST['city'],
                province=request.POST['province'],
                postal_code=request.POST['postalCode'],
                customer_ref=request.POST['customerRef'],
                verified='verified' in request.POST
            )
            return JsonResponse(donor.camel_serialize(), status=201)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()

    def put(self, request):
        try:
            request.PUT = QueryDict(request.body)
            donor = Donor.objects.get(id=request.PUT['id'])
            donor.donor_name = request.PUT['donorName']
            donor.email = request.PUT['email']
            donor.want_receipt = 'wantReceipt' in request.PUT
            donor.telephone_number = request.PUT['telephoneNumber']
            donor.mobile_number = request.PUT['mobileNumber']
            donor.address_line = request.PUT['addressLine']
            donor.city = request.PUT['city']
            donor.province = request.PUT['province']
            donor.postal_code = request.PUT['postalCode']
            donor.customer_ref = request.PUT['customerRef']
            donor.verified = 'verified' in request.PUT
            donor.save()
            return JsonResponse(donor.camel_serialize(), status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()

    def delete(self, request):
        try:
            request.DELETE = QueryDict(request.body)
            donor = Donor.objects.get(id=request.DELETE['id'])
            donor.delete()
            return JsonResponse({}, status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()


class DonationView(View):
    """DonationView
    - GET: Return Donation object based on tax_receipt_no
    - GET: Return JSON serialized Donation objects based on donor id
    - POST: Insert and return that Donation object
    - PUT: Update and return that Donation object
    - DELETE: Delete and return HTTP status code
    """

    def get(self, request):
        try:
            donation = Donation.objects.get(tax_receipt_no=request.GET['taxReceiptNo'])
            return JsonResponse(donation.camel_serialize(), status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()

    def post(self, request):
        try:
            donation = Donation.objects.create(
                donor_id=Donor.objects.get(id=request.POST['donorId']),
                donate_date=datetime.datetime.strptime(
                    request.POST['donateDate'], '%Y-%m-%d').date(),
                verified='verified' in request.POST,
                pick_up=request.POST['pickUp']
            )
            return JsonResponse(donation.camel_serialize(), status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()

    def put(self, request):
        try:
            request.PUT = QueryDict(request.body)
            donation = Donation.objects.get(
                tax_receipt_no=request.PUT['taxReceiptNo'])
            donation.donate_date = request.PUT['donateDate']
            donation.verified = 'verified' in request.PUT
            donation.pick_up = request.PUT['pickUp']
            donation.save()
            return JsonResponse(donation.camel_serialize(), status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()

    def delete(self, request):
        try:
            request.DELETE = QueryDict(request.body)
            donation = Donation.objects.get(
                tax_receipt_no=request.DELETE['taxReceiptNo'])
            donation.delete()
            return JsonResponse({}, status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()


class ItemView(View):
    """ItemView
    - GET: Return JSON serialized Item objects based on donation id
    - POST: Insert and return Item object
    - PUT: Update and return Item object
    - DELETE: Delete and return HTTP status code
    """

    def get(self, request):
        try:
            item = Item.objects.get(id=request.GET['id'])
            return JsonResponse(item.underscore_serialize(), status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()

    def post(self, request):
        try:
            item = Item.objects.create(
                tax_receipt_no=Donation.objects.get(
                    tax_receipt_no=request.POST['tax_receipt_no']),
                description=request.POST['description'],
                particulars=request.POST['particulars'],
                manufacturer=request.POST['manufacturer'],
                model=request.POST['model'],
                quantity=request.POST['quantity'],
                working='working' in request.POST,
                condition=request.POST['condition'],
                quality=request.POST['quality'],
                status=request.POST['status'],
                batch=request.POST['batch'],
                value=request.POST['value'],
                verified='verified' in request.POST
            )
            return JsonResponse(item.underscore_serialize(), status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()

    def put(self, request):
        try:
            request.PUT = QueryDict(request.body)
            item = Item.objects.get(id=request.PUT['item_id'])
            item.description = request.PUT['description']
            item.particulars = request.PUT['particulars']
            item.manufacturer = request.PUT['manufacturer']
            item.model = request.PUT['model']
            item.quantity = request.PUT['quantity']
            item.working = 'working' in request.PUT
            item.condition = request.PUT['condition']
            item.quality = request.PUT['quality']
            item.status=request.POST['status'],
            item.batch = request.PUT['batch']
            item.value = request.PUT['value']
            item.verified = 'verified' in request.PUT
            item.save()
            return JsonResponse(item.underscore_serialize(), status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()

    def delete(self, request):
        try:
            request.DELETE = QueryDict(request.body)
            item = Item.objects.get(id=request.DELETE['id'])
            item.delete()
            return JsonResponse({}, status=200)
        except Exception as e:
            print e.args
            return HttpResponseBadRequest()
