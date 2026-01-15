# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SalesInvoice(Document):
	# def before_save(self):
	# 	total_invoice_amount = 0
	
	# 	for row in self.item_list:
	# 		total_invoice_amount += row.amount

	# 	self.total_invoice_amount = total_invoice_amount

	def on_submit(self):

		if(self.debit_to == "Accounts Payable"):
			frappe.throw("Cannot debit to Accounts Payable!")

		gl_entry1 = frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"account": self.credit_from,
			"debit": 0,
			"credit": self.total_invoice_amount,
		})
		gl_entry2 = frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"account": "Cost of Goods Sold",
			"debit": self.total_invoice_amount,
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
			"credit": self.total_invoice_amount,
		})
		gl_entry4 = frappe.get_doc({
			"doctype": "GL Entry",
			"posting_date": self.posting_date,
			"voucher_type": self.doctype,
			"voucher_no": self.name,
			"account": self.debit_to,
			"debit": self.total_invoice_amount,
			"credit": 0,
		})
		gl_entry3.insert(ignore_permissions = True)
		gl_entry4.insert(ignore_permissions = True)

	def on_cancel(self):
		frappe.db.delete("GL Entry", {
			"voucher_no": self.name,
		})