import frappe
import re
import json

# Path to the SQL file
sql_file = "/home/ibni-wali/frappe-bench/apps/quran_app_installer/quran.sql"

def parse_sql_insert_values(sql_content):
    """Extract values from SQL INSERT statements"""
    # Find all INSERT INTO `ayahs` statements
    insert_pattern = r"INSERT INTO `ayahs` \([^)]+\) VALUES\s*(.+?)(?:;|INSERT INTO|CREATE TABLE)"
    matches = re.findall(insert_pattern, sql_content, re.DOTALL)
    
    all_values = []
    for match in matches:
        # Split by ) , ( to get individual rows
        rows = re.split(r'\),\s*\(', match.strip())
        for row in rows:
            # Clean up
            row = row.strip()
            if row.startswith('('):
                row = row[1:]
            if row.endswith(')'):
                row = row[:-1]
            if row:
                all_values.append(row)
    
    return all_values

def parse_row(row_str):
    """Parse a single row from SQL VALUES"""
    try:
        # Split by comma, but be careful with quoted strings
        values = []
        current = ""
        in_quote = False
        quote_char = None
        
        i = 0
        while i < len(row_str):
            char = row_str[i]
            
            if char in ("'", '"') and (i == 0 or row_str[i-1] != '\\'):
                if not in_quote:
                    in_quote = True
                    quote_char = char
                    i += 1
                    continue
                elif quote_char == char:
                    in_quote = False
                    quote_char = None
                    i += 1
                    continue
            
            if char == ',' and not in_quote:
                values.append(current.strip())
                current = ""
                i += 1
                continue
            
            current += char
            i += 1
        
        if current.strip():
            values.append(current.strip())
        
        return values
    except Exception as e:
        print(f"Error parsing row: {e}")
        return None

def import_ayahs_from_sql():
    print("Reading SQL file...")
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Parsing SQL INSERT statements...")
    # Find all INSERT INTO ayahs statements
    insert_pattern = r"INSERT INTO `ayahs` \([^)]+\) VALUES\s*(.+?)(?:;|INSERT INTO|CREATE TABLE)"
    matches = re.findall(insert_pattern, content, re.DOTALL)
    
    print(f"Found {len(matches)} INSERT statements")
    
    total_imported = 0
    
    # Get existing surah mapping
    surahs = frappe.get_all("Surah", fields=["name", "number"])
    surah_map = {s.number: s.name for s in surahs}
    
    print(f"Found {len(surahs)} surahs in database")
    
    for idx, match in enumerate(matches):
        print(f"Processing INSERT statement {idx + 1}/{len(matches)}...")
        
        # Extract rows - handle the multi-row VALUES format
        values_str = match.strip()
        
        # Parse individual rows
        # The pattern is: (val1, val2, 'val3', ...), (val1, val2, ...)
        rows = []
        depth = 0
        current_row = ""
        in_string = False
        string_char = None
        
        for char in values_str:
            if char in ("'", '"') and (not current_row or current_row[-1] != '\\'):
                if not in_string:
                    in_string = True
                    string_char = char
                elif string_char == char:
                    in_string = False
                    string_char = None
            
            if char == '(' and not in_string:
                if depth == 0:
                    current_row = ""
                depth += 1
            elif char == ')' and not in_string:
                depth -= 1
                if depth == 0:
                    rows.append(current_row)
                    current_row = ""
            elif depth > 0:
                current_row += char
        
        print(f"  Found {len(rows)} rows in this statement")
        
        for row_idx, row in enumerate(rows):
            if row_idx % 100 == 0:
                print(f"    Processing row {row_idx}/{len(rows)}...")
            
            values = parse_row(row)
            if not values or len(values) < 9:
                continue
            
            try:
                # Extract values based on column order:
                # id, number, text, number_in_surah, page, surah_id, hizb_id, juz_id, sajda, created_at, updated_at
                ayah_id = int(values[0])
                ayah_number = int(values[1])
                text_arabic = values[2].strip("'") if values[2].startswith("'") else values[2]
                number_in_surah = int(values[3])
                page = int(values[4])
                surah_id = int(values[5])
                juz = int(values[7])
                
                # Find surah name
                surah_name = surah_map.get(surah_id)
                if not surah_name:
                    print(f"    Warning: Surah {surah_id} not found")
                    continue
                
                # Check if ayah already exists
                existing = frappe.db.exists("Ayah", {
                    "surah": surah_name,
                    "number_in_surah": number_in_surah
                })
                
                if existing:
                    continue
                
                # Create ayah document
                doc = frappe.get_doc({
                    "doctype": "Ayah",
                    "surah": surah_name,
                    "number": ayah_number,
                    "number_in_surah": number_in_surah,
                    "text_arabic": text_arabic,
                    "page": page,
                    "juz": juz
                })
                doc.insert(ignore_permissions=True, ignore_if_duplicate=True)
                total_imported += 1
                
            except Exception as e:
                print(f"    Error processing row {row_idx}: {e}")
                continue
        
        frappe.db.commit()
        print(f"  Imported {total_imported} ayahs so far")
    
    print(f"Total ayahs imported: {total_imported}")
    return total_imported

import_ayahs_from_sql()
