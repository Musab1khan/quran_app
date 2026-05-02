import frappe

@frappe.whitelist()
def update_all_ayah_counts():
    """Update ayah_count for all Surahs"""
    surahs = frappe.db.get_all('Surah', fields=['name'])
    
    for surah in surahs:
        ayah_count = frappe.db.count('Ayah', {'surah': surah.name})
        frappe.db.set_value('Surah', surah.name, 'ayah_count', ayah_count)
    
    frappe.db.commit()
    return f"Updated {len(surahs)} surahs"
