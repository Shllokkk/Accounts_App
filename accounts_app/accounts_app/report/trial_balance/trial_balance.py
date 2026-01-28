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
			"label": _("Debit"),
			"fieldname": "debit",
			"fieldtype": "Int",
			"width": 200,
		},
		{
			"label": _("Credit"),
			"fieldname": "credit",
			"fieldtype": "Int",
			"width": 200,
		},
		{
			"label": _("Balance"),
			"fieldname": "balance",
			"fieldtype": "Int",
			"width": 200,
		},
	]


def get_data(filters) -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""

	GLEntry = DocType("GL Entry")

	query = (
		frappe.qb.from_("GL Entry")
		.select(
			GLEntry.account,
			Sum(GLEntry.debit).as_("debit"),
			Sum(GLEntry.credit).as_("credit"),
			(Sum(GLEntry.debit) - Sum(GLEntry.credit)).as_("balance"),
		)
		.where(GLEntry.posting_date.between(filters.get("from_date"), filters.get("to_date")))
		.groupby(GLEntry.account)
	)

	data = query.run(as_dict=True)

	total_debit = 0
	total_credit = 0
	total_balance = 0

	for row in data:
		total_debit += row["debit"] or 0
		total_credit += row["credit"] or 0

	total_balance = total_debit - total_credit

	data.append(
		{
			"account": "Total",
			"debit": total_debit,
			"credit": total_credit,
			"balance": total_balance,
			"is_total": 1,
		}
	)

	return data
