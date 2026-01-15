# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class Account(NestedSet):
	def validate(self):
		if self.is_group and self.cash:
			frappe.throw("Cash account can be set for Leaf accounts only!")
