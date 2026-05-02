frappe.pages.on('quran-reader', function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Quran Reader',
        single_column: false
    });
    
    new QuranReader(page);
});

class QuranReader {
    constructor(page) {
        this.page = page;
        this.make();
        this.load_surahs();
    }
    
    make() {
        // Create layout
        let html = `
            <div class="quran-reader">
                <div class="row">
                    <div class="col-md-3">
                        <div class="sidebar">
                            <div class="search-box mb-3">
                                <input type="text" class="form-control" id="search-ayah" 
                                    placeholder="Search ayahs...">
                                <button class="btn btn-primary btn-sm mt-2" id="search-btn">
                                    Search
                                </button>
                            </div>
                            <div class="surah-list">
                                <h6>Surahs</h6>
                                <div id="surah-list" class="list-group"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-9">
                        <div class="main-content">
                            <div class="reading-controls mb-3">
                                <div class="btn-group">
                                    <button class="btn btn-outline-secondary btn-sm" id="prev-ayah">
                                        ← Previous
                                    </button>
                                    <button class="btn btn-outline-secondary btn-sm" id="next-ayah">
                                        Next →
                                    </button>
                                </div>
                                <button class="btn btn-success btn-sm float-right" id="mark-read">
                                    Mark as Read
                                </button>
                            </div>
                            <div id="ayah-display" class="ayah-display"></div>
                            <div id="search-results" class="search-results d-none"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        $(this.page.body).html(html);
        this.bind_events();
    }
    
    bind_events() {
        let me = this;
        
        $('#search-btn').on('click', function() {
            me.search_ayahs();
        });
        
        $('#search-ayah').on('keypress', function(e) {
            if (e.which === 13) me.search_ayahs();
        });
        
        $('#prev-ayah').on('click', function() {
            me.navigate_ayah(-1);
        });
        
        $('#next-ayah').on('click', function() {
            me.navigate_ayah(1);
        });
        
        $('#mark-read').on('click', function() {
            me.mark_as_read();
        });
        
        $(document).on('click', '.surah-item', function() {
            let surah = $(this).data('surah');
            me.load_surah_ayahs(surah);
        });
        
        $(document).on('click', '.ayah-result', function() {
            let surah = $(this).data('surah');
            let ayah = $(this).data('ayah');
            me.load_specific_ayah(surah, ayah);
        });
    }
    
    load_surahs() {
        let me = this;
        frappe.call({
            method: 'quran_app.api.quran.get_surah_list',
            callback: function(r) {
                if (r.message) {
                    let html = '';
                    r.message.forEach(surah => {
                        html += `<a href="#" class="list-group-item list-group-item-action surah-item" 
                            data-surah="${surah.name}">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">${surah.number}. ${surah.name_en}</h6>
                                <small>${surah.ayah_count} ayahs</small>
                            </div>
                            <p class="mb-1">${surah.name_ar}</p>
                            <small>${surah.type}</small>
                        </a>`;
                    });
                    $('#surah-list').html(html);
                }
            }
        });
    }
    
    load_surah_ayahs(surah, start_ayah=1) {
        let me = this;
        this.current_surah = surah;
        this.current_ayah = start_ayah;
        
        frappe.call({
            method: 'quran_app.api.quran.get_ayahs_by_surah',
            args: {
                surah: surah,
                start_ayah: start_ayah,
                end_ayah: start_ayah + 9
            },
            callback: function(r) {
                if (r.message) {
                    me.display_ayahs(r.message);
                }
            }
        });
    }
    
    display_ayahs(ayahs) {
        let html = '';
        ayahs.forEach(ayah => {
            html += `
                <div class="ayah-card mb-4 p-3 border rounded" data-surah="${ayah.surah}" data-ayah="${ayah.number_in_surah}">
                    <div class="ayah-header mb-2">
                        <span class="badge badge-info">${ayah.surah} : ${ayah.number_in_surah}</span>
                        <span class="badge badge-secondary">Page ${ayah.page}</span>
                    </div>
                    <div class="arabic-text text-right mb-3" dir="rtl">
                        <h4>${ayah.text_arabic}</h4>
                    </div>
                    <div class="translation-text">
                        <p class="text-muted">${ayah.text_translation || 'No translation available'}</p>
                    </div>
                </div>
            `;
        });
        $('#ayah-display').html(html);
        $('#search-results').addClass('d-none');
    }
    
    search_ayahs() {
        let search_text = $('#search-ayah').val();
        if (!search_text) return;
        
        let me = this;
        frappe.call({
            method: 'quran_app.api.quran.search_ayahs',
            args: {
                search_text: search_text,
                limit: 20
            },
            callback: function(r) {
                if (r.message) {
                    me.display_search_results(r.message);
                }
            }
        });
    }
    
    display_search_results(ayahs) {
        let html = '<h5>Search Results</h5>';
        if (ayahs.length === 0) {
            html += '<p class="text-muted">No results found</p>';
        } else {
            ayahs.forEach(ayah => {
                html += `
                    <div class="ayah-result p-2 border-bottom cursor-pointer" 
                        data-surah="${ayah.surah}" data-ayah="${ayah.number_in_surah}">
                        <div class="d-flex justify-content-between">
                            <strong>${ayah.surah} : ${ayah.number_in_surah}</strong>
                            <small>Page ${ayah.page}</small>
                        </div>
                        <div class="text-right" dir="rtl">${ayah.text_arabic.substring(0, 100)}...</div>
                    </div>
                `;
            });
        }
        $('#search-results').html(html).removeClass('d-none');
        $('#ayah-display').empty();
    }
    
    navigate_ayah(direction) {
        if (!this.current_surah) return;
        
        let new_ayah = this.current_ayah + direction;
        if (new_ayah < 1) new_ayah = 1;
        
        this.load_surah_ayahs(this.current_surah, new_ayah);
    }
    
    load_specific_ayah(surah, ayah) {
        this.load_surah_ayahs(surah, ayah);
    }
    
    mark_as_read() {
        if (!this.current_surah || !this.current_ayah) {
            frappe.msgprint('Please select an ayah first');
            return;
        }
        
        frappe.call({
            method: 'quran_app.api.quran.create_daily_reading',
            args: {
                start_surah: this.current_surah,
                start_ayah: this.current_ayah,
                end_surah: this.current_surah,
                end_ayah: this.current_ayah
            },
            callback: function(r) {
                if (r.message) {
                    frappe.show_alert({
                        message: 'Reading marked successfully!',
                        indicator: 'green'
                    });
                }
            }
        });
    }
}
