# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
import re
from frappe.model.document import Document


class FiscalYear(Document):

	def validate(self): 
		name_str = re.match(r"^(\d{4})-(\d{4})$", self.name)

		if not name_str:
			frappe.throw("Fiscal Yrear name must be in the format YYYY-YYYY")
		
		# start_year = int(name_str.group(1))
		# end_year = int(name_str.group(2))

		# if self.start_date.year != start_year or self.end_date.year != end_year:
		# 	frappe.throw(f"Start and end dates must match the years in the name: {self.name}")
