/**
 * NASA FIRE-X Universal Client-Side Controller & Complete Bilingual Engine
 * Seamlessly translates 100% of all 6 platform pages between English and Azerbaijani.
 */
(function() {
  'use strict';

  // --- COMPREHENSIVE AZERBAIJANI TRANSLATIONS ---
  const TRANSLATIONS_AZ = {
    // === COMMON NAVBAR ===
    nav: {
      brandSub: 'MİKROYERÇƏKİM YANMA İNTELLEKTİ',
      home: 'Ana Səhifə',
      analytics: 'Analitika',
      explorer: 'Məlumat Kəşfiyyatı',
      simulator: 'Simulyator',
      ai: 'AI Köməkçi',
      about: 'Haqqında',
      live: 'CANLI',
      aiBtn: 'AI Köməkçi'
    },

    // === COMMON FOOTER ===
    footer: {
      desc: 'Mikroyerçəkim Yanma Datalarından Süni İntellektlə Yanğın Təhlükəsizliyi İntellekti. NASA Space Apps Challenge 2026.',
      colPlatform: 'Platforma',
      colData: 'Məlumat Mənbələri',
      analytics: 'Analitika Mərkəzi',
      explorer: 'Məlumat Kəşfiyyatı',
      simulator: 'Missiya Simulyatoru',
      ai: 'AI Köməkçi',
      about: 'Sənədləşmə & Haqqında',
      copyright: '© 2026 NASA FIRE-X · NASA Space Apps Challenge üçün hazırlanıb',
      dataAttribution: 'Məlumat: NASA Physical Science Informatics (PSI) · 879 kanonik eksperiment'
    },

    // === 1. HOME PAGE (index.html) ===
    home: {
      badge: 'NASA SPACE APPS CHALLENGE 2026 \u00a0·\u00a0 KOSMOSDA YANĞIN TƏHLÜKƏSİZLİYİ',
      title: 'ALOV SƏRBƏST DÜŞMƏDƏ',
      subtitle: 'FIRE-X İntellekt Platforması',
      desc: 'AI tərəfindən təhlil edilmiş 879 yoxlanılmış mikroqravitasiya yanma eksperimenti — BKS, Artemis Ay Yaşayış Modulu və gələcək kosmik missiyalarda yanğın təhlükəsizliyini təmin edir.',
      btnExplore: 'Məlumatları Kəşf Et',
      btnSimulator: 'Simulyatoru Başlat',
      clockLabel: 'MİSSİYA VAXTI (UTC):',
      scroll: 'Aşağı',
      statExp: 'Kanonik Eksperimentlər',
      statFam: 'Uçuş Ailələri',
      statScen: 'Missiya Ssenariləri',
      statInt: 'Məlumat Dəqiqliyi',

      aboutEyebrow: 'Layihə Haqqında',
      aboutTitle: 'Orbitdə <span class="text-gradient">Yanğın Təhlükəsizliyi Elmi</span>',
      aboutDesc: 'FIRE-X NASA-nın ən əhatəli mikroyerçəkim yanma məlumat bazasını toplayır və təhlil edir. Qravitasiya olmadan alov tamamilə fərqli davranır — alov kürəvi forma alır, soyuq alovlar davam edir və ənənəvi yanğın təhlükəsizliyi qaydaları artıq tətbiq olunmur.',
      feat1Title: '879 Yoxlanılmış Eksperiment',
      feat1Desc: 'FLEX damcı alovlarından SAFFIRE böyük miqyaslı kosmik yanğın sınaqlarına qədər — hamısı NASA PSI rəsmi datalarıdır.',
      feat2Title: 'Süni İntellekt Analitikası',
      feat2Desc: 'Hallüsinasiyasız elmi cavablar üçün deterministik NASA datası ilə inteqrasiya edilmiş GPT-6-luna.',
      feat3Title: 'Missiya Ssenari Simulyatoru',
      feat3Desc: 'BKS, Artemis Ay Modulu (34% O₂) və Dərin Kosmos mühitlərində yanğın təhlükələrini modelləşdirin.',
      issBadgeTitle: 'Beynəlxalq Kosmik Stansiya',
      issBadgeSub: 'Orbit: 408 km | Sürət: 27,600 km/s',

      famEyebrow: 'Uçuş Tədqiqatları',
      famTitle: '24 <span class="text-gradient">Eksperiment Ailəsi</span>',
      famViewAll: 'Bütün Datalara Bax →',

      envEyebrow: 'Planetar Yanğın Riski',
      envTitle: 'Missiya <span class="text-gradient">Mühitləri</span>',
      envDesc: 'Alov hər bir kosmik gəmi atmosferində fərqli davranır. Oksigen faizi və kabin təzyiqi hər şeyi müəyyən edir.',

      modEyebrow: 'Platforma Modulları',
      modTitle: 'Platformanı <span class="text-gradient">Kəşf Edin</span>'
    },

    // === 2. ANALYTICS PAGE (analytics.html) ===
    analytics: {
      pageTitle: 'Yanma Analitikası Mərkəzi',
      pageDesc: '879 NASA eksperimentindən 3D elmi telemetriya',
      holoTitle: '3D/4D İNTERAKTİV YANMA HOLO-LABORATORİYASI',
      btnScatter: '4D SAÇILMA KUBİ',
      btnFlame: '3D KÜRƏVİ ALOV',
      btnDuct: '3D HAVA AXINI KANALI',
      btnReset: 'KAMERANI SIFIRLA',
      btnRotate: 'FIRLANMANI DƏYİŞ',
      kpiTotalLabel: 'UÇUŞ DATA NÖQTƏLƏRİ',
      kpiTempLabel: 'MÜŞAHİDƏ EDİLƏN TEMPERATUR',
      kpiRateLabel: 'ORTA YANMA SÜRƏTİ',
      kpiO2Label: 'ORTA OKSİGEN QATILIĞI',
      chart1Title: 'Alovun Sönmə Diametri vs. Oksigen Konsentrasiyası',
      chart1Desc: 'O₂ mol fraksiyasından asılı olaraq damcı və bərk yanacaq sönmə sərhədlərini qiymətləndirir',
      chart2Title: 'Yanma Müddəti vs. Məcburi Konvektiv Hava Axını',
      chart2Desc: 'Aşağı axında radiativ sönmə ilə yüksək axında konvektiv üfürülmə arasındakı keçidi təhlil edir',
      chart3Title: 'Yanacaq Alovlanma Matrisi & Nümunə Bölgüsü',
      chart3Desc: '879 uçuş eksperimentinin material kateqoriyası və kimyəvi tərkibinə görə bölgüsü',
      chart4Title: 'Sönmə Nəticələrinin Paylanması',
      chart4Desc: 'Orbital sınaq kampaniyalarında müşahidə olunan sönmə rejimlərinin təsnifatı',
      insight1Title: 'Soyuq Alov (Cool Flame) Sönmə Rejimləri',
      insight1Desc: 'FLEX-2 telemetriyası sübut edir ki, damcı yanması görünən alov söndükdən sonra belə ikinci dərəcəli aşağı temperaturlu (400-800 K) kimyəvi reaksiya rejimləri nümayiş etdirir.',
      insight2Title: 'Konvektiv Üfürmə Sürət Hədləri',
      insight2Desc: 'BASS-II və SAFFIRE nümayiş etdirir ki, zəif məcburi hava axınları (<5 sm/s) radiativ sönməyə səbəb olur, yüksək hava axınları (>20 sm/s) isə alovu üfürərək söndürür.',
      insight3Title: 'Oksigen Konsentrasiyası Alovlanma Sərhədi',
      insight3Desc: 'NASA-STD-6001 və SOFIE müəyyən edir ki, sakit mikroyerçəkimdə Məhdudlaşdırıcı Oksigen Qatılığı (LOC) əksər kosmik materiallar üçün ~14.5% səviyyəsinə düşür.'
    },

    // === 3. EXPLORER PAGE (explorer.html) ===
    explorer: {
      pageTitle: 'Eksperiment Məlumat Kəşfiyyatçısı',
      pageDesc: 'Tam fiziki telemetriyaya malik 879 uçuş qeydini filtrasiya edin, axtarın və təhlil edin',
      searchLabel: 'Açar Sözlə Axtarış',
      searchPlaceholder: 'Eksperiment ID, yanacaq (məs. Heptan, PMMA) və ya qeydlər üzrə axtarış...',
      familyLabel: 'Uçuş və Tədqiqat Ailəsi (Cəmi 24)',
      fuelLabel: 'Yanacaq / Material (106 Növ)',
      outcomeLabel: 'Sönmə Nəticəsi',
      o2RangeLabel: 'Minimum O₂ Konsentrasiyası',
      btnReset: 'Filtrləri Sıfırla',
      tableHeaderId: 'ID',
      tableHeaderFamily: 'UÇUŞ AİLƏSİ',
      tableHeaderFuel: 'YANACAQ / MATERİAL',
      tableHeaderO2: 'O₂ %',
      tableHeaderPressure: 'TƏZYİQ (kPa)',
      tableHeaderBurnTime: 'YANMA VAXTI (s)',
      tableHeaderDe: 'SÖNMƏ Dₑ (mm)',
      tableHeaderOutcome: 'NƏTİCƏ',
      tableHeaderActions: 'ƏMƏLİYYATLAR',
      btnInspect: 'Bax',
      btnCompare: '+ Müqayisə et',
      btnCompareActive: '✓ Seçildi',
      paginationPrev: 'Əvvəlki',
      paginationNext: 'Növbəti',
      dockTitle: 'Müqayisə Paneli',
      btnRunCompare: 'Müqayisəni Başlat',
      btnClearCompare: 'Təmizlə',
      drawerTitle: 'Telemetriya Müfəttişi',
      tabGeneral: 'Ümumi Məlumat',
      tabCombustion: 'Yanma Telemetriyası',
      tabAtmosphere: 'Atmosfer Şəraiti',
      btnAskAi: 'AI Köməkçi ilə Təhlil Et',
      btnCloseDrawer: 'Bağla'
    },

    // === 4. SIMULATOR PAGE (simulator.html) ===
    simulator: {
      pageTitle: 'Planetar Missiya Yanğın Riski Simulyatoru',
      pageDesc: 'Ay, Mars və fərdi kosmik atmosferlərdə alov dinamikasını və Yanğın Təhlükəsi İndeksini (FHI) simulyasiya edin',
      presetHeading: 'Atmosfer Ssenariləri',
      presetIssTitle: 'BKS Standartı',
      presetIssSub: 'Nominal orbital kabin mühiti',
      presetLunarTitle: 'Artemis Ay Modulu',
      presetLunarSub: '34% O₂ zənginləşdirilmiş kabin atmosferi',
      presetHypoxicTitle: 'Hipoqsik Sığınacaq',
      presetHypoxicSub: 'Fövqəladə yanğınsöndürmə və avtomatik boğma zonası',
      presetCustomTitle: 'Fərdi Tədqiqat Mühiti',
      presetCustomSub: 'İstifadəçi tərəfindən təyin olunan parametrlər',
      sliderO2Label: 'Oksigen Konsentrasiyası (O₂ %)',
      sliderPressureLabel: 'Kabin Təzyiqi (kPa)',
      btnAskAiSim: 'Bu Ssenarini AI ilə Təhlil Et',
      fhiHeading: 'Yanğın Təhlükəsi İndeksi (FHI)',
      badgeNominal: 'MÖTƏDİL RİSK',
      badgeElevated: 'YÜKSƏK TƏHLÜKƏ',
      badgeSuppressed: 'SÖNDÜRÜLMÜŞ MÜHİT',
      metricO2Title: 'Oksigen Qatılığı',
      metricPressureTitle: 'Kabin Təzyiqi',
      metricPo2Title: 'Qismən O₂ Təzyiqi (pO₂)',
      metricDeTitle: 'Təxmini Sönmə dₑ',
      metricBurnTitle: 'Yanma Sürəti Çoxaldıcısı',
      metricAgentTitle: 'Tövsiyə Edilən Söndürücü',
      advisoryHeading: 'NASA Uçuş Təhlükəsizliyi Məsləhəti',
      comparisonHeading: 'Ssenari Müqayisə Matrisi'
    },

    // === 5. AI ASSISTANT (ai.html) ===
    ai: {
      heading: 'TÖVSİYƏ OLUNAN ELMİ SUALLAR',
      chip1: 'FLEX-2 Soyuq Alov (Cool Flame) Kinetikası →',
      chip2: 'Artemis 34% O₂ Yanğın Riski →',
      chip3: 'Məcburi Hava Axını və Sönmə Hədləri →',
      chip4: 'SAFFIRE Kosmik Gəmi Yanğınları →',
      chip5: 'NASA-STD-6001 Söndürmə Qaydaları →',
      specEngine: 'AI MÜHƏRRİKİ: OpenAI Responses API',
      specModel: 'MODEL: gpt-6-luna',
      specContext: 'KONTEKST: 879 Kanonik Uçuş Sınağı',
      specLatency: 'GECİKMƏ: Real-vaxt yüksək sürət',
      welcomeTitle: 'FIRE-X Elmi Tədqiqat Köməkçisi Onlayndır',
      welcomeDesc: 'NASA Mikroyerçəkim Yanma İntellekt Konsoluna xoş gəlmisiniz. <strong>OpenAI GPT-6-luna</strong> ilə təchiz olunub və Beynəlxalq Kosmik Stansiya ilə Cygnus orbital sınaqlarından <strong>879 yoxlanılmış uçuş eksperimentinə</strong> əsaslanır.<br><br>Damcı sönməsi (FLEX), bərk yanacaqların alovlanması (BASS/SOFIE), kosmik gəmi yanğınlarının yayılması (SAFFIRE) və ya planetar yaşayış modullarının atmosfer təhlükəsizliyi (Artemis / BKS) haqqında ətraflı suallar verə bilərsiniz.',
      welcomeSource: 'NASA FİZİKİ ELMLƏR İNFORMATİKASI // GROUND TRUTH',
      welcomeStatus: 'SİSTEM HAZIRDIR',
      typingText: 'OpenAI gpt-6-luna və NASA PSI Telemetriyası sorğulanır...',
      placeholder: 'Mikroyerçəkimdə yanma, alov dinamikası və ya eksperiment ID-ləri haqqında soruşun...',
      btnSend: 'Sorğunu Göndər',
      btnClear: 'Sessiyanı Təmizlə',
      securityNote: 'MƏXFİ UÇUŞ DATALARI TƏHLÜKƏSİZ SERVER VASİTƏSİLƏ TƏHLİL OLUNUR',
      enterNote: 'GÖNDƏRMƏK ÜÇÜN ENTER BASIN'
    },

    // === 6. ABOUT PAGE (about.html) ===
    about: {
      eyebrow: 'Sənədləşmə & Mənbələr',
      pageTitle: 'FIRE-X <span class="text-gradient">Haqqında</span>',
      pageDesc: 'NASA Space Apps Challenge 2026 — Flame in Freefall: Mikroyerçəkim Yanma Datalarından AI Yanğın Təhlükəsizliyi İntellekti',
      sec1Eyebrow: 'Layihə İcmalı',
      sec1Title: 'FIRE-X Layihəsinin <span class="text-gradient">Elmi Əsasları</span>',
      card1Title: 'Niyə Mikroyerçəkim?',
      card1Desc: 'Mikroyerçəkimdə qravitasiya qaldırma qüvvəsi (buoyancy) yoxdur. Alovlar kürəvi forma alır. Soyuq alovlar davam edir. Standart yanğın təhlükəsizliyi modelləri işləmir. FIRE-X kosmik yaşayış modulları üçün yeni təhlükəsizlik modelləri hazırlamaq məqsədilə NASA-nın ən əhatəli mikroyerçəkim yanma bazasını təhlil edir.',
      card2Title: 'Məlumat Bazası',
      card2Desc: 'NASA Physical Science Informatics (PSI) repozitoriyasından 24 uçuş və tədqiqat ailəsi üzrə 879 kanonik eksperiment: FLEX-1/2 (damcı yanması), BASS-I/II (bərk materiallar), SAFFIRE I-VI (böyük miqyaslı gəmi yanğınları), ACME/CIR, SOFIE, SLICE və NASA-STD-6001 material sınaqları.',
      card3Title: 'Süni İntellekt İnteqrasiyası',
      card3Desc: 'Platforma ixtisaslaşdırılmış NASA yanma sistemi göstərişi ilə Responses API vasitəsilə OpenAI GPT-6-luna modelindən istifadə edir. Bütün AI çağırışları yalnız server tərəfində həyata keçirilir — API açarı heç vaxt brauzerə ötürülmür. Deterministik SQL+RAG ehtiyat sistemi cavabların həmişə real eksperimental datalara əsaslanmasını təmin edir.',
      card4Title: 'Missiya Simulyatoru',
      card4Desc: 'Yanğın Təhlükəsi İndeksi (FHI) formulu NASA-STD-6001 oksigen qismən təzyiqi və mol fraksiyası həssaslıq əyrilərindən əldə edilmişdir: FHI = 1 + (O₂/21) × 3.5 + (pO₂/21.3) × 1.8. BKS Standartı (FHI≈5.1), Artemis Kəşfiyyat Atmosferi (FHI≈8.3) və Hipoqsik Sığınacaq (FHI≈2.1) profillərinə qarşı təsdiqlənmişdir.',
      sec2Eyebrow: 'Məlumat Mənbələri',
      sec2Title: 'NASA <span class="text-gradient">Məlumat Mənbəyi</span>'
    }
  };

  /**
   * Translates the entire current page DOM based on active language
   */
  function applyLanguage(lang) {
    const isAz = (lang === 'az');

    // 1. Navbar Translation
    const navLinks = document.querySelectorAll('.nav-links .nav-link');
    if (navLinks.length >= 6) {
      navLinks[0].textContent = isAz ? TRANSLATIONS_AZ.nav.home : 'Home';
      navLinks[1].textContent = isAz ? TRANSLATIONS_AZ.nav.analytics : 'Analytics';
      navLinks[2].textContent = isAz ? TRANSLATIONS_AZ.nav.explorer : 'Data Explorer';
      navLinks[3].textContent = isAz ? TRANSLATIONS_AZ.nav.simulator : 'Simulator';
      navLinks[4].textContent = isAz ? TRANSLATIONS_AZ.nav.ai : 'AI Assistant';
      navLinks[5].textContent = isAz ? TRANSLATIONS_AZ.nav.about : 'About';
    }

    const brandSub = document.querySelector('.nav-brand-sub');
    if (brandSub) brandSub.textContent = isAz ? TRANSLATIONS_AZ.nav.brandSub : 'MICROGRAVITY COMBUSTION INTEL';

    const liveBadge = document.querySelector('.nav-actions div');
    if (liveBadge && liveBadge.textContent.includes('LIVE') || liveBadge && liveBadge.textContent.includes('CANLI')) {
      const dot = liveBadge.querySelector('.nav-status-dot');
      if (dot) {
        liveBadge.innerHTML = '';
        liveBadge.appendChild(dot);
        liveBadge.appendChild(document.createTextNode(isAz ? ' CANLI' : ' LIVE'));
      }
    }

    const navAiBtn = document.querySelector('.nav-ai-btn');
    if (navAiBtn) {
      const svg = navAiBtn.querySelector('svg');
      if (svg) {
        navAiBtn.innerHTML = '';
        navAiBtn.appendChild(svg);
        navAiBtn.appendChild(document.createTextNode(isAz ? ' AI Köməkçi' : ' AI Assistant'));
      }
    }

    // 2. Language Switcher Button Text
    const langBtn = document.getElementById('nav-lang-btn') || document.getElementById('lang-btn-ai');
    if (langBtn) langBtn.textContent = lang.toUpperCase();

    // 3. Footer Translation
    const footerDesc = document.querySelector('.footer p');
    if (footerDesc && footerDesc.textContent.includes('AI-Powered')) {
      if (isAz) footerDesc.textContent = TRANSLATIONS_AZ.footer.desc;
    }
    const footerColumns = document.querySelectorAll('.footer div > div > div:first-child');
    footerColumns.forEach(fc => {
      if (fc.textContent.trim() === 'PLATFORM' && isAz) fc.textContent = 'PLATFORMA';
      if (fc.textContent.trim() === 'DATA' && isAz) fc.textContent = 'MƏLUMAT';
    });

    // 4. Page Specific Translations
    const pathname = window.location.pathname.replace(/\/+$/, '') || '/';

    // --- HOME PAGE (/) ---
    if (pathname === '/') {
      if (isAz) {
        const badge = document.querySelector('.hero-badge');
        if (badge) {
          const dot = badge.querySelector('.hero-badge-dot');
          badge.innerHTML = '';
          if (dot) badge.appendChild(dot);
          badge.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.home.badge));
        }

        const heroTitleSpan = document.querySelector('.hero-title span');
        if (heroTitleSpan) heroTitleSpan.textContent = TRANSLATIONS_AZ.home.title;

        const heroSub = document.querySelector('.hero-subtitle-line');
        if (heroSub) heroSub.textContent = TRANSLATIONS_AZ.home.subtitle;

        const heroDesc = document.querySelector('.hero-desc');
        if (heroDesc) heroDesc.textContent = TRANSLATIONS_AZ.home.desc;

        const heroActions = document.querySelectorAll('.hero-actions a');
        if (heroActions.length >= 2) {
          const svg1 = heroActions[0].querySelector('svg');
          heroActions[0].innerHTML = '';
          if (svg1) heroActions[0].appendChild(svg1);
          heroActions[0].appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.home.btnExplore));

          const svg2 = heroActions[1].querySelector('svg');
          heroActions[1].innerHTML = '';
          if (svg2) heroActions[1].appendChild(svg2);
          heroActions[1].appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.home.btnSimulator));
        }

        const statLabels = document.querySelectorAll('.stat-item .stat-label');
        if (statLabels.length >= 4) {
          statLabels[0].textContent = TRANSLATIONS_AZ.home.statExp;
          statLabels[1].textContent = TRANSLATIONS_AZ.home.statFam;
          statLabels[2].textContent = TRANSLATIONS_AZ.home.statScen;
          statLabels[3].textContent = TRANSLATIONS_AZ.home.statInt;
        }

        // About Section
        const aboutEyebrow = document.querySelector('.about-grid .section-eyebrow');
        if (aboutEyebrow) aboutEyebrow.textContent = TRANSLATIONS_AZ.home.aboutEyebrow;

        const aboutTitle = document.querySelector('.about-grid .section-title-xl');
        if (aboutTitle) aboutTitle.innerHTML = TRANSLATIONS_AZ.home.aboutTitle;

        const aboutP = document.querySelector('.about-grid p');
        if (aboutP) aboutP.textContent = TRANSLATIONS_AZ.home.aboutDesc;

        const featureTitles = document.querySelectorAll('.feature-title');
        const featureDescs = document.querySelectorAll('.feature-desc');
        if (featureTitles.length >= 3) {
          featureTitles[0].textContent = TRANSLATIONS_AZ.home.feat1Title;
          featureDescs[0].textContent = TRANSLATIONS_AZ.home.feat1Desc;
          featureTitles[1].textContent = TRANSLATIONS_AZ.home.feat2Title;
          featureDescs[1].textContent = TRANSLATIONS_AZ.home.feat2Desc;
          featureTitles[2].textContent = TRANSLATIONS_AZ.home.feat3Title;
          featureDescs[2].textContent = TRANSLATIONS_AZ.home.feat3Desc;
        }

        // Flight Families
        const famSection = document.querySelectorAll('.section')[1];
        if (famSection) {
          const eye = famSection.querySelector('.section-eyebrow');
          if (eye) eye.textContent = TRANSLATIONS_AZ.home.famEyebrow;
          const tit = famSection.querySelector('.section-title-xl');
          if (tit) tit.innerHTML = TRANSLATIONS_AZ.home.famTitle;
          const va = famSection.querySelector('.btn-sm');
          if (va) va.textContent = TRANSLATIONS_AZ.home.famViewAll;
        }

        // Mission Environments
        const envSection = document.querySelectorAll('.section')[2];
        if (envSection) {
          const eye = envSection.querySelector('.section-eyebrow');
          if (eye) eye.textContent = TRANSLATIONS_AZ.home.envEyebrow;
          const tit = envSection.querySelector('.section-title-xl');
          if (tit) tit.innerHTML = TRANSLATIONS_AZ.home.envTitle;
          const desc = envSection.querySelector('.section-desc');
          if (desc) desc.textContent = TRANSLATIONS_AZ.home.envDesc;
        }

        // Platform modules
        const modSection = document.querySelectorAll('.section')[3];
        if (modSection) {
          const eye = modSection.querySelector('.section-eyebrow');
          if (eye) eye.textContent = TRANSLATIONS_AZ.home.modEyebrow;
          const tit = modSection.querySelector('.section-title-xl');
          if (tit) tit.innerHTML = TRANSLATIONS_AZ.home.modTitle;
        }
      }
    }

    // --- ANALYTICS PAGE (/analytics) ---
    else if (pathname === '/analytics') {
      if (isAz) {
        const hTitle = document.querySelector('.analytics-hero h1');
        if (hTitle) hTitle.textContent = TRANSLATIONS_AZ.analytics.pageTitle;
        const hDesc = document.querySelector('.analytics-hero p');
        if (hDesc) hDesc.textContent = TRANSLATIONS_AZ.analytics.pageDesc;

        // Holo lab buttons
        const modeBtns = document.querySelectorAll('.view-mode-pill');
        if (modeBtns.length >= 3) {
          modeBtns[0].textContent = TRANSLATIONS_AZ.analytics.btnScatter;
          modeBtns[1].textContent = TRANSLATIONS_AZ.analytics.btnFlame;
          modeBtns[2].textContent = TRANSLATIONS_AZ.analytics.btnDuct;
        }

        // Charts
        const chartCards = document.querySelectorAll('.chart-card');
        if (chartCards.length >= 4) {
          const t1 = chartCards[0].querySelector('.chart-header-title');
          if (t1) t1.textContent = TRANSLATIONS_AZ.analytics.chart1Title;
          const t2 = chartCards[1].querySelector('.chart-header-title');
          if (t2) t2.textContent = TRANSLATIONS_AZ.analytics.chart2Title;
          const t3 = chartCards[2].querySelector('.chart-header-title');
          if (t3) t3.textContent = TRANSLATIONS_AZ.analytics.chart3Title;
          const t4 = chartCards[3].querySelector('.chart-header-title');
          if (t4) t4.textContent = TRANSLATIONS_AZ.analytics.chart4Title;
        }
      }
    }

    // --- EXPLORER PAGE (/explorer) ---
    else if (pathname === '/explorer') {
      if (isAz) {
        const title = document.querySelector('.explorer-header-title');
        if (title) title.textContent = TRANSLATIONS_AZ.explorer.pageTitle;
        const desc = document.querySelector('.explorer-header-subtitle');
        if (desc) desc.textContent = TRANSLATIONS_AZ.explorer.pageDesc;

        const searchInp = document.getElementById('filter-search');
        if (searchInp) searchInp.setAttribute('placeholder', TRANSLATIONS_AZ.explorer.searchPlaceholder);

        const resetBtn = document.querySelector('.btn-reset-filters');
        if (resetBtn) resetBtn.textContent = TRANSLATIONS_AZ.explorer.btnReset;

        const ths = document.querySelectorAll('.explorer-table th');
        if (ths.length >= 9) {
          ths[0].textContent = TRANSLATIONS_AZ.explorer.tableHeaderId;
          ths[1].textContent = TRANSLATIONS_AZ.explorer.tableHeaderFamily;
          ths[2].textContent = TRANSLATIONS_AZ.explorer.tableHeaderFuel;
          ths[3].textContent = TRANSLATIONS_AZ.explorer.tableHeaderO2;
          ths[4].textContent = TRANSLATIONS_AZ.explorer.tableHeaderPressure;
          ths[5].textContent = TRANSLATIONS_AZ.explorer.tableHeaderBurnTime;
          ths[6].textContent = TRANSLATIONS_AZ.explorer.tableHeaderDe;
          ths[7].textContent = TRANSLATIONS_AZ.explorer.tableHeaderOutcome;
          ths[8].textContent = TRANSLATIONS_AZ.explorer.tableHeaderActions;
        }
      }
    }

    // --- SIMULATOR PAGE (/simulator) ---
    else if (pathname === '/simulator') {
      if (isAz) {
        const sTitle = document.querySelector('.sim-header h1');
        if (sTitle) sTitle.textContent = TRANSLATIONS_AZ.simulator.pageTitle;
        const sDesc = document.querySelector('.sim-header p');
        if (sDesc) sDesc.textContent = TRANSLATIONS_AZ.simulator.pageDesc;

        const pHead = document.querySelector('.preset-heading');
        if (pHead) pHead.textContent = TRANSLATIONS_AZ.simulator.presetHeading;

        const askBtn = document.querySelector('.btn-ask-ai-sim');
        if (askBtn) askBtn.textContent = TRANSLATIONS_AZ.simulator.btnAskAiSim;
      }
    }

    // --- ABOUT PAGE (/about) ---
    else if (pathname === '/about') {
      if (isAz) {
        const pEye = document.querySelector('.page-header .section-eyebrow');
        if (pEye) pEye.textContent = TRANSLATIONS_AZ.about.eyebrow;
        const pTit = document.querySelector('.page-header .section-title-xl');
        if (pTit) pTit.innerHTML = TRANSLATIONS_AZ.about.pageTitle;
        const pDesc = document.querySelector('.page-header .section-desc');
        if (pDesc) pDesc.textContent = TRANSLATIONS_AZ.about.pageDesc;

        const sec1Eye = document.querySelector('.about-section .two-col > div:first-child .section-eyebrow');
        if (sec1Eye) sec1Eye.textContent = TRANSLATIONS_AZ.about.sec1Eyebrow;
        const sec1Tit = document.querySelector('.about-section .two-col > div:first-child .section-title-xl');
        if (sec1Tit) sec1Tit.innerHTML = TRANSLATIONS_AZ.about.sec1Title;

        const infoCards = document.querySelectorAll('.info-card');
        if (infoCards.length >= 4) {
          infoCards[0].querySelector('h3').textContent = TRANSLATIONS_AZ.about.card1Title;
          infoCards[0].querySelector('p').textContent = TRANSLATIONS_AZ.about.card1Desc;
          infoCards[1].querySelector('h3').textContent = TRANSLATIONS_AZ.about.card2Title;
          infoCards[1].querySelector('p').textContent = TRANSLATIONS_AZ.about.card2Desc;
          infoCards[2].querySelector('h3').textContent = TRANSLATIONS_AZ.about.card3Title;
          infoCards[2].querySelector('p').textContent = TRANSLATIONS_AZ.about.card3Desc;
          infoCards[3].querySelector('h3').textContent = TRANSLATIONS_AZ.about.card4Title;
          infoCards[3].querySelector('p').textContent = TRANSLATIONS_AZ.about.card4Desc;
        }

        const sec2Eye = document.querySelector('.about-section .two-col > div:last-child .section-eyebrow');
        if (sec2Eye) sec2Eye.textContent = TRANSLATIONS_AZ.about.sec2Eyebrow;
        const sec2Tit = document.querySelector('.about-section .two-col > div:last-child .section-title-xl');
        if (sec2Tit) sec2Tit.innerHTML = TRANSLATIONS_AZ.about.sec2Title;
      }
    }
  }

  // --- CONTROLLER INIT ---
  function initNav() {
    // 1. Progress Bar
    const progressBar = document.getElementById('nav-progress');
    if (progressBar) {
      window.addEventListener('scroll', () => {
        const total = document.body.scrollHeight - window.innerHeight;
        const pct = total > 0 ? (window.scrollY / total) * 100 : 0;
        progressBar.style.width = pct + '%';
      });
    }

    // 2. Navbar shrink on scroll
    const navbar = document.getElementById('navbar');
    if (navbar) {
      window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 40);
      });
    }

    // 3. Active Link detection
    const path = window.location.pathname.replace(/\/+$/, '') || '/';
    document.querySelectorAll('.nav-link').forEach(link => {
      const href = link.getAttribute('href');
      if (href === path || (path === '/' && href === '/') || (href !== '/' && path.startsWith(href))) {
        link.classList.add('active');
      }
    });

    // 4. Smooth page transition
    document.querySelectorAll('a[href^="/"]').forEach(link => {
      link.addEventListener('click', e => {
        const href = link.getAttribute('href');
        if (href && !href.startsWith('#') && !link.target) {
          e.preventDefault();
          document.body.style.opacity = '0';
          document.body.style.transition = 'opacity 0.2s ease';
          setTimeout(() => { window.location.href = href; }, 200);
        }
      });
    });

    // 5. Fade in
    document.body.style.opacity = '0';
    requestAnimationFrame(() => {
      document.body.style.transition = 'opacity 0.35s ease';
      document.body.style.opacity = '1';
    });

    // 6. Mobile menu
    const mobileBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.getElementById('nav-links-list');
    if (mobileBtn && navLinks) {
      mobileBtn.addEventListener('click', () => navLinks.classList.toggle('open'));
    }

    // 7. Scroll reveal observer
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
    }, { threshold: 0.1 });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

    // 8. Language Toggle Handler
    const currentLang = localStorage.getItem('firex_lang') || 'en';
    applyLanguage(currentLang);

    const langBtn = document.getElementById('nav-lang-btn') || document.getElementById('lang-btn-ai');
    if (langBtn) {
      langBtn.textContent = currentLang.toUpperCase();
      langBtn.addEventListener('click', () => {
        const cur = localStorage.getItem('firex_lang') || 'en';
        const next = (cur === 'az') ? 'en' : 'az';
        localStorage.setItem('firex_lang', next);
        langBtn.textContent = next.toUpperCase();
        applyLanguage(next);
        window.location.reload();
      });
    }
  }

  // Ensure execution regardless of load state
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initNav);
  } else {
    initNav();
  }
})();
