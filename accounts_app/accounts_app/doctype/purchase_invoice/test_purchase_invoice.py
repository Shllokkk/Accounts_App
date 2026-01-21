# Copyright (c) 2026, Shllok and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestPurchaseInvoice(IntegrationTestCase):
	"""
	Integration tests for PurchaseInvoice.
	Use this class for testing interactions between multiple components.
	"""

	def test_row_amt_and_total_amt_calculation_pass(self):
		doc = frappe.new_doc("Purchase Invoice")
		doc.company = "SG Dies"
		doc.seller = "SEL0001"
		doc.posting_date = "2026-01-17"
		doc.debit_to = "Inventory"
		doc.credit_from = "Bank Account"

		doc.append("item_list", {
			"item_name": "ITM0001",
			"quantity": 10,
			"rate": 10,
		})

		doc.insert()

		for row in doc.item_list:
			self.assertEqual(row.amount, 100)

		self.assertEqual(doc.total_invoice_amount, 100)

	def test_debit_to_account_validation_pass(self):
		doc = frappe.new_doc("Purchase Invoice")
		doc.debit_to = "Inventory"
		doc.credit_from = "Bank Account"

		doc.insert(ignore_mandatory=True)

	def test_debit_to_account_validation_fail(self):
		doc = frappe.new_doc("Purchase Invoice")
		doc.debit_to = "Bank Account"
		doc.credit_from = "Bank Account"

		self.assertRaises(frappe.ValidationError, doc.insert, ignore_mandatory=True)

	def test_credit_from_account_validation_pass(self):
		doc = frappe.new_doc("Purchase Invoice")
		doc.debit_to = "Inventory"
		doc.credit_from = "Accounts Payable"

		doc.insert(ignore_mandatory=True)

	def test_credit_from_account_validation_fail(self):
		doc = frappe.new_doc("Purchase Invoice")
		doc.debit_to = "Inventory"
		doc.credit_from = "Loans Payable"

		self.assertRaises(frappe.ValidationError, doc.insert, ignore_mandatory=True)

	def test_gl_enties_creation(self):
		doc = frappe.new_doc("Purchase Invoice")
		doc.company = "SG Dies"
		doc.seller = "SEL0001"
		doc.posting_date = "2026-01-17"
		doc.debit_to = "Inventory"
		doc.credit_from = "Bank Account"

		doc.append("item_list", {
			"item_name": "ITM0001",
			"quantity": 10,
			"rate": 10,
		})

		doc.insert()
		doc.submit()

		gl_entries = frappe.db.get_all("GL Entry", filters = {"voucher_no": doc.name})

		self.assertEqual(len(gl_entries), 2)
