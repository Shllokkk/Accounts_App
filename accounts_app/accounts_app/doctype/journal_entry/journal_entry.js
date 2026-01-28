// Copyright (c) 2026, Shllok and contributors
// For license information, please see license.txt

frappe.ui.form.on("Journal Entry", {
	onload(frm) {
		frm.fields_dict.entries.grid.get_field("account").get_query = function () {
			return {
				filters: {
					is_group: 0,
				},
			};
		};
	},
});
