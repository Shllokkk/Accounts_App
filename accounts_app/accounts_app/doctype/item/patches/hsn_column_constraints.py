import frappe


def execute():
	"""alters the hsn column constraints"""

	def execute():
		frappe.db.sql("""
			ALTER TABLE `tabItem`
			DROP INDEX `hsn`
		""")

		frappe.db.sql("""
			ALTER TABLE `tabItem`
			MODIFY `hsn` INT NULL
		""")
