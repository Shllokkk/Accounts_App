# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data(filters)

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Account"),
			"fieldname": "account",
			"fieldtype": "Data",
			"width": 300,
		},
		{
			"label": _("Net"),
			"fieldname" : "net",
			"fieldtype": "int",
			"width": 200
		}
	]


def get_data(filters) -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""

	GLEntry = DocType('GL Entry')
	Account = DocType('Account')

	query = frappe.qb.from_(GLEntry).join(Account).on(
				GLEntry.account == Account.name
			).select(
				(Account.root_type).as_("account"),
				(Sum(GLEntry.debit) - Sum(GLEntry.credit)).as_("net")		
			).where(
				Account.root_type.isin(["Assets", "Liabilities"])
			).groupby(Account.root_type)
	
	data = query.run(as_dict = True)

	return data
