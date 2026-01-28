# Copyright (c) 2026, Shllok and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today

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

		doc.append(
			"entries",
			{
				"account": "Bank Account",
				"debit": 0,
				"credit": 100,
			},
		)

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_debit_from_credit_to_same_account_validation(self):
		doc = frappe.new_doc("Journal Entry")
		doc.company = "SG Dies"
		doc.posting_date = "2026-01-21"

		doc.append(
			"entries",
			{
				"account": "Bank Account",
				"debit": 100,
				"credit": 100,
			},
		)

		doc.append(
			"entries",
			{
				"account": "Inventory",
				"debit": 100,
				"credit": 0,
			},
		)

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_debit_credit_amount_validation(self):
		doc = frappe.new_doc("Journal Entry")
		doc.company = "SG Dies"
		doc.posting_date = "2026-01-21"

		doc.append(
			"entries",
			{
				"account": "Bank Account",
				"debit": 0,
				"credit": 1000,
			},
		)

		doc.append(
			"entries",
			{
				"account": "Inventory",
				"debit": 100,
				"credit": 0,
			},
		)

		self.assertRaises(frappe.ValidationError, doc.insert)

	def test_gl_entry_creation_on_submit(self):
		doc = frappe.new_doc("Journal Entry")
		doc.company = "SG Dies"
		doc.posting_date = "2026-01-21"

		doc.append(
			"entries",
			{
				"account": "Bank Account",
				"debit": 0,
				"credit": 100,
			},
		)

		doc.append(
			"entries",
			{
				"account": "Inventory",
				"debit": 100,
				"credit": 0,
			},
		)

		doc.insert()
		doc.submit()

		gl_entries = frappe.db.get_all("GL Entry", filters={"voucher_no": doc.name})

		self.assertEqual(len(gl_entries), len(doc.entries))

	def test_gl_entry_reversal_on_cancel(self):
		doc = frappe.new_doc("Journal Entry")
		doc.company = "SG Dies"
		doc.posting_date = "2026-01-17"

		doc.append(
			"entries",
			{
				"account": "Bank Account",
				"debit": 0,
				"credit": 100,
			},
		)

		doc.append(
			"entries",
			{
				"account": "Inventory",
				"debit": 100,
				"credit": 0,
			},
		)

		doc.insert()
		doc.submit()
		doc.cancel()

		gl_entries = frappe.db.get_all(
			"GL Entry",
			filters={"voucher_no": doc.name, "posting_date": doc.posting_date},
			fields=["name", "account", "debit", "credit"],
		)
		rev_gl_entries = frappe.db.get_all(
			"GL Entry",
			filters={"voucher_no": doc.name, "posting_date": today()},
			fields=["name", "account", "debit", "credit"],
		)

		self.assertEqual(len(rev_gl_entries), len(gl_entries))

		iter = 0

		while iter < len(gl_entries):
			self.assertEqual(gl_entries[iter].account, rev_gl_entries[iter].account)
			self.assertEqual(gl_entries[iter].debit, rev_gl_entries[iter].credit)
			self.assertEqual(gl_entries[iter].credit, rev_gl_entries[iter].debit)
			iter += 1
