# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalesInvoice(Document):
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
			"account": "Inventory",
			"debit": 0,
			"credit": self.total_amount,
		})
		gl_entry2 = frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"account": "Cost of Goods Sold",
			"debit": self.total_amount,
			"credit": 0,
		})
		gl_entry1.insert(ignore_permissions = True)
		gl_entry2.insert(ignore_permissions = True)

		gl_entry3 = frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"account": "Proceeds from Sales ",
			"debit": 0,
			"credit": self.total_amount,
		})
		gl_entry4 = frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"account": "Bank Account",
			"debit": self.total_amount,
			"credit": 0,
		})
		gl_entry3.insert(ignore_permissions = True)
		gl_entry4.insert(ignore_permissions = True)