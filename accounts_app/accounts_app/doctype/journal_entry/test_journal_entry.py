# Copyright (c) 2026, Shllok and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestJournalEntry(IntegrationTestCase):
	"""
	Integration tests for JournalEntry.
	Use this class for testing interactions between multiple components.
	"""

	def test_number_of_entries_validation(self):
		doc = frappe.new_doc("Journal Entry")
		doc.company = "SG Dies"
		doc.posting_date = "2026-01-21"
		
		doc.append("entries", {
			"account": "Bank Account",
			"debit": 0,
			"credit": 100,
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_debit_from_credit_to_same_account_validation(self):
		doc = frappe.new_doc("Journal Entry")
		doc.company = "SG Dies"
		doc.posting_date = "2026-01-21"
		
		doc.append("entries", {
			"account": "Bank Account",
			"debit": 100,
			"credit": 100,
		})

		doc.append("entries", {
			"account": "Inventory",
			"debit": 100,
			"credit": 0,
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_debit_credit_amount_validation(self):
		doc = frappe.new_doc("Journal Entry")
		doc.company = "SG Dies"
		doc.posting_date = "2026-01-21"
		
		doc.append("entries", {
			"account": "Bank Account",
			"debit": 0,
			"credit": 1000,
		})

		doc.append("entries", {
			"account": "Inventory",
			"debit": 100,
			"credit": 0,
		})

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_gl_entry_creation(self):
		doc = frappe.new_doc("Journal Entry")
		doc.company = "SG Dies"
		doc.posting_date = "2026-01-21"
		
		doc.append("entries", {
			"account": "Bank Account",
			"debit": 0,
			"credit": 100,
		})

		doc.append("entries", {
			"account": "Inventory",
			"debit": 100,
			"credit": 0,
		})

		doc.insert()
		doc.submit()

		self.assertTrue(frappe.db.exists("GL Entry", {"voucher_no": doc.name}))
