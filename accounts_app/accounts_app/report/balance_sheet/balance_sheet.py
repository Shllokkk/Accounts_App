# Copyright (c) 2026, Shllok and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum

# from erpnext.accounts.utils import get_fiscal_year


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
		{"label": _("Net"), "fieldname": "net", "fieldtype": "Currency", "width": 200},
	]


def get_data(filters) -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""

	start_date, end_date = get_fiscal_year(filters)

	net_balances = get_net_balance_data(filters, start_date, end_date)

	account_tree_data = get_accounts_tree_data(filters)

	parent_account_map = frappe._dict()

	for row in account_tree_data:
		if row.parent_account not in parent_account_map:
			parent_account_map.setdefault(row.parent_account, [])
		parent_account_map.get(row.parent_account).append(row.name)

	account_map = {}

	for row in account_tree_data:
		account_map[row.name] = row

	final_data, _ = traversal(None, 0, parent_account_map, account_map, net_balances)

	return final_data


def get_fiscal_year(filters):
	FiscalYear = DocType("Fiscal Year")

	get_dates_query = (
		frappe.qb.from_(FiscalYear)
		.select(FiscalYear.start_date, FiscalYear.end_date)
		.where(FiscalYear.name == filters.get("fiscal_year"))
	)
	fiscal_year_data = get_dates_query.run(as_dict=True)

	start_date = fiscal_year_data[0].get("start_date")
	end_date = fiscal_year_data[0].get("end_date")

	return start_date, end_date


def get_net_balance_data(filters, start_date, end_date):
	GLEntry = DocType("GL Entry")

	get_balance_query = (
		frappe.qb.from_(GLEntry)
		.select(
			GLEntry.account, Sum(GLEntry.debit).as_("total_debit"), Sum(GLEntry.credit).as_("total_credit")
		)
		.where(
			(GLEntry.company == filters.get("company")) & (GLEntry.posting_date.between(start_date, end_date))
		)
		.groupby(GLEntry.account)
	)

	balance_data = get_balance_query.run(as_dict=True)

	net_balances = {}

	for row in balance_data:
		net_balances[row.account] = row.total_debit - row.total_credit
		if net_balances[row.account] < 0:
			net_balances[row.account] = abs(net_balances[row.account])

	return net_balances


def get_accounts_tree_data(filters):
	Account = DocType("Account")

	get_accounts_tree_query = (
		frappe.qb.from_(Account)
		.select(Account.name, Account.parent_account, Account.root_type, Account.is_group)
		.where(
			(Account.company == filters.get("company")) & (Account.root_type.isin(["Assets", "Liabilities"]))
		)
		.orderby(Account.lft, Account.rgt)
	)

	account_tree_data = get_accounts_tree_query.run(as_dict=True)

	return account_tree_data


def traversal(parent, indent, parent_account_map, account_map, net_balances):
	final_rows = []
	total = 0

	for acc_name in parent_account_map.get(parent, []):
		account_record = account_map.get(acc_name)
		balance = net_balances.get(acc_name, 0)

		if account_record.is_group == 1:
			child_rows, balance = traversal(
				acc_name, indent + 1, parent_account_map, account_map, net_balances
			)

		final_rows.append(
			{
				"account": acc_name,
				"net": balance,
				"indent": indent,
				"is_group": account_record.is_group,
				"root_type": account_record.root_type,
			}
		)

		if account_record.is_group == 1:
			final_rows.extend(child_rows)

		total += balance

	return final_rows, total
