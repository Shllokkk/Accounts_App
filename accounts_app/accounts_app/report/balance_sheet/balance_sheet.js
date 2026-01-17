// Copyright (c) 2026, Shllok and contributors
// For license information, please see license.txt

frappe.query_reports["Balance Sheet"] = {
	filters: [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
		},
		{
			"fieldname": "fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Select",
			"options": "\n2024-2025\n2025-2026",
			"default": "2025-2026",
			"reqd": 1,
		},
	],
};
