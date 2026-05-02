import frappe
import os

def after_install():
    """Import Quran data after installation"""
    import_quran_data()

def import_quran_data():
    """Import Surahs and Ayahs from the cloned database"""
    
    # Check if data already exists
    if frappe.db.exists("Surah", {"number": 1}):
        frappe.msgprint("Quran data already imported.")
        return
    
    # Import Surahs
    surahs = [
        {"number": 1, "name_ar": "سورة الفاتحة", "name_en": "Al-Faatiha", "name_en_translation": "The Opening", "type": "Meccan"},
        {"number": 2, "name_ar": "سورة البقرة", "name_en": "Al-Baqara", "name_en_translation": "The Cow", "type": "Medinan"},
        {"number": 3, "name_ar": "سورة آل عمران", "name_en": "Aal-i-Imraan", "name_en_translation": "The Family of Imraan", "type": "Medinan"},
        {"number": 4, "name_ar": "سورة النساء", "name_en": "An-Nisaa", "name_en_translation": "The Women", "type": "Medinan"},
        {"number": 5, "name_ar": "سورة المائدة", "name_en": "Al-Maaida", "name_en_translation": "The Table", "type": "Medinan"},
        {"number": 6, "name_ar": "سورة الأنعام", "name_en": "Al-An'aam", "name_en_translation": "The Cattle", "type": "Meccan"},
        {"number": 7, "name_ar": "سورة الأعراف", "name_en": "Al-A'raaf", "name_en_translation": "The Heights", "type": "Meccan"},
        {"number": 8, "name_ar": "سورة الأنفال", "name_en": "Al-Anfaal", "name_en_translation": "The Spoils of War", "type": "Medinan"},
        {"number": 9, "name_ar": "سورة التوبة", "name_en": "At-Tawba", "name_en_translation": "The Repentance", "type": "Medinan"},
        {"number": 10, "name_ar": "سورة يونس", "name_en": "Yunus", "name_en_translation": "Jonas", "type": "Meccan"},
        {"number": 11, "name_ar": "سورة هود", "name_en": "Hud", "name_en_translation": "Hud", "type": "Meccan"},
        {"number": 12, "name_ar": "سورة يوسف", "name_en": "Yusuf", "name_en_translation": "Joseph", "type": "Meccan"},
        {"number": 13, "name_ar": "سورة الرعد", "name_en": "Ar-Ra'd", "name_en_translation": "The Thunder", "type": "Medinan"},
        {"number": 14, "name_ar": "سورة ابراهيم", "name_en": "Ibrahim", "name_en_translation": "Abraham", "type": "Meccan"},
        {"number": 15, "name_ar": "سورة الحجر", "name_en": "Al-Hijr", "name_en_translation": "The Rock", "type": "Meccan"},
        {"number": 16, "name_ar": "سورة النحل", "name_en": "An-Nahl", "name_en_translation": "The Bee", "type": "Meccan"},
        {"number": 17, "name_ar": "سورة الإسراء", "name_en": "Al-Israa", "name_en_translation": "The Night Journey", "type": "Meccan"},
        {"number": 18, "name_ar": "سورة الكهف", "name_en": "Al-Kahf", "name_en_translation": "The Cave", "type": "Meccan"},
        {"number": 19, "name_ar": "سورة مريم", "name_en": "Maryam", "name_en_translation": "Mary", "type": "Meccan"},
        {"number": 20, "name_ar": "سورة طه", "name_en": "Taa-Haa", "name_en_translation": "Taa-Haa", "type": "Meccan"},
        {"number": 21, "name_ar": "سورة الأنبياء", "name_en": "Al-Anbiyaa", "name_en_translation": "The Prophets", "type": "Meccan"},
        {"number": 22, "name_ar": "سورة الحج", "name_en": "Al-Hajj", "name_en_translation": "The Pilgrimage", "type": "Medinan"},
        {"number": 23, "name_ar": "سورة المؤمنون", "name_en": "Al-Muminoon", "name_en_translation": "The Believers", "type": "Meccan"},
        {"number": 24, "name_ar": "سورة النور", "name_en": "An-Noor", "name_en_translation": "The Light", "type": "Medinan"},
        {"number": 25, "name_ar": "سورة الفرقان", "name_en": "Al-Furqaan", "name_en_translation": "The Criterion", "type": "Meccan"},
        {"number": 26, "name_ar": "سورة الشعراء", "name_en": "Ash-Shu'araa", "name_en_translation": "The Poets", "type": "Meccan"},
        {"number": 27, "name_ar": "سورة النمل", "name_en": "An-Naml", "name_en_translation": "The Ant", "type": "Meccan"},
        {"number": 28, "name_ar": "سورة القصص", "name_en": "Al-Qasas", "name_en_translation": "The Stories", "type": "Meccan"},
        {"number": 29, "name_ar": "سورة العنكبوت", "name_en": "Al-Ankaboot", "name_en_translation": "The Spider", "type": "Meccan"},
        {"number": 30, "name_ar": "سورة الروم", "name_en": "Ar-Room", "name_en_translation": "The Romans", "type": "Meccan"},
        {"number": 31, "name_ar": "سورة لقمان", "name_en": "Luqman", "name_en_translation": "Luqman", "type": "Meccan"},
        {"number": 32, "name_ar": "سورة السجدة", "name_en": "As-Sajda", "name_en_translation": "The Prostration", "type": "Meccan"},
        {"number": 33, "name_ar": "سورة الأحزاب", "name_en": "Al-Ahzaab", "name_en_translation": "The Clans", "type": "Medinan"},
        {"number": 34, "name_ar": "سورة سبأ", "name_en": "Saba", "name_en_translation": "Sheba", "type": "Meccan"},
        {"number": 35, "name_ar": "سورة فاطر", "name_en": "Faatir", "name_en_translation": "The Originator", "type": "Meccan"},
        {"number": 36, "name_ar": "سورة يس", "name_en": "Yaseen", "name_en_translation": "Yaseen", "type": "Meccan"},
        {"number": 37, "name_ar": "سورة الصافات", "name_en": "As-Saaffaat", "name_en_translation": "Those drawn up in Ranks", "type": "Meccan"},
        {"number": 38, "name_ar": "سورة ص", "name_en": "Saad", "name_en_translation": "The letter Saad", "type": "Meccan"},
        {"number": 39, "name_ar": "سورة الزمر", "name_en": "Az-Zumar", "name_en_translation": "The Crowds", "type": "Meccan"},
        {"number": 40, "name_ar": "سورة غافر", "name_en": "Al-Ghaafir", "name_en_translation": "The Forgiver", "type": "Meccan"},
        {"number": 41, "name_ar": "سورة فصلت", "name_en": "Fussilat", "name_en_translation": "Explained in detail", "type": "Meccan"},
        {"number": 42, "name_ar": "سورة الشورى", "name_en": "Ash-Shura", "name_en_translation": "Consultation", "type": "Meccan"},
        {"number": 43, "name_ar": "سورة الزخرف", "name_en": "Az-Zukhruf", "name_en_translation": "Ornaments of gold", "type": "Meccan"},
        {"number": 44, "name_ar": "سورة الدخان", "name_en": "Ad-Dukhaan", "name_en_translation": "The Smoke", "type": "Meccan"},
        {"number": 45, "name_ar": "سورة الجاثية", "name_en": "Al-Jaathiya", "name_en_translation": "Crouching", "type": "Meccan"},
        {"number": 46, "name_ar": "سورة الأحقاف", "name_en": "Al-Ahqaf", "name_en_translation": "The Dunes", "type": "Meccan"},
        {"number": 47, "name_ar": "سورة محمد", "name_en": "Muhammad", "name_en_translation": "Muhammad", "type": "Medinan"},
        {"number": 48, "name_ar": "سورة الفتح", "name_en": "Al-Fath", "name_en_translation": "The Victory", "type": "Medinan"},
        {"number": 49, "name_ar": "سورة الحجرات", "name_en": "Al-Hujuraat", "name_en_translation": "The Inner Apartments", "type": "Medinan"},
        {"number": 50, "name_ar": "سورة ق", "name_en": "Qaaf", "name_en_translation": "The letter Qaaf", "type": "Meccan"},
        {"number": 51, "name_ar": "سورة الذاريات", "name_en": "Adh-Dhaariyat", "name_en_translation": "The Winnowing Winds", "type": "Meccan"},
        {"number": 52, "name_ar": "سورة الطور", "name_en": "At-Tur", "name_en_translation": "The Mount", "type": "Meccan"},
        {"number": 53, "name_ar": "سورة النجم", "name_en": "An-Najm", "name_en_translation": "The Star", "type": "Meccan"},
        {"number": 54, "name_ar": "سورة القمر", "name_en": "Al-Qamar", "name_en_translation": "The Moon", "type": "Meccan"},
        {"number": 55, "name_ar": "سورة الرحمن", "name_en": "Ar-Rahmaan", "name_en_translation": "The Beneficent", "type": "Medinan"},
        {"number": 56, "name_ar": "سورة الواقعة", "name_en": "Al-Waaqia", "name_en_translation": "The Inevitable", "type": "Meccan"},
        {"number": 57, "name_ar": "سورة الحديد", "name_en": "Al-Hadid", "name_en_translation": "The Iron", "type": "Medinan"},
        {"number": 58, "name_ar": "سورة المجادلة", "name_en": "Al-Mujaadila", "name_en_translation": "The Pleading Woman", "type": "Medinan"},
        {"number": 59, "name_ar": "سورة الحشر", "name_en": "Al-Hashr", "name_en_translation": "The Exile", "type": "Medinan"},
        {"number": 60, "name_ar": "سورة الممتحنة", "name_en": "Al-Mumtahana", "name_en_translation": "She that is to be examined", "type": "Medinan"},
        {"number": 61, "name_ar": "سورة الصف", "name_en": "As-Saff", "name_en_translation": "The Ranks", "type": "Medinan"},
        {"number": 62, "name_ar": "سورة الجمعة", "name_en": "Al-Jumu'a", "name_en_translation": "Friday", "type": "Medinan"},
        {"number": 63, "name_ar": "سورة المنافقون", "name_en": "Al-Munaafiqoon", "name_en_translation": "The Hypocrites", "type": "Medinan"},
        {"number": 64, "name_ar": "سورة التغابن", "name_en": "At-Taghaabun", "name_en_translation": "Mutual Disillusion", "type": "Medinan"},
        {"number": 65, "name_ar": "سورة الطلاق", "name_en": "At-Talaaq", "name_en_translation": "Divorce", "type": "Medinan"},
        {"number": 66, "name_ar": "سورة التحريم", "name_en": "At-Tahrim", "name_en_translation": "The Prohibition", "type": "Medinan"},
        {"number": 67, "name_ar": "سورة الملك", "name_en": "Al-Mulk", "name_en_translation": "The Sovereignty", "type": "Meccan"},
        {"number": 68, "name_ar": "سورة القلم", "name_en": "Al-Qalam", "name_en_translation": "The Pen", "type": "Meccan"},
        {"number": 69, "name_ar": "سورة الحاقة", "name_en": "Al-Haaqqa", "name_en_translation": "The Reality", "type": "Meccan"},
        {"number": 70, "name_ar": "سورة المعارج", "name_en": "Al-Ma'aarij", "name_en_translation": "The Ascending Stairways", "type": "Meccan"},
        {"number": 71, "name_ar": "سورة نوح", "name_en": "Nooh", "name_en_translation": "Noah", "type": "Meccan"},
        {"number": 72, "name_ar": "سورة الجن", "name_en": "Al-Jinn", "name_en_translation": "The Jinn", "type": "Meccan"},
        {"number": 73, "name_ar": "سورة المزمل", "name_en": "Al-Muzzammil", "name_en_translation": "The Enshrouded One", "type": "Meccan"},
        {"number": 74, "name_ar": "سورة المدثر", "name_en": "Al-Muddaththir", "name_en_translation": "The Cloaked One", "type": "Meccan"},
        {"number": 75, "name_ar": "سورة القيامة", "name_en": "Al-Qiyaama", "name_en_translation": "The Resurrection", "type": "Meccan"},
        {"number": 76, "name_ar": "سورة الإنسان", "name_en": "Al-Insaan", "name_en_translation": "Man", "type": "Medinan"},
        {"number": 77, "name_ar": "سورة المرسلات", "name_en": "Al-Mursalaat", "name_en_translation": "The Emissaries", "type": "Meccan"},
        {"number": 78, "name_ar": "سورة النبأ", "name_en": "An-Naba", "name_en_translation": "The Announcement", "type": "Meccan"},
        {"number": 79, "name_ar": "سورة النازعات", "name_en": "An-Naazi'aat", "name_en_translation": "Those who drag forth", "type": "Meccan"},
        {"number": 80, "name_ar": "سورة عبس", "name_en": "Abasa", "name_en_translation": "He frowned", "type": "Meccan"},
        {"number": 81, "name_ar": "سورة التكوير", "name_en": "At-Takwir", "name_en_translation": "The Overthrowing", "type": "Meccan"},
        {"number": 82, "name_ar": "سورة الإنفطار", "name_en": "Al-Infitaar", "name_en_translation": "The Cleaving", "type": "Meccan"},
        {"number": 83, "name_ar": "سورة المطففين", "name_en": "Al-Mutaffifin", "name_en_translation": "Defrauding", "type": "Meccan"},
        {"number": 84, "name_ar": "سورة الإنشقاق", "name_en": "Al-Inshiqaaq", "name_en_translation": "The Splitting Open", "type": "Meccan"},
        {"number": 85, "name_ar": "سورة البروج", "name_en": "Al-Burooj", "name_en_translation": "The Constellations", "type": "Meccan"},
        {"number": 86, "name_ar": "سورة الطارق", "name_en": "At-Taariq", "name_en_translation": "The Morning Star", "type": "Meccan"},
        {"number": 87, "name_ar": "سورة الأعلى", "name_en": "Al-A'laa", "name_en_translation": "The Most High", "type": "Meccan"},
        {"number": 88, "name_ar": "سورة الغاشية", "name_en": "Al-Ghaashiya", "name_en_translation": "The Overwhelming", "type": "Meccan"},
        {"number": 89, "name_ar": "سورة الفجر", "name_en": "Al-Fajr", "name_en_translation": "The Dawn", "type": "Meccan"},
        {"number": 90, "name_ar": "سورة البلد", "name_en": "Al-Balad", "name_en_translation": "The City", "type": "Meccan"},
        {"number": 91, "name_ar": "سورة الشمس", "name_en": "Ash-Shams", "name_en_translation": "The Sun", "type": "Meccan"},
        {"number": 92, "name_ar": "سورة الليل", "name_en": "Al-Layl", "name_en_translation": "The Night", "type": "Meccan"},
        {"number": 93, "name_ar": "سورة الضحى", "name_en": "Ad-Dhuhaa", "name_en_translation": "The Morning Hours", "type": "Meccan"},
        {"number": 94, "name_ar": "سورة الشرح", "name_en": "Ash-Sharh", "name_en_translation": "The Consolation", "type": "Meccan"},
        {"number": 95, "name_ar": "سورة التين", "name_en": "At-Tin", "name_en_translation": "The Fig", "type": "Meccan"},
        {"number": 96, "name_ar": "سورة العلق", "name_en": "Al-Alaq", "name_en_translation": "The Clot", "type": "Meccan"},
        {"number": 97, "name_ar": "سورة القدر", "name_en": "Al-Qadr", "name_en_translation": "The Power", "type": "Meccan"},
        {"number": 98, "name_ar": "سورة البينة", "name_en": "Al-Bayyina", "name_en_translation": "The Evidence", "type": "Medinan"},
        {"number": 99, "name_ar": "سورة الزلزلة", "name_en": "Az-Zalzala", "name_en_translation": "The Earthquake", "type": "Medinan"},
        {"number": 100, "name_ar": "سورة العاديات", "name_en": "Al-Aadiyaat", "name_en_translation": "The Chargers", "type": "Meccan"},
        {"number": 101, "name_ar": "سورة القارعة", "name_en": "Al-Qaari'a", "name_en_translation": "The Calamity", "type": "Meccan"},
        {"number": 102, "name_ar": "سورة التكاثر", "name_en": "At-Takaathur", "name_en_translation": "Competition", "type": "Meccan"},
        {"number": 103, "name_ar": "سورة العصر", "name_en": "Al-Asr", "name_en_translation": "The Declining Day", "type": "Meccan"},
        {"number": 104, "name_ar": "سورة الهمزة", "name_en": "Al-Humaza", "name_en_translation": "The Traducer", "type": "Meccan"},
        {"number": 105, "name_ar": "سورة الفيل", "name_en": "Al-Fil", "name_en_translation": "The Elephant", "type": "Meccan"},
        {"number": 106, "name_ar": "سورة قريش", "name_en": "Quraish", "name_en_translation": "Qureish", "type": "Meccan"},
        {"number": 107, "name_ar": "سورة الماعون", "name_en": "Al-Maa'un", "name_en_translation": "Almsgiving", "type": "Meccan"},
        {"number": 108, "name_ar": "سورة الكوثر", "name_en": "Al-Kawthar", "name_en_translation": "Abundance", "type": "Meccan"},
        {"number": 109, "name_ar": "سورة الكافرون", "name_en": "Al-Kaafiroon", "name_en_translation": "The Disbelievers", "type": "Meccan"},
        {"number": 110, "name_ar": "سورة النصر", "name_en": "An-Nasr", "name_en_translation": "Divine Support", "type": "Medinan"},
        {"number": 111, "name_ar": "سورة المسد", "name_en": "Al-Masad", "name_en_translation": "The Palm Fibre", "type": "Meccan"},
        {"number": 112, "name_ar": "سورة الإخلاص", "name_en": "Al-Ikhlaas", "name_en_translation": "Sincerity", "type": "Meccan"},
        {"number": 113, "name_ar": "سورة الفلق", "name_en": "Al-Falaq", "name_en_translation": "The Dawn", "type": "Meccan"},
        {"number": 114, "name_ar": "سورة الناس", "name_en": "An-Naas", "name_en_translation": "Mankind", "type": "Meccan"},
    ]
    
    frappe.msgprint("Importing Surahs...")
    for surah_data in surahs:
        if not frappe.db.exists("Surah", surah_data["name_en"]):
            doc = frappe.get_doc({
                "doctype": "Surah",
                "number": surah_data["number"],
                "name_ar": surah_data["name_ar"],
                "name_en": surah_data["name_en"],
                "name_en_translation": surah_data["name_en_translation"],
                "type": surah_data["type"]
            })
            doc.insert(ignore_permissions=True)
    
    frappe.db.commit()
    frappe.msgprint(f"Imported {len(surahs)} Surahs successfully!")
