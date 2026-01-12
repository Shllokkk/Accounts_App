// Copyright (c) 2026, Shllok and contributors
// For license information, please see license.txt

// can do the same logic through the ui property panel
// frappe.ui.form.on("Account", {
// 	is_group(frm) {
//         let is_checked = frm.doc.is_group;

//         if(is_checked) {
//             frm.set_df_property('balance', 'hidden', '1');
//         } else {
//             frm.set_df_property('balance', 'hidden', '0');
//         }
//     }
// });

frappe.ui.form.on("Account", {
    root_type(frm) {
        let type = frm.doc.root_type;

        if(type == "Assets" || type == "Expenses")
            frm.set_value('type', 'Debit');
        else
            frm.set_value('type', 'Credit');
    }
});
