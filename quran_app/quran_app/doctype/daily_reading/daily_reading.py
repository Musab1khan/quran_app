import frappe
from frappe.model.document import Document

class DailyReading(Document):
    def validate(self):
        self.calculate_total_ayahs()
    
    def calculate_total_ayahs(self):
        """Calculate total ayahs read"""
        total = 0
        
        if self.start_surah == self.end_surah:
            # Same surah
            total = self.end_ayah - self.start_ayah + 1
        else:
            # Different surahs
            start_surah_number = frappe.db.get_value("Surah", self.start_surah, "number")
            end_surah_number = frappe.db.get_value("Surah", self.end_surah, "number")
            
            # Add remaining ayahs from start surah
            start_ayah_count = frappe.db.count("Ayah", {"surah": self.start_surah})
            total += start_ayah_count - self.start_ayah + 1
            
            # Add ayahs from middle surahs
            for surah_num in range(start_surah_number + 1, end_surah_number):
                surah_name = frappe.db.get_value("Surah", {"number": surah_num}, "name")
                total += frappe.db.count("Ayah", {"surah": surah_name})
            
            # Add ayahs from end surah
            total += self.end_ayah
        
        self.total_ayahs_read = total
