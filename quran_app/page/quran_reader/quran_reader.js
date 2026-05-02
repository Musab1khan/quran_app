// Quran Reader Page - Auto-loaded by Frappe based on page name
class QuranReader {
    constructor(page) {
        console.log('QuranReader: Constructor called');
        this.page = page;
        this.current_surah = null;
        this.current_ayah = 1;
        this.reading_start = null; // Track reading session start
        this.reading_mode = 'book'; // 'book' or 'single'
        this.ayahs_per_page = 10; // Book mode ayahs per page
        this.make();
        this.load_surahs();
        console.log('QuranReader: Constructor complete');
    }
    
    make() {
        // Create layout
        let html = `
            <div class="quran-reader">
                <div class="row quran-layout">
                    <div class="col-sidebar">
                        <div class="sidebar">
                            <div class="search-box mb-2">
                                <input type="text" class="form-control" id="search-ayah" 
                                    placeholder="Search ayahs...">
                                <button class="btn btn-primary btn-sm mt-2 w-100" id="search-btn">
                                    <i class="fa fa-search"></i> Search
                                </button>
                            </div>
                            <div class="reading-session-box mb-2 p-2 bg-light rounded">
                                <button class="btn btn-success btn-sm w-100 mb-2" id="start-reading-btn">
                                    <i class="fa fa-play"></i> Start Reading
                                </button>
                                <button class="btn btn-warning btn-sm w-100" id="bookmark-btn" disabled>
                                    <i class="fa fa-bookmark"></i> Bookmark Reading
                                </button>
                                <div id="reading-status" class="text-center mt-2" style="font-size: 11px; display: none;">
                                    <span class="text-muted">Reading from: <b id="start-pos"></b></span>
                                </div>
                            </div>
                            <div class="surah-list">
                                <h6>Surahs</h6>
                                <div id="surah-list" class="list-group"></div>
                            </div>
                        </div>
                    </div>
                    <div class="col-content">
                        <div class="main-content">
                            <div class="reading-controls mb-3">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div class="btn-group">
                                        <button class="btn btn-outline-secondary btn-sm" id="prev-ayah">
                                            <i class="fa fa-chevron-left"></i> Previous
                                        </button>
                                        <button class="btn btn-outline-secondary btn-sm" id="next-ayah">
                                            Next <i class="fa fa-chevron-right"></i>
                                        </button>
                                    </div>
                                    <div class="reading-modes">
                                        <div class="btn-group btn-group-sm">
                                            <button class="btn btn-outline-primary active" id="book-mode" title="Book Mode">
                                                <i class="fa fa-book"></i> Book
                                            </button>
                                            <button class="btn btn-outline-primary" id="single-ayah-mode" title="Single Ayah">
                                                <i class="fa fa-align-center"></i> Single
                                            </button>
                                        </div>
                                    </div>
                                    <span id="current-position" class="mx-3 text-muted fw-bold"></span>
                                </div>
                            </div>
                            <div id="ayah-display" class="ayah-display"></div>
                            <div id="search-results" class="search-results d-none"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        console.log('QuranReader: About to inject HTML, page.body =', this.page.body);
        console.log('QuranReader: HTML length =', html.length);
        $(this.page.body).html(html);
        console.log('QuranReader: HTML injected, checking...', $('.quran-reader').length);
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
        
        // Start Reading Session
        $('#start-reading-btn').on('click', function() {
            me.start_reading_session();
        });
        
        // Bookmark Reading
        $('#bookmark-btn').on('click', function() {
            me.bookmark_reading();
        });
        
        // Reading Mode Switch
        $('#book-mode').on('click', function() {
            me.switch_reading_mode('book');
        });
        
        $('#single-ayah-mode').on('click', function() {
            me.switch_reading_mode('single');
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
    
    start_reading_session() {
        if (!this.current_surah) {
            frappe.msgprint('Please select a Surah first');
            return;
        }
        
        this.reading_start = {
            surah: this.current_surah,
            ayah: this.current_ayah
        };
        
        // Update UI
        $('#start-reading-btn').html('<i class="fa fa-check"></i> Reading...').removeClass('btn-success').addClass('btn-info');
        $('#bookmark-btn').prop('disabled', false);
        $('#reading-status').show();
        $('#start-pos').text(this.current_surah + ':' + this.current_ayah);
        
        frappe.show_alert({
            message: 'Reading session started from ' + this.current_surah + ':' + this.current_ayah,
            indicator: 'green'
        });
    }
    
    bookmark_reading() {
        if (!this.reading_start) {
            frappe.msgprint('Please start a reading session first');
            return;
        }
        
        if (!this.current_surah || !this.current_ayah) {
            frappe.msgprint('Please navigate to an ayah first');
            return;
        }
        
        let me = this;
        frappe.call({
            method: 'quran_app.api.quran.create_daily_reading',
            args: {
                start_surah: this.reading_start.surah,
                start_ayah: this.reading_start.ayah,
                end_surah: this.current_surah,
                end_ayah: this.current_ayah
            },
            callback: function(r) {
                if (r.message) {
                    // Reset UI
                    me.reading_start = null;
                    $('#start-reading-btn').html('<i class="fa fa-play"></i> Start Reading').removeClass('btn-info').addClass('btn-success');
                    $('#bookmark-btn').prop('disabled', true);
                    $('#reading-status').hide();
                    
                    frappe.show_alert({
                        message: 'Reading bookmarked successfully!',
                        indicator: 'green'
                    });
                    
                    // Ask if user wants to view the Daily Reading record
                    frappe.confirm(
                        'View your reading log?',
                        () => frappe.set_route('List', 'Daily Reading')
                    );
                }
            }
        });
    }
    
    switch_reading_mode(mode) {
        this.reading_mode = mode;
        
        // Update button states
        $('#book-mode').toggleClass('active', mode === 'book');
        $('#single-ayah-mode').toggleClass('active', mode === 'single');
        
        // Reload ayahs with new mode
        if (this.current_surah) {
            this.load_surah_ayahs(this.current_surah, this.current_ayah);
        }
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
                                <h6 class="mb-1">${surah.name}. ${surah.name_en || 'Unknown'}</h6>
                                <small>${surah.total_ayahs || 0} ayahs</small>
                            </div>
                            <p class="mb-1">${surah.name_ar || ''}</p>
                            <small>${surah.type || ''}</small>
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
        
        let limit = this.reading_mode === 'single' ? 1 : this.ayahs_per_page;
        
        frappe.call({
            method: 'quran_app.api.quran.get_surah_ayahs',
            args: {
                surah: surah,
                start_ayah: start_ayah,
                limit: limit
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
        let first_ayah = null;
        
        if (this.reading_mode === 'single') {
            // Single Ayah Mode - show only current ayah
            let current_ayah_data = ayahs.find(ayah => ayah.number_in_surah == this.current_ayah);
            if (current_ayah_data) {
                first_ayah = current_ayah_data;
                html += `
                    <div class="book-page single-ayah">
                        <div class="ayah-card text-center">
                            <div class="ayah-header mb-4">
                                <span class="badge badge-primary fs-6">${current_ayah_data.surah} : ${current_ayah_data.number_in_surah}</span>
                                <span class="badge badge-secondary ms-2">Page ${current_ayah_data.page}</span>
                            </div>
                            <div class="arabic-text quran-font mb-4" dir="rtl">
                                <h2 class="mb-3">${current_ayah_data.text_arabic}</h2>
                            </div>
                            <div class="translation-text">
                                <p class="fs-5 text-muted fst-italic">${current_ayah_data.text_translation || 'No translation available'}</p>
                            </div>
                        </div>
                    </div>
                `;
            }
        } else {
            // Book Mode - show multiple ayahs like a book page
            html += '<div class="book-page">';
            ayahs.forEach((ayah, index) => {
                if (index === 0) first_ayah = ayah;
                html += `
                    <div class="book-ayah" data-surah="${ayah.surah}" data-ayah="${ayah.number_in_surah}">
                        <div class="ayah-header mb-2">
                            <span class="ayah-number-mark">${ayah.number_in_surah}</span>
                            <span class="badge badge-light">${ayah.surah}:${ayah.number_in_surah}</span>
                        </div>
                        <div class="arabic-text quran-font mb-3" dir="rtl">
                            <h4>${ayah.text_arabic}</h4>
                        </div>
                        <div class="translation-text">
                            <p class="text-muted">${ayah.text_translation || 'No translation available'}</p>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
        }
        
        $('#ayah-display').html(html);
        $('#search-results').addClass('d-none');
        
        // Update current position display
        if (first_ayah) {
            this.current_ayah = first_ayah.number_in_surah;
            $('#current-position').text(`${first_ayah.surah} : ${first_ayah.number_in_surah}`);
        }
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

// Initialize when page is loaded by Frappe
(function() {
    console.log('Quran Reader: Script loaded');
    
    function init_page() {
        console.log('Quran Reader: Trying to init, frappe.pages =', frappe.pages);
        // Wait for frappe.page to be available
        if (frappe.pages && frappe.pages['quran-reader']) {
            console.log('Quran Reader: Page found!');
            var page = frappe.pages['quran-reader'];
            if (!page.quran_reader_initialized) {
                page.quran_reader_initialized = true;
                page.quran_reader = new QuranReader(page);
                console.log('Quran Reader: Initialized!');
            } else {
                console.log('Quran Reader: Already initialized');
            }
        } else {
            console.log('Quran Reader: Page not found yet');
        }
    }
    
    // Try immediately and after delay
    init_page();
    setTimeout(init_page, 500);
    setTimeout(init_page, 1000);
    setTimeout(init_page, 2000);
})();
