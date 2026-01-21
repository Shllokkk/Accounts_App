# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
import re
from frappe.model.document import Document

class FiscalYear(Document):

	def validate(self): 
		start_year, end_year = self.validate_fy_name()

		self.start_date = f"{start_year}/04/01"
		self.end_date = f"{end_year}/03/31"

	def validate_fy_name(self):
		name_str = re.match(r"^(\d{4})-(\d{4})$", self.name)

		if not name_str:
			frappe.throw("Fiscal Year name must be in the format YYYY-YYYY")

		start_year = int(name_str.group(1))
		end_year = int(name_str.group(2))

		difference = end_year - start_year

		if difference < 0:
			frappe.throw("Start Year cannot be greater than End Year!")
		elif difference == 0:
			frappe.throw("Start Year and End Year cannot be same!")
		elif difference > 1:
			frappe.throw("Start Year and End Year cannot be more than 1 year apart!")

		return start_year, end_year
