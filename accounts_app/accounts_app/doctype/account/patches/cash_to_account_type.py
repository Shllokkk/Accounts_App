import frappe
from frappe.query_builder import DocType

def execute():
	"""Change cash check field to account_type select"""

	Account = DocType("Account")
	query = frappe.qb.update(Account).set(
				Account.account_type , "Cash"
			).where(
				Account.cash == 1
			)
	
	query.run()
