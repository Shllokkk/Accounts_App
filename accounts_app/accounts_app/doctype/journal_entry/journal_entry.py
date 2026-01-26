# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class JournalEntry(Document):
	def validate(self):
		self.validate_number_of_entries()

		self.validate_debit_credit_accounts()

		self.validate_debit_credit_amount()
		
	def on_submit(self):
		self.create_gl_entries()

	def on_cancel(self):
		self.create_reverse_gl_entries()
		self.cancel_original_gl_entries()

	def validate_number_of_entries(self):
		if len(self.entries) < 2:
			frappe.throw("A Journal Entry must have atleast two entries!")

	def validate_debit_credit_accounts(self):
		for row in self.entries:
			if row.debit !=0 and row.credit != 0:
				frappe.throw("An account cannot be both debited and credited in the same entry")

	def validate_debit_credit_amount(self):
		debit = 0
		credit = 0

		for row in self.entries:
			debit += row.debit
			credit += row.credit

		if debit - credit != 0:
			frappe.throw('Debit and Credit Amount must be equal!')

		else:
			self.total_debit = debit
			self.total_credit = credit
			self.difference = debit - credit

	def create_gl_entries(self):
		for row in self.entries:
			gl_entry = frappe.get_doc({
				"doctype": "GL Entry",
				"company": "SG Dies",
				"posting_date": self.posting_date,
				"voucher_type": self.doctype,
				"voucher_no": self.name,
				"account": row.account,
				"debit": row.debit,
				"credit": row.credit,
			})
			gl_entry.insert()

	def create_reverse_gl_entries(self):
		for row in self.entries:
			rev_gl_entry = frappe.new_doc("GL Entry")
			rev_gl_entry.company = "SG Dies"
			rev_gl_entry.posting_date = today()
			rev_gl_entry.voucher_type = self.doctype
			rev_gl_entry.voucher_no = self.name
			rev_gl_entry.account = row.account
			rev_gl_entry.debit = row.credit
			rev_gl_entry.credit = row.debit
			rev_gl_entry.is_cancelled = 1

			rev_gl_entry.insert()

	def cancel_original_gl_entries(self):
		gl_entries = frappe.db.get_all("GL Entry",filters = {"voucher_no": self.name})

		for g in gl_entries:
			gl_entry = frappe.get_doc("GL Entry", g.name)
			gl_entry.is_cancelled = 1
			gl_entry.save()
