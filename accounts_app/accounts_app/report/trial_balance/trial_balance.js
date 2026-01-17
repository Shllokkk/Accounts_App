// Copyright (c) 2026, Shllok and contributors
// For license information, please see license.txt

frappe.query_reports["Trial Balance"] = {
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && data.is_total) {
			value = `<b class="text-danger">${value}</b>`;
		}
		return value;
	},

	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
		},
	],
};
