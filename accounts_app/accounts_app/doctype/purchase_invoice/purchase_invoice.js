// Copyright (c) 2026, Shllok and contributors
// For license information, please see license.txt

frappe.ui.form.on("Invoice Item", {
	quantity(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },
    rate(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    }
});

function calculate_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    row.amount = row.quantity * row.rate;
    refresh_field['item_list'];
    calculate_total(frm);
}

function calculate_total(frm) {
    let total = 0;
    for(let i=0; i<frm.doc.item_list.length; i++) {
        total += frm.doc.item_list[i].amount;
    }
    frm.set_value('total_invoice_amount', total);
}