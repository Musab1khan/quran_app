import frappe
from frappe.model.document import Document

class Surah(Document):
    def validate(self):
        # Count ayahs for this surah
        ayah_count = frappe.db.count("Ayah", {"surah": self.name})
        self.ayah_count = ayah_count
