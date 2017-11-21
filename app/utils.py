import csv, datetime
from io import BytesIO
from xhtml2pdf import pisa
from .models import Donor,Donation,Item
from django.http import HttpResponse
from django.template.loader import get_template



def parser(csvfile):
	'''
	Helper Function
	Checks for existing donor matching the given parameter:
	- if exists, return donor_id
	- else, create new Donor object and return its donor_id
	'''
	def getDonor(donor_name_f, email_f, want_receipt_f, telephone_number_f, mobile_number_f, address_line_f, city_f, province_f, postal_code_f):

		want_receipt_f = True if (want_receipt_f.lower() == "email") or (want_receipt_f.lower() == "e-mail") else False

		result_donor = None
		try:
			result_donor = Donor.objects.get(donor_name = donor_name_f, email = email_f, want_receipt = want_receipt_f, telephone_number = telephone_number_f, mobile_number = mobile_number_f, address_line = address_line_f, city = city_f, province = province_f, postal_code=postal_code_f, verified=True)
		except Donor.DoesNotExist:
			result_donor = Donor.objects.create(donor_name = donor_name_f, email = email_f, want_receipt = want_receipt_f, telephone_number = telephone_number_f, mobile_number = mobile_number_f, address_line = address_line_f, city = city_f, province = province_f, postal_code=postal_code_f, verified=True)

		return result_donor.id

	'''
	Helper Function
	Checks for existing donation matching the given parameter:
	- if exists, return donation_id/tax_receipt_no
	- else, create new Donation object and return its donation_id/tax_receipt_no
	'''
	def getDonation(donor_id_f, tax_receipt_no_f, donate_date_f):
		result_donation = None

		donate_date_f = parseDate(donate_date_f)
		donor_id_f = Donor.objects.get(id = donor_id_f)
		try:
			result_donation = Donation.objects.get(tax_receipt_no=tax_receipt_no_f)
			# result_donation = Donation.objects.get(donor_id=donor_id_f, tax_receipt_no=tax_receipt_no_f, donate_date = donate_date_f, donor_city = donor_city_f)
		except Donation.DoesNotExist:
			result_donation = Donation.objects.create(donor_id=donor_id_f, tax_receipt_no=tax_receipt_no_f, donate_date = donate_date_f, verified=True)

		# TODO: Return primary key
		return result_donation

	'''
	Helper Function
	Insert new Item using the parameters
	Returns nothing
	'''
	def addItem(donation_id_f, description_f, particulars_f, manufacturer_f, model_f, quantity_f, working_f, condition_f, quality_f, batch_f, value_f):
		working_f = True if (working_f == "Y") else False
		value_f = 0 if (not value_f) else value_f
		Item.objects.create(tax_receipt_no=donation_id_f, description = description_f, particulars = particulars_f, manufacturer=manufacturer_f, model=model_f, quantity=quantity_f, working=working_f,condition = condition_f, quality=quality_f, batch=batch_f, value=value_f, verified=True)
		return

	'''
	Helper Function
	Takes verbose date
	Returns string
	'''
	def parseDate(date_f):

		date_f = date_f.split(", ")[1]
		date_f = date_f.split(" ")

		months = {"January": "01","February": "02","March": "03","April": "04","May": "05","June": "06","July": "07","August": "08","September": "09","October": "10","November": "11","December": "12"}

		result = date_f[2] + "-" + months.get(date_f[1]) + "-" + date_f[0]
		return result

	# Use the 10b dummy.csv
	read_file = csv.reader(csvfile, delimiter = ',')
	rowcount = 0
	verified = True
	# Donor Variables - verified is same for all
	donor_name_f, email_f, want_receipt_f, telephone_number_f, mobile_number_f, address_line_f, city_f, province_f, postal_code_f = None,None,None,None,None,None,None,None,None
	# Donation Variables - verified is same for all - donor_id pull from donor
	tax_receipt_no_f, donate_date_f, donor_city_f = None,None,None
	# Item Variables - verified is same for all - tax_receipt_no pull from donation
	description_f, particulars_f, manufacturer_f, model_f, quantity_f, working_f, condition_f, quality_f, batch_f, value_f = None,None,None,None,None,None,None,None,None,None

	for row in read_file:
		if(rowcount != 0):
			donor_name_f         = row[4]
			email_f              = row[15]
			want_receipt_f       = row[14]
			telephone_number_f   = row[11]
			mobile_number_f      = row[12]
			address_line_f       = row[5]
			city_f               = row[7]
			province_f           = row[8]
			postal_code_f        = row[9]
			donor_id_f           = None
			tax_receipt_no_f     = row[1]
			donate_date_f        = row[3]
			description_f        = row[21]
			particulars_f		 = row[22]
			manufacturer_f       = row[17]
			model_f              = row[20]
			quantity_f           = row[16]
			working_f            = row[23]
			condition_f          = row[24]
			quality_f            = row[25]
			batch_f              = row[26]
			value_f              = row[27]
			donor_id = getDonor(donor_name_f, email_f, want_receipt_f, telephone_number_f, mobile_number_f, address_line_f, city_f, province_f, postal_code_f);
			donation_id = getDonation(donor_id, tax_receipt_no_f, donate_date_f) # donation_id = tax_receipt_no
			addItem(donation_id, description_f, particulars_f, manufacturer_f, model_f, quantity_f, working_f, condition_f, quality_f, batch_f, value_f)
		rowcount += 1

def render_to_pdf(template_src,tax_no, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		response = HttpResponse(result.getvalue(), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=Tax Receipt '+ tax_no +'.pdf'
		return response
	return None

def generate_zip(pdf_array, pdf_array_names):
	# Open HttpResponse
	response = HttpResponse(content_type='application/zip')
	# Get date
	today = datetime.date.today()
	today_date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
	# Set correct content-disposition
	zip_csv_filename = 'Tax Receipts ' + today_date + '.zip'
	response['Content-Disposition'] = 'attachment; filename=' + zip_csv_filename
	# Open the file, writable
	zip = zipfile.ZipFile(response, 'w')

	idx = 0
	for name in pdf_array_names:
		zip.writestr(name, pdf_array[idx].getvalue())
		idx += 1

	# Must close zip for all contents to be written
	zip.close()

	return response
