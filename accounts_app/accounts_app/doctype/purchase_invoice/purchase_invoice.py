# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PurchaseInvoice(Document):
	def before_save(self):
		total_amount = 0
	
		for row in self.item_list:
			total_amount += row.amount

		self.total_amount = total_amount

	def on_update(self):
		gl_entry1 = frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"account": "Bank Account",
			"debit": 0,
			"credit": self.total_amount,
		})

		gl_entry2 = frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"account": "Inventory",
			"debit": self.total_amount,
			"credit": 0,
		})

		gl_entry1.insert(ignore_permissions = True)
		gl_entry2.insert(ignore_permissions = True)