// Copyright (c) 2026, Shllok and contributors
// For license information, please see license.txt

frappe.ui.form.on("Account", {
	root_type(frm) {
		let type = frm.doc.root_type;

		if (type == "Assets" || type == "Expenses") frm.set_value("type", "Debit");
		else if (type == "Liabilities" || type == "Income") frm.set_value("type", "Credit");
		else frm.set_value("type", "");

		frm.set_query("parent_account", function () {
			if (type == "")
				return {
					filters: {
						is_group: 1,
					},
				};
			else
				return {
					filters: {
						root_type: type,
						is_group: 1,
					},
				};
		});
	},
	is_group(frm) {
		if (frm.doc.is_group) frm.set_df_property("account_type", "read_only", "1");
		else frm.set_df_property("account_type", "read_only", "0");
	},
});
