# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PurchaseInvoice(Document):
	def validate(self):
		self.calculate_amt_and_total_amt()
		self.validate_debit_to_account()
		self.validate_credit_from_account()
		
	def on_submit(self):
		self.create_gl_entries()
		
	def on_cancel(self):
		frappe.db.delete("GL Entry", {
			"voucher_no": self.name,
		})

	def calculate_amt_and_total_amt(self):
		total_invoice_amount = 0
	
		for row in self.item_list:
			row.amount = row.quantity * row.rate
			total_invoice_amount += row.amount

		self.total_invoice_amount = total_invoice_amount

	def validate_debit_to_account(self):
		account = frappe.get_doc("Account", self.debit_to)

		if(account.account_type != "Stock"):
			frappe.throw("Debit To account must be of the type Stock")

	def validate_credit_from_account(self):
		account = frappe.get_doc("Account", self.credit_from)

		if(account.account_type not in ["Cash", "Payable"]):
			frappe.throw("Credit from account must be of the type Cash or Payable")

	def create_gl_entries(self):
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
			"account": self.debit_to,
			"debit": self.total_invoice_amount,
			"credit": 0,
		})

		gl_entry1.insert()
		gl_entry2.insert()
