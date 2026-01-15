# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JournalEntry(Document):
	def validate(self):
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

	def on_submit(self):
		for row in self.entries:
			gl_entry = frappe.get_doc({
				"doctype": "GL Entry",
				"posting_date": self.posting_date,
				"voucher_type": self.doctype,
				"voucher_no": self.name,
				"account": row.account,
				"debit": row.debit,
				"credit": row.credit,
			})
			gl_entry.insert(ignore_permissions = True)

	def on_cancel(self):
		frappe.db.delete("GL Entry", {
			"voucher_no": self.name,
		})
