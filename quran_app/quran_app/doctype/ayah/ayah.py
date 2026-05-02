import frappe
from frappe.model.document import Document

class Ayah(Document):
    def validate(self):
        # Generate name
        if not self.name:
            surah_name = frappe.db.get_value("Surah", self.surah, "name_en")
            self.name = f"{surah_name}-{self.number_in_surah}"
