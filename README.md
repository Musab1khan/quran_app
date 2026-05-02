# Quran App

A beautiful Quran reading and search application built on the Frappe framework.

> **Made with love by Umair Wali for his father's (abu) sawab**

---

## Features

- **Complete Surah List** - Browse all 114 Surahs with Arabic and English names
- **Multiple Reading Modes**
  - *Book Mode*: Read multiple ayahs at once like a book
  - *Single Mode*: Focus on one ayah at a time
- **Search Ayahs** - Search through the entire Quran
- **Bookmark Reading** - Save your daily reading progress
- **Responsive Design** - Works on desktop and mobile
- **Navigation Controls** - Previous/Next buttons for easy browsing
- **Daily Reading Tracker** - Track your reading sessions

---

## Installation

### Prerequisites
- Frappe Framework (v14 or v15)
- Python 3.10+
- MariaDB/MySQL

### Using Bench CLI

```bash
# Get the app from the repository
cd /path/to/your/frappe-bench
bench get-app https://github.com/Musabikhan/quran_app.git --branch main

# Install the app on your site
bench --site your-site.local install-app quran_app

# Migrate and clear cache
bench --site your-site.local migrate
bench --site your-site.local clear-cache
bench restart
```

### Post-Installation

1. **Setup the data**: 
   - Go to Surah doctype and add your Surah data
   - Go to Ayah doctype and add ayah content
   - Or import data using the Data Import tool

2. **Access the Quran Reader**:
   - Visit: `http://your-site.local/quran-reader`
   - Or search "Quran Reader" in the Frappe desk search bar

---

## Usage

### Reading the Quran
1. Open the Quran Reader page
2. Select a Surah from the left sidebar
3. Choose your preferred reading mode (Book or Single)
4. Navigate using Previous/Next buttons

### Searching
1. Enter a keyword in the search box
2. Click "Search" or press Enter
3. Click on any result to jump to that ayah

### Bookmarking
1. Click "Start Reading" to begin a session
2. Read through the ayahs
3. Click "Bookmark Reading" to save your progress
4. The reading will be recorded in the Daily Reading doctype

---

## Architecture

### DocTypes
- **Surah** - Stores Surah information (name, number, type, ayah count)
- **Ayah** - Stores individual ayahs with Arabic text and translations
- **Daily Reading** - Tracks user reading sessions

### Pages
- **quran-reader** - Main reading interface

### API
- `quran_app.api.quran.get_surah_list` - Fetch all surahs
- `quran_app.api.quran.get_ayahs_by_surah` - Fetch ayahs for a specific surah
- `quran_app.api.quran.search_ayahs` - Search through ayahs
- `quran_app.api.quran.create_daily_reading` - Create reading records

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

This app uses `pre-commit` for code formatting:

```bash
cd apps/quran_app
pre-commit install
```

Pre-commit tools:
- ruff (Python linting)
- eslint (JavaScript)
- prettier (Formatting)

---

## Author

**Umair Wali**
- Email: umairwali6@gmail.com
- GitHub: [@umairwali](https://github.com/your-github)

This application is dedicated to my beloved father (abu). May Allah grant him the highest rank in Jannah. Ameen.

---

## License

MIT License - see [license.txt](license.txt) for details

---

## Acknowledgments

- **Quran data**: [Source of your Quran data]
- **Frappe Framework**: [https://frappeframework.com](https://frappeframework.com)
- **Translation**: [Source of translations if any]

---

*"Indeed, it is We who sent down the Qur'an, and indeed, We will be its guardian."* - Al-Hijr 15:9
