# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class Account(NestedSet):
	def validate(self):
		self.validate_type_field(self)
		self.validate_account_type_field(self)
		self.validate_parent_account_field(self)

	def validate_type_field(self):
		if self.root_type in ("Assets", "Expenses"):
			self.type = "Debit"
		elif self.root_type in ("Liabilities", "Income"):
			self.type = "Credit"
		else:
			self.type = None

	def validate_account_type_field(self):
		if not self.is_group and not self.account_type:
			frappe.throw("Account Type is mandatory for leaf accounts")

	def validate_parent_account_field(self):
		parent = frappe.get_doc("Account", self.parent_account)
		if parent.root_type != self.root_type:
			frappe.throw("Parent Account must have the same Root Type")
		if not parent.is_group:
			frappe.throw("Parent Account must be a group account")

@frappe.whitelist()
def get_children(doctype, parent=None, company=None):
	filters = {}

	if not parent or parent == company:
		filters["parent_account"] = None
	else:
		filters["parent_account"] = parent

	if company:
		filters["company"] = company

	result = frappe.get_all(
		doctype,
		fields=[
			"name as value",
			"is_group as expandable",
		],
		filters=filters,
		order_by="lft",
	)

	return result
