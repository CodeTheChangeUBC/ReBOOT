# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
import simplejson as json
import datetime
from app.model_managers import SoftDeletionModel


# Create your models here.
class Donor(SoftDeletionModel):
    PROVINCE = {
        ('AB', 'Alberta'),
        ('BC', 'British Columbia'),
        ('SK', 'Saskatchewan'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
        ('PE', 'Prince Edward Island'),
        ('NS', 'Nova Scotia'),
        ('NL', 'Newfoundland and Labrador'),
        ('NB', 'New Brunswick'),
        ('NT', 'Northwest Territories'),
        ('NU', 'Nunavut'),
        ('YT', 'Yukon')
    }
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    # message = ('Phone number must be entered in the format: '+999999999'. Up
    # to 15 digits allowed.'))
    donor_name = models.CharField(max_length=75, verbose_name='Donor Name')
    email = models.EmailField(verbose_name='E-mail')
    want_receipt = models.BooleanField(verbose_name='Tax receipt?')
    telephone_number = models.CharField(
        max_length=30, blank=True, verbose_name='Telephone #')
    mobile_number = models.CharField(
        max_length=30, blank=True, verbose_name='Mobile #')
    # telephone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, verbose_name='Telephone #')
    # mobile_number = models.CharField(validators=[phone_regex],
    # max_length=15, blank=True, verbose_name='Mobile #')
    address_line = models.CharField(
        max_length=256, verbose_name='Street Address')
    city = models.CharField(max_length=30, verbose_name='City')
    province = models.CharField(
        max_length=20, choices=PROVINCE, verbose_name='Province')
    postal_code = models.CharField(max_length=7, verbose_name='Postal Code')
    customer_ref = models.CharField(
        max_length=20, blank=True, verbose_name='Customer Ref.')
    verified = models.BooleanField(
        verbose_name='D & I Verified?', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        donations_list = Donation.objects.select_related().filter(donor_id=self.pk)
        donationtrue, itemtrue = True, True
        item_list = []

        for donation in donations_list:
            if not donation.verified:
                donationtrue = False
                receiptnumber = donation.tax_receipt_no
                item_list = Item.objects.select_related().filter(tax_receipt_no=receiptnumber)

        for item in item_list:
            if not item.verified:
                itemtrue = False

        self.verified = itemtrue and donationtrue
        super(Donor, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.pk)  # Changed to PK because donation_id was removed

    def serialize(self):
        return _serialize(self)


class Donation(SoftDeletionModel):
    donor_id = models.ForeignKey(
        Donor, on_delete=models.CASCADE, verbose_name='Donor ID')
    tax_receipt_no = models.CharField(
        max_length=9, primary_key=True, verbose_name='Tax Receipt Number')
    donate_date = models.DateField('Date Donated')
    pick_up = models.CharField(
        max_length=30, verbose_name='Pick-Up Postal', blank=True)
    verified = models.BooleanField(verbose_name='Verified Donation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.tax_receipt_no)

    def serialize(self):
        return _serialize(self)

    def save(self, *args, **kwargs):
        if self.tax_receipt_no is None or self.tax_receipt_no is "":
            self.tax_receipt_no = gen_tax_receipt_no()
        super(Donation, self).save(*args, **kwargs)


class Item(SoftDeletionModel):
    QUALITY = {
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    }
    ITEM_TYPE = {
        ('PC-DESKTOP', 'Computer Desktop'),
        ('PC-Laptop', 'Computer Laptop'),
        ('Server', 'Server'),
        ('HDD', 'Hard Disk Drive'),
        ('SSD', 'Solid State Drive'),
        ('Floppy Drive', 'Floppy Diskette'),
        ('Other Storage Device', 'Other Storage Device'),
        ('LCD Monitor', 'LCD Monitor'),
        ('LED Monitor', 'LED Monitor'),
        ('Other Monitor', 'Other Monitor'),
        ('AllInOne Printer', 'All-In-One Printer'),
        ('Inkjet Printer', 'Inkjet Printer'),
        ('Laser Printer', 'Laser Printer'),
        ('Other Printer', 'Other Printer'),
        ('Router', 'Router'),
        ('Switch', 'Network Switch'),
        ('Other Network Device', 'Other Network Device'),
        ('Keyboard', 'Keyboard'),
        ('Mice', 'Mice'),
        ('Webcam', 'Webcam'),
        ('GPU', 'Video Card'),
        ('Mic', 'Microphone'),
        ('RAM', 'Ram'),
        ('CPU', 'CPU'),
        ('HeatSink', 'Heat Sink'),
        ('HeadPhone', 'Headphones'),
        ('MotherBoard', 'MotherBoard'),
        ('PSU', 'Power Supply'),
        ('LiquidCooler', 'Liquid Cooler'),
        ('Fan', 'Fan'),
        ('Mobile Phone', 'Mobile Phone'),
        ('Cables', 'Cables/Connectors'),
        ('3d Printer', '3d Printer'),
        ('Speaker', 'Speaker'),
        ('Audio Receiver', 'Audio Receiver'),
        ('Xbox', 'Xbox'),
        ('Playstation', 'Playstation'),
        ('Other gaming console', 'Gaming console'),
        ('Camera', 'Camera'),
        ('DSLR', 'DSLR'),
        ('Tablet', 'Tablet'),
        ('CCTV Camera', 'CCTV camera'),
        ('TV', 'Television'),
        ('Other', 'Other'),
    }
    tax_receipt_no = models.ForeignKey(
        Donation, on_delete=models.CASCADE, verbose_name='Tax Receipt Number')
    description = models.CharField(
        max_length=500, choices=ITEM_TYPE, verbose_name='Description')
    particulars = models.CharField(
        max_length=500, blank=True, verbose_name='Particulars')
    manufacturer = models.CharField(
        max_length=500, blank=True, verbose_name='Manufacturer')
    model = models.CharField(max_length=50, blank=True, verbose_name='Model')
    quantity = models.IntegerField(verbose_name='Quantity')
    working = models.BooleanField(verbose_name='Is the item working?')
    condition = models.CharField(
        max_length=20, blank=True, verbose_name='Condition')
    quality = models.CharField(
        max_length=20, choices=QUALITY, verbose_name='Quality')
    batch = models.CharField(max_length=20, blank=True, verbose_name='Batch')
    value = models.DecimalField(
        max_digits=10, blank=True, decimal_places=2, verbose_name='Value', default=0)
    verified = models.BooleanField(verbose_name='Verified Item', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, blank=True, verbose_name='Status', default='received')

    def __unicode__(self):
        return str(self.id)

    def serialize(self):
        return _serialize(self)

'''
Private Method
'''


def _serialize(self):
    serialized_dict = self.__dict__
    if '_state' in serialized_dict:
        serialized_dict.pop('_state')
    json_str = json.dumps(serialized_dict, default=json_serial)
    return json.loads(json_str)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, Donor):
        return obj.id
    if isinstance(obj, Donation):
        return obj.tax_receipt_no
    raise TypeError("Type %s not serializable" % type(obj))

def gen_tax_receipt_no():
    donation = Donation.objects.values('tax_receipt_no').order_by().last()
    tax_receipt_no = '0000' if donation is None else donation['tax_receipt_no'][5:]
    tax_receipt_no = int(tax_receipt_no) + 1
    return '%04d-%04d' % (datetime.date.today().year, tax_receipt_no)