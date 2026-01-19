# Copyright (c) 2026, Shllok and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestFiscalYear(IntegrationTestCase):
	"""
	Integration tests for FiscalYear.
	Use this class for testing interactions between multiple components.
	"""

	def test_invalid_name_without_hyphen(self):
		doc = frappe.get_doc({
			"doctype": "Fiscal Year",
			"fy_name": "20242025",
			"start_date": "2024-01-23",
			"end_date": "2025-01-22",
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_invalid_name_with_letters(self):
		doc = frappe.get_doc({
			"doctype": "Fiscal Year",
			"fy_name": "abcd-2025",
			"start_date": "2024-01-23",
			"end_date": "2025-01-22",
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_invalid_name_without_hyphen(self):
		doc = frappe.get_doc({
			"doctype": "Fiscal Year",
			"fy_name": "20242025",
			"start_date": "2024-01-23",
			"end_date": "2025-01-22",
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_invalid_name_without_hyphen(self):
		doc = frappe.get_doc({
			"doctype": "Fiscal Year",
			"fy_name": "20242025",
			"start_date": "2024-01-23",
			"end_date": "2025-01-22",
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

