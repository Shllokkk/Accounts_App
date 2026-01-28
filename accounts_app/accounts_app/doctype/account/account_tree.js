frappe.provide("frappe.treeview_settings");

frappe.treeview_settings["Account"] = {
	breadcrumb: "Account",
	get_tree_root: false,
    get_tree_nodes: "accounts_app.accounts_app.doctype.account.account.get_children",

	filters: [
		{
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			label: "Company",
			reqd: 1,

			on_change() {
				const tree_obj = frappe.treeview_settings.Account.treeview;
				const company = tree_obj.page.fields_dict.company.get_value();

				if (!company) {
					frappe.throw("Please select a Company!");
				}

                tree_obj.args = tree_obj.args || {};
				tree_obj.args.company = company;
                tree_obj.root_node = null;

				tree_obj.refresh();
			},
		},
	],
};
