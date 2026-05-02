import frappe
from frappe.utils import today, getdate

@frappe.whitelist()
def search_ayahs(search_text=None, surah=None, page=None, juz=None, limit=50):
    """
    Search for ayahs by text, surah, page, or juz
    """
    filters = {}
    
    if surah:
        filters["surah"] = surah
    if page:
        filters["page"] = page
    if juz:
        filters["juz"] = juz
    
    if search_text:
        # Search in both Arabic and translation
        ayahs = frappe.db.sql("""
            SELECT name, surah, number, number_in_surah, text_arabic, text_translation, page, juz
            FROM `tabAyah`
            WHERE text_arabic LIKE %(search)s OR text_translation LIKE %(search)s
            LIMIT %(limit)s
        """, {"search": f"%{search_text}%", "limit": limit}, as_dict=True)
    else:
        ayahs = frappe.get_all("Ayah", 
            filters=filters,
            fields=["name", "surah", "number", "number_in_surah", "text_arabic", "text_translation", "page", "juz"],
            limit=limit
        )
    
    return ayahs

@frappe.whitelist()
def get_surah_list():
    """Get list of all surahs"""
    return frappe.get_all("Surah", 
        fields=["name", "number", "name_ar", "name_en", "name_en_translation", "type", "ayah_count"],
        order_by="number asc"
    )

@frappe.whitelist()
def get_ayahs_by_surah(surah, start_ayah=1, end_ayah=None):
    """Get ayahs for a specific surah"""
    filters = {"surah": surah}
    
    if end_ayah:
        filters["number_in_surah"]= ["between", [start_ayah, end_ayah]]
    else:
        filters["number_in_surah"]= [">=", start_ayah]
    
    return frappe.get_all("Ayah",
        filters=filters,
        fields=["name", "number", "number_in_surah", "text_arabic", "text_translation", "page"],
        order_by="number_in_surah asc"
    )

@frappe.whitelist()
def get_daily_reading_progress(user=None, date=None):
    """Get user's daily reading progress"""
    if not user:
        user = frappe.session.user
    if not date:
        date = today()
    
    readings = frappe.get_all("Daily Reading",
        filters={"user": user, "reading_date": date},
        fields=["name", "start_surah", "start_ayah", "end_surah", "end_ayah", "total_ayahs_read", "notes"]
    )
    
    total_ayahs = sum([r.total_ayahs_read for r in readings]) if readings else 0
    
    return {
        "readings": readings,
        "total_ayahs_today": total_ayahs
    }

@frappe.whitelist()
def create_daily_reading(start_surah, start_ayah, end_surah, end_ayah, notes=""):
    """Create a new daily reading entry"""
    reading = frappe.get_doc({
        "doctype": "Daily Reading",
        "user": frappe.session.user,
        "reading_date": today(),
        "start_surah": start_surah,
        "start_ayah": int(start_ayah),
        "end_surah": end_surah,
        "end_ayah": int(end_ayah),
        "notes": notes
    })
    reading.insert()
    frappe.db.commit()
    return reading.name

@frappe.whitelist()
def get_reading_stats(user=None, days=30):
    """Get reading statistics for last N days"""
    if not user:
        user = frappe.session.user
    
    from_date = frappe.utils.add_days(today(), -days)
    
    stats = frappe.db.sql("""
        SELECT 
            reading_date,
            SUM(total_ayahs_read) as total_ayahs
        FROM `tabDaily Reading`
        WHERE user = %(user)s AND reading_date >= %(from_date)s
        GROUP BY reading_date
        ORDER BY reading_date DESC
    """, {"user": user, "from_date": from_date}, as_dict=True)
    
    return stats

@frappe.whitelist()
def get_random_ayah():
    """Get a random ayah for daily inspiration"""
    import random
    count = frappe.db.count("Ayah")
    random_number = random.randint(1, count)
    
    ayah = frappe.get_all("Ayah",
        filters={"number": random_number},
        fields=["name", "surah", "number", "number_in_surah", "text_arabic", "text_translation"],
        limit=1
    )
    
    return ayah[0] if ayah else None
