// Copyright (c) 2026, Shllok and contributors
// For license information, please see license.txt

frappe.ui.form.on("Invoice Item", {
	quantity(frm, cdt, cdn) {
        calculate_amount(cdt, cdn);
    },
    rate(frm, cdt, cdn) {
        calculate_amount(cdt, cdn);
    }
});

function calculate_amount(cdt, cdn) {
    let row = locals[cdt][cdn];
    row.amount = row.quantity * row.rate;
    refresh_field['Item List']
}
