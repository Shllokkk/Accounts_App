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
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_invalid_name_with_letters(self):
		doc = frappe.get_doc({
			"doctype": "Fiscal Year",
			"fy_name": "abcd-2025",
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_invalid_name_with_wrong_format(self):
		doc = frappe.get_doc({
			"doctype": "Fiscal Year",
			"fy_name": "24-25",
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_same_year_on_both_sides(self):
		doc = frappe.get_doc({
			"doctype": "Fiscal Year",
			"fy_name": "2024-2024",
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_start_end_dates_validation(self):
		doc = frappe.get_doc({
			"doctype": "Fiscal Year",
			"fy_name": "2029-2030"
		})

		doc.insert()

		test_doc = frappe.get_doc("Fiscal Year", doc.name)

		self.assertEqual("2029-04-01", str(test_doc.start_date))
		self.assertEqual("2030-03-31", str(test_doc.end_date))
