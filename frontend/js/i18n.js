/**
 * NASA FIRE-X Internationalization (i18n) Engine
 * Seamless switching between English (EN) and Azerbaijani (AZ)
 */

class I18nEngine {
  constructor() {
    this.currentLanguage = localStorage.getItem('firex_lang') || 'en';
    this.translations = {};
    this.listeners = [];
  }

  async init() {
    try {
      const [enRes, azRes] = await Promise.all([
        fetch('/static/locales/en.json').then(r => r.json()).catch(() => null),
        fetch('/static/locales/az.json').then(r => r.json()).catch(() => null)
      ]);

      if (enRes) this.translations['en'] = enRes;
      if (azRes) this.translations['az'] = azRes;

      // Fallback if not loaded via static path
      if (!this.translations['en'] || !this.translations['az']) {
        const [enRes2, azRes2] = await Promise.all([
          fetch('/locales/en.json').then(r => r.json()).catch(() => null),
          fetch('/locales/az.json').then(r => r.json()).catch(() => null)
        ]);
        if (enRes2) this.translations['en'] = enRes2;
        if (azRes2) this.translations['az'] = azRes2;
      }
    } catch (e) {
      console.warn("Could not load external locale files, using fallback dictionary", e);
    }

    this.applyTranslations();
  }

  t(path, params = {}) {
    const langDict = this.translations[this.currentLanguage] || this.translations['en'] || {};
    const keys = path.split('.');
    let val = langDict;

    for (const k of keys) {
      if (val && typeof val === 'object' && k in val) {
        val = val[k];
      } else {
        val = null;
        break;
      }
    }

    if (!val) {
      // Fallback to English dictionary
      let fallbackVal = this.translations['en'];
      for (const k of keys) {
        if (fallbackVal && typeof fallbackVal === 'object' && k in fallbackVal) {
          fallbackVal = fallbackVal[k];
        } else {
          fallbackVal = path;
          break;
        }
      }
      val = fallbackVal || path;
    }

    if (typeof val === 'string') {
      for (const [pKey, pVal] of Object.entries(params)) {
        val = val.replace(new RegExp(`{{${pKey}}}`, 'g'), pVal);
      }
    }

    return val;
  }

  setLanguage(lang) {
    if (lang !== 'en' && lang !== 'az') lang = 'en';
    this.currentLanguage = lang;
    localStorage.setItem('firex_lang', lang);
    this.applyTranslations();
    this.notifyListeners();
  }

  toggleLanguage() {
    const nextLang = this.currentLanguage === 'en' ? 'az' : 'en';
    this.setLanguage(nextLang);
    return nextLang;
  }

  applyTranslations() {
    // Update all text nodes with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = this.t(key);
      if (translation && typeof translation === 'string') {
        el.textContent = translation;
      }
    });

    // Update placeholders with data-i18n-placeholder attribute
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      const translation = this.t(key);
      if (translation && typeof translation === 'string') {
        el.setAttribute('placeholder', translation);
      }
    });

    // Update language switcher UI indicator
    const langBtnText = document.getElementById('current-lang-text');
    if (langBtnText) {
      langBtnText.textContent = this.currentLanguage === 'en' ? 'EN' : 'AZ';
    }
  }

  onLanguageChange(callback) {
    this.listeners.push(callback);
  }

  notifyListeners() {
    this.listeners.forEach(cb => {
      try { cb(this.currentLanguage); } catch (e) { console.error(e); }
    });
  }
}

window.i18n = new I18nEngine();
