/**
 * NASA FIRE-X Universal Client-Side Controller & Complete Bilingual Engine (v5.0)
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
      analytics: 'Analitika Mərkəzi',
      explorer: 'Məlumat Kəşfiyyatı',
      simulator: 'Missiya Simulyatoru',
      ai: 'AI Köməkçi',
      about: 'Haqqında',
      live: 'CANLI',
      aiBtn: 'AI Köməkçi'
    },

    // === COMMON FOOTER ===
    footer: {
      desc: 'Mikroyerçəkim Yanma Datalarından Süni İntellektlə Yanğın Təhlükəsizliyi İntellekti. NASA Space Apps Challenge 2026.',
      devCredit: 'Tərtibatçı: <strong>Raiz Həkimov</strong> · <span style="color:rgba(255,255,255,0.55);">Developed & Engineered by Raiz Həkimov</span>',
      colPlatform: 'Platforma',
      colData: 'Məlumat Mənbələri',
      analytics: 'Analitika Mərkəzi',
      explorer: 'Məlumat Kəşfiyyatı',
      simulator: 'Missiya Simulyatoru',
      ai: 'AI Köməkçi',
      about: 'Sənədləşmə & Haqqında',
      copyright: '© 2026 NASA FIRE-X · NASA Space Apps Challenge üçün hazırlanıb',
      githubBtn: 'GitHub Repozitoriyası',
      dataCount: 'Məlumat: NASA Physical Science Informatics (PSI) · 879 kanonik eksperiment'
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
      heroTag: 'ORBİTAL MAYE VƏ YANMA TELEMETRİYASI MƏRKƏZİ',
      pageTitle: 'Mikroyerçəkim Yanma Analitikası Mühərriki',
      pageDesc: '879 NASA uçuş testindən real-vaxt 3D telemetriya, sönmə hədləri analizi və məcburi hava axını dinamikası',
      
      stat1Label: 'Kanonik Eksperimentlər',
      stat1Sub: 'NASA PSI təsdiqlənmiş uçuş qeydləri',
      stat2Label: 'Orta Sönmə Diametri (de)',
      stat2Sub: 'Mikroyerçəkimdə sönmə həddi',
      stat3Label: 'Orta O₂ Mol Hissəsi',
      stat3Sub: 'Sınaq diapazonu: 14.0% – 50.0%',
      stat4Label: 'Uçuş Tədqiqatları',
      stat4Val: '24 Ailə',
      stat4Sub: 'FLEX · BASS · SAFFIRE · SOFIE · ACME · FLARE · MGM',

      holoTitle: 'İnteraktiv 3D/4D Yanma Holo-Laboratoriyası',
      holoSub: 'WebGL 3D Telemetriya Simulyasiyası // Fırlatmaq üçün çəkin, Miqyası dəyişmək üçün sürüşdürün',
      tabScatter: '4D Saçılma Kubu',
      tabDroplet: '3D Kürəvi Damcı Alovu',
      tabAirflow: '3D Məcburi Hava Axını Kanalı',

      hudTitle: 'SEÇİLMİŞ EKSPERİMENT',
      hudActive: 'AKTİV',
      hudKeyId: 'Telemetriya ID:',
      hudKeyFam: 'Uçuş Tədqiqatı:',
      hudKeyFuel: 'Yanacaq / Material:',
      hudKeyO2: 'Oksigen Mol Hissəsi:',
      hudKeyPress: 'Kamera Təzyiqi:',
      hudKeyDe: 'Sönmə Diametri (de):',
      hudKeyOutcome: 'Sönmə Nəticəsi:',
      hudInspect: 'Bazada İncələ →',
      hudAskAi: 'AI-ya Soruş',
      hudHint: '[3D İDARƏETMƏ] Sol Düymə: 3D Fırlat · Çarx: Yaxınlaşdır · Üzərinə gətir: Məlumatı oxu',

      mod1Badge: 'SÖNMƏ HƏDDİ // NASA-STD-6001',
      mod1Title: 'Alov Sönmə Diametri vs. Oksigen Qatılığı',
      mod1Desc: 'O₂ mol hissəsindən asılı olaraq damcı və yanacaq nümunələrinin kritik sönmə sərhədlərini qiymətləndirir. Oksidləşdirici artdıqca sönmə diametrinin eksponensial azalmasını göstərir.',
      mod1Btn: 'Sönmə Dinamikasını Təhlil Et',

      mod2Badge: 'HİDROAERODİNAMİKA // CIR KANALI TELEMETRİYASI',
      mod2Title: 'Yanma Müddəti vs. Məcburi Konvektiv Hava Axını',
      mod2Desc: 'Aşağı axında (<2 sm/s) radiativ soyuma ilə yüksək axında (>18 sm/s) konvektiv üfürmə arasındakı keçidi təhlil edir. Mikroyerçəkimdə optimal yanma sabitliyi dəhlizini müəyyən edir.',
      mod2Btn: 'Üfürmə Sürətini Qiymətləndir',

      mod3Badge: 'MATERİALŞÜNASLIQ // KİMYƏVİ TƏSNİFAT',
      mod3Title: 'Yanacaq Alovlanma Matrisi və Nümunə Bölgüsü',
      mod3Desc: '879 uçuş testinin material kateqoriyası və kimyəvi tərkibinə görə ətraflı bölgüsü. Maye karbohidrogenlər, spirtlər, bərk termoplastlar, parçalar və kosmik polimerləri müqayisə edir.',
      mod3Btn: 'Material Riskini Sorğula',

      mod4Badge: 'SINAQ REJİMLƏRİ // NƏTİCƏ TAKSONOMİYASI',
      mod4Title: 'Sönmə Nəticələrinin Tezlikləri',
      mod4Desc: 'BKS-də həyata keçirilən orbital sınaq kampaniyalarında müşahidə olunan sönmə rejimlərinin təsnifatı. Radiativ itki, konvektiv üfürmə və tam yanacaq tükənməsini kəmiyyətcə müəyyən edir.',
      mod4Btn: 'Sönmə Fizikasını İzah Et',

      outcomeRad: 'Radiativ Sönmə (Soyuma > İstilik Ayrılması)',
      outcomeBlow: 'Konvektiv Üfürmə / Hava Axını ilə Qopma',
      outcomeDep: 'Yanacağın Tam Tükənməsi (Bitmə)',
      outcomeSus: 'Davamlı Sabit Mikroyerçəkim Yanması',

      lawsBadge: 'NASA GLENN TƏDQİQAT MƏRKƏZİ // ELMİ NƏTİCƏLƏR ARXİVİ',
      lawsTitle: 'Mikroyerçəkimdə Üç Əsas Yanma Qanunu',
      law1Num: 'QANUN 01 // DİFFUZİYA ÜSTÜNLÜYÜ',
      law1Title: 'Təbii Konveksiyanın Olmaması',
      law1Desc: 'Yerdə qaldırıcı qüvvə isti qazları yuxarı qaldıraraq təzə oksigeni içəri çəkir. 10⁻⁴ g mikroyerçəkimdə isə oksigen daşınması sırf molekulyar diffuziyadır. Alovlar tam kürəvi forma alır və daha aşağı temperaturda yanır (Yerdəki 2200 K qarşılığında 1400–1650 K).',
      law2Num: 'QANUN 02 // SOYUQ ALOVUN DAVAMLILIĞI',
      law2Title: 'Aşağı Temperaturlu Kimyəvi Kinetika',
      law2Desc: 'NASA FLEX təcrübələri aşkar etdi ki, görünən isti alov söndükdən sonra belə damcılar 600–800 K-də soyuq alov kinetikası ilə görünməz şəkildə yanmağa davam edir. Standart kosmik gəmi yanğın detektorları bu gizli rejimi hiss edə bilmir.',
      law3Num: 'QANUN 03 // VENTİLYASİYA ALOVLANMA PARADOKSU',
      law3Title: 'Məcburi Konveksiya Paradoksu',
      law3Desc: 'Kabin ventilyasiyasını söndürərək yanğını yatırtmaq kiçik hava axını rejimlərində (2–6 sm/s) alovlanmanı daha da pisləşdirə bilər, çünki bu zəif axın radiativ sönmə baş verənə qədər oksigen təchizatını gücləndirir.'
    },

    // === 3. EXPLORER PAGE (explorer.html) ===
    explorer: {
      subBadge: 'NASA FİZİKİ ELMLƏR İNFORMATİKASI // ORBİTAL UÇUŞ REPOZİTORİYASI',
      pageTitle: 'Orbital Telemetriya Məlumat Kəşfiyyatı',
      btnExport: 'Telemetriyanı İxrac Et (.CSV)',
      btnAnalytics: '3D Analitika Görünüşü',

      sidebarTitle: 'FİLTRLƏR VƏ AXTARIŞ',
      btnReset: 'Hamısını Sıfırla',
      searchLabel: 'Sürətli Axtarış',
      searchPlaceholder: 'ID, yanacaq və ya nəticə...',
      familyLabel: 'Uçuş və Tədqiqat Ailəsi (Cəmi 24)',
      familyDefault: 'Bütün Uçuş Tədqiqatları',
      fuelLabel: 'Yanacaq / Material (106 Növ)',
      fuelDefault: 'Bütün Materiallar və Yanacaqlar',
      outcomeLabel: 'Sönmə Nəticəsi',
      outcomeDefault: 'Bütün Sönmə Nəticələri',
      o2MinLabel: 'Minimum O₂ Mol %',
      btnAskAiDataset: 'Dataset Haqqında AI-dan Soruş',

      showingPrefix: 'CƏMİ',
      showingMid: 'UÇUŞ SINAĞINDAN',
      showingSuffix: 'GÖSTƏRİLİR',
      pageSize: 'SƏHİFƏ ÖLÇÜSÜ:',

      thId: 'Kanonik ID ⬍',
      thFamily: 'Tədqiqat / Ailə ⬍',
      thFuel: 'Yanacaq / Material ⬍',
      thO2: 'O₂ Mol % ⬍',
      thPressure: 'Təzyiq (kPa) ⬍',
      thBurnTime: 'Yanma Müddəti (s) ⬍',
      thDe: 'Sönmə d_e (mm) ⬍',
      thOutcome: 'Nəticə ⬍',
      thActions: 'Əməliyyatlar',

      btnInspect: 'İncələ',
      btnCompare: '+ Müqayisə et',
      btnCompareAdded: '✓ Əlavə edildi',
      btnPrev: '← Əvvəlki',
      btnNext: 'Növbəti →',
      pageIndicator: (cur, total) => `SƏHİFƏ ${cur} / ${total}`,

      cmpSelected: (n) => `4 EKSPERİMENTDƏN ${n} SEÇİLDİ`,
      btnRunCompare: 'Yan-yana Müqayisə Et',
      btnClearCompare: 'Təmizlə',

      drawerSub: 'TELEMETRİYA MÜFƏTTİŞİ // KANONİK QEYD',
      btnCloseDrawer: '✕ Bağla',
      drawerNotesTitle: 'NASA ELMİ MÜŞAHİDƏ QEYDLƏRİ',
      btnAskAiExp: 'Bu Eksperiment Haqqında AI-dan Soruş'
    },

    // === 4. SIMULATOR PAGE (simulator.html) ===
    simulator: {
      subBadge: 'UÇUŞ RİSKİNİN PROQNOZLAŞDIRILMASI VƏ SÖNDÜRMƏ MODELİ',
      pageTitle: 'Planetar Missiya Yanğın Riski Simulyatoru',
      pageDesc: 'NASA-STD-6001 həssaslıq metrikləri əsasında müxtəlif kosmik kabin mühitlərində alovlanma potensialını, sönmə diametrlərini və tələb olunan boğucu qaz miqdarını hesablayır.',

      scenIssTitle: 'BKS Standart Atmosferi',
      scenIssSub: '21.0% O₂ · 101.3 kPa · Dəniz Səviyyəsi Standartı',
      scenLunarTitle: 'Artemis Ay Yaşayış Modulu',
      scenLunarSub: '34.0% O₂ · 56.5 kPa · Aşağı Təzyiqli EVA Rejimi',
      scenHypoxicTitle: 'Dərin Kosmos Hipoqsik Sığınacaq',
      scenHypoxicSub: '15.0% O₂ · 70.3 kPa · Yanğın Boğma Rejimi',
      scenCustomTitle: 'Fərdi Atmosfer Laboratoriyası',
      scenCustomSub: 'Parametrik Oksidləşdirici və Təzyiq Sınağı',

      sliderO2: 'Oksigen Qatılığı (O₂ %)',
      sliderPressure: 'Ümumi Təzyiq (kPa)',
      btnAskAiSim: 'Yaşayış Təhlükəsizliyini AI ilə Qiymətləndir',

      fhiLabel: 'FHI / 10.0',
      
      metO2Title: 'O₂ Qatılığı',
      metO2Sub: 'Kabin həcm payı',
      metPressTitle: 'Ümumi Təzyiq',
      metPressSub: '1.0 atm ekvivalenti',
      metPo2Title: 'O₂ Parsial Təzyiqi',
      metPo2Sub: 'Metabolik norma: 21.3 kPa',
      metDeTitle: 'Sönmə Diametri (de)',
      metDeSub: 'Kritik sönmə damcı ölçüsü',
      metMultTitle: 'Alov Sürəti Əmsalı',
      metMultSub: '21% O₂-yə görə normallaşdırılıb',
      metPurgeTitle: 'Tələb Olunan Söndürücü',
      metPurgeSub: 'N₂/CO₂ qaz doldurma qatılığı',

      advisoryHeader: 'AVTOMATLAŞDIRILMIŞ NASA EKİPAJ TƏHLÜKƏSİZLİYİ MƏSLƏHƏTİ',

      matrixTitle: 'Ssenari Müqayisə Matrisi',
      matThScen: 'SSENARİ',
      matThO2: 'O₂ %',
      matThPress: 'TƏZYİQ',
      matThFhi: 'FHI XALI',
      matThRisk: 'RİSK SƏVİYYƏSİ',
      matThSupp: 'SÖNDÜRMƏ'
    },

    // === 5. AI ASSISTANT (ai.html) ===
    ai: {
      heading: 'TÖVSİYƏ OLUNAN ELMİ SUALLAR',
      welcomeTitle: 'FIRE-X Elmi Tədqiqat Köməkçisi Onlayndır',
      welcomeDesc: 'NASA Mikroyerçəkim Yanma İntellekt Konsoluna xoş gəlmisiniz. <strong>OpenAI GPT-6-luna</strong> ilə təchiz olunub və Beynəlxalq Kosmik Stansiya ilə Cygnus orbital sınaqlarından <strong>879 yoxlanılmış uçuş eksperimentinə</strong> əsaslanır.<br><br>Damcı sönməsi (FLEX), bərk yanacaqların alovlanması (BASS/SOFIE), kosmik gəmi yanğınlarının yayılması (SAFFIRE) və ya planetar yaşayış modullarının atmosfer təhlükəsizliyi (Artemis / BKS) haqqında ətraflı suallar verə bilərsiniz.',
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
   * Applies translations to the entire page DOM based on active language
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
    if (liveBadge && (liveBadge.textContent.includes('LIVE') || liveBadge.textContent.includes('CANLI'))) {
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
    const footerTagline = document.getElementById('footer-tagline');
    if (footerTagline) footerTagline.textContent = isAz ? TRANSLATIONS_AZ.footer.desc : 'AI-Powered Fire Safety Insights from Microgravity Combustion Data. NASA Space Apps Challenge 2026.';

    const footerColPlatform = document.getElementById('footer-col-platform');
    if (footerColPlatform) footerColPlatform.textContent = isAz ? TRANSLATIONS_AZ.footer.colPlatform : 'Platform';

    const footerColData = document.getElementById('footer-col-data');
    if (footerColData) footerColData.textContent = isAz ? TRANSLATIONS_AZ.footer.colData : 'Data';

    const linkAnalytics = document.getElementById('footer-link-analytics');
    if (linkAnalytics) linkAnalytics.textContent = isAz ? TRANSLATIONS_AZ.footer.analytics : 'Analytics Hub';

    const linkExplorer = document.getElementById('footer-link-explorer');
    if (linkExplorer) linkExplorer.textContent = isAz ? TRANSLATIONS_AZ.footer.explorer : 'Data Explorer';

    const linkSimulator = document.getElementById('footer-link-simulator');
    if (linkSimulator) linkSimulator.textContent = isAz ? TRANSLATIONS_AZ.footer.simulator : 'Mission Simulator';

    const linkAi = document.getElementById('footer-link-ai');
    if (linkAi) linkAi.textContent = isAz ? TRANSLATIONS_AZ.footer.ai : 'AI Assistant';

    const linkAbout = document.getElementById('footer-link-about');
    if (linkAbout) linkAbout.textContent = isAz ? TRANSLATIONS_AZ.footer.about : 'Documentation';

    const footerCopyright = document.getElementById('footer-copyright');
    if (footerCopyright) footerCopyright.textContent = isAz ? TRANSLATIONS_AZ.footer.copyright : '© 2026 NASA FIRE-X · Built for NASA Space Apps Challenge';

    const footerDataCount = document.getElementById('footer-data-count');
    if (footerDataCount) footerDataCount.textContent = isAz ? TRANSLATIONS_AZ.footer.dataCount : 'Data: NASA Physical Science Informatics (PSI) · 879 canonical';

    // 4. Page-Specific Deep Translations
    const pathname = window.location.pathname.replace(/\/+$/, '') || '/';

    // ==========================================
    // PAGE 1: HOME (/)
    // ==========================================
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

    // ==========================================
    // PAGE 2: ANALYTICS (/analytics)
    // ==========================================
    else if (pathname === '/analytics') {
      if (isAz) {
        // Tag & Hero
        const holoTag = document.querySelector('.holo-tag');
        if (holoTag) {
          const dot = holoTag.querySelector('.holo-tag-dot');
          holoTag.innerHTML = '';
          if (dot) holoTag.appendChild(dot);
          holoTag.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.analytics.heroTag));
        }

        const heroH1 = document.querySelector('header h1');
        if (heroH1) {
          heroH1.innerHTML = 'Mikroyerçəkim Yanma <span style="background:linear-gradient(135deg,#00F5FF,#2979FF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Analitikası Mühərriki</span>';
        }

        const heroDesc = document.querySelector('header p');
        if (heroDesc) heroDesc.textContent = TRANSLATIONS_AZ.analytics.pageDesc;

        // HUD Stat boxes
        const statBoxes = document.querySelectorAll('.hud-stat-box');
        if (statBoxes.length >= 4) {
          statBoxes[0].querySelector('.hud-stat-label').textContent = TRANSLATIONS_AZ.analytics.stat1Label;
          statBoxes[0].querySelector('.hud-stat-sub').textContent = TRANSLATIONS_AZ.analytics.stat1Sub;

          statBoxes[1].querySelector('.hud-stat-label').textContent = TRANSLATIONS_AZ.analytics.stat2Label;
          statBoxes[1].querySelector('.hud-stat-sub').textContent = TRANSLATIONS_AZ.analytics.stat2Sub;

          statBoxes[2].querySelector('.hud-stat-label').textContent = TRANSLATIONS_AZ.analytics.stat3Label;
          statBoxes[2].querySelector('.hud-stat-sub').textContent = TRANSLATIONS_AZ.analytics.stat3Sub;

          statBoxes[3].querySelector('.hud-stat-label').textContent = TRANSLATIONS_AZ.analytics.stat4Label;
          statBoxes[3].querySelector('.hud-stat-value').textContent = TRANSLATIONS_AZ.analytics.stat4Val;
          statBoxes[3].querySelector('.hud-stat-sub').textContent = TRANSLATIONS_AZ.analytics.stat4Sub;
        }

        // Holo toolbar
        const tabScatter = document.getElementById('tab-3d-scatter');
        if (tabScatter) {
          const svg = tabScatter.querySelector('svg');
          tabScatter.innerHTML = '';
          if (svg) tabScatter.appendChild(svg);
          tabScatter.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.analytics.tabScatter));
        }

        const tabDroplet = document.getElementById('tab-3d-droplet');
        if (tabDroplet) {
          const svg = tabDroplet.querySelector('svg');
          tabDroplet.innerHTML = '';
          if (svg) tabDroplet.appendChild(svg);
          tabDroplet.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.analytics.tabDroplet));
        }

        const tabAirflow = document.getElementById('tab-3d-airflow');
        if (tabAirflow) {
          const svg = tabAirflow.querySelector('svg');
          tabAirflow.innerHTML = '';
          if (svg) tabAirflow.appendChild(svg);
          tabAirflow.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.analytics.tabAirflow));
        }

        // HUD readout keys
        const hudKeys = document.querySelectorAll('.hud-telemetry-overlay .hud-key');
        if (hudKeys.length >= 7) {
          hudKeys[0].textContent = TRANSLATIONS_AZ.analytics.hudKeyId;
          hudKeys[1].textContent = TRANSLATIONS_AZ.analytics.hudKeyFam;
          hudKeys[2].textContent = TRANSLATIONS_AZ.analytics.hudKeyFuel;
          hudKeys[3].textContent = TRANSLATIONS_AZ.analytics.hudKeyO2;
          hudKeys[4].textContent = TRANSLATIONS_AZ.analytics.hudKeyPress;
          hudKeys[5].textContent = TRANSLATIONS_AZ.analytics.hudKeyDe;
          hudKeys[6].textContent = TRANSLATIONS_AZ.analytics.hudKeyOutcome;
        }

        const hudHint = document.querySelector('.hud-controls-hint');
        if (hudHint) hudHint.innerHTML = '<span style="color:var(--hud-cyan);">[3D İDARƏETMƏ]</span> Sol Düymə: 3D Fırlat · Çarx: Yaxınlaşdır · Üzərinə gətir: Məlumatı oxu';

        // 4 Modules
        const modCards = document.querySelectorAll('.module-card');
        if (modCards.length >= 4) {
          // Module 1
          modCards[0].querySelector('.module-badge').textContent = TRANSLATIONS_AZ.analytics.mod1Badge;
          modCards[0].querySelector('.module-title').textContent = TRANSLATIONS_AZ.analytics.mod1Title;
          modCards[0].querySelector('.module-desc').textContent = TRANSLATIONS_AZ.analytics.mod1Desc;
          const a1 = modCards[0].querySelector('.ask-ai-chip');
          if (a1) a1.textContent = ' ' + TRANSLATIONS_AZ.analytics.mod1Btn;

          // Module 2
          modCards[1].querySelector('.module-badge').textContent = TRANSLATIONS_AZ.analytics.mod2Badge;
          modCards[1].querySelector('.module-title').textContent = TRANSLATIONS_AZ.analytics.mod2Title;
          modCards[1].querySelector('.module-desc').textContent = TRANSLATIONS_AZ.analytics.mod2Desc;
          const a2 = modCards[1].querySelector('.ask-ai-chip');
          if (a2) a2.textContent = ' ' + TRANSLATIONS_AZ.analytics.mod2Btn;

          // Module 3
          modCards[2].querySelector('.module-badge').textContent = TRANSLATIONS_AZ.analytics.mod3Badge;
          modCards[2].querySelector('.module-title').textContent = TRANSLATIONS_AZ.analytics.mod3Title;
          modCards[2].querySelector('.module-desc').textContent = TRANSLATIONS_AZ.analytics.mod3Desc;
          const a3 = modCards[2].querySelector('.ask-ai-chip');
          if (a3) a3.textContent = ' ' + TRANSLATIONS_AZ.analytics.mod3Btn;

          // Module 4
          modCards[3].querySelector('.module-badge').textContent = TRANSLATIONS_AZ.analytics.mod4Badge;
          modCards[3].querySelector('.module-title').textContent = TRANSLATIONS_AZ.analytics.mod4Title;
          modCards[3].querySelector('.module-desc').textContent = TRANSLATIONS_AZ.analytics.mod4Desc;
          const a4 = modCards[3].querySelector('.ask-ai-chip');
          if (a4) a4.textContent = ' ' + TRANSLATIONS_AZ.analytics.mod4Btn;

          const outcomeLabels = modCards[3].querySelectorAll('.outcome-label-row span:first-child');
          if (outcomeLabels.length >= 4) {
            outcomeLabels[0].textContent = TRANSLATIONS_AZ.analytics.outcomeRad;
            outcomeLabels[1].textContent = TRANSLATIONS_AZ.analytics.outcomeBlow;
            outcomeLabels[2].textContent = TRANSLATIONS_AZ.analytics.outcomeDep;
            outcomeLabels[3].textContent = TRANSLATIONS_AZ.analytics.outcomeSus;
          }
        }

        // Insights / Laws
        const insightsBanner = document.querySelector('.insights-banner');
        if (insightsBanner) {
          const bannerTag = insightsBanner.querySelector('.holo-tag');
          if (bannerTag) bannerTag.textContent = TRANSLATIONS_AZ.analytics.lawsBadge;

          const bannerTitle = insightsBanner.querySelector('h3');
          if (bannerTitle) bannerTitle.textContent = TRANSLATIONS_AZ.analytics.lawsTitle;

          const insightCards = insightsBanner.querySelectorAll('.insight-card');
          if (insightCards.length >= 3) {
            insightCards[0].querySelector('.insight-num').textContent = TRANSLATIONS_AZ.analytics.law1Num;
            insightCards[0].querySelector('h4').textContent = TRANSLATIONS_AZ.analytics.law1Title;
            insightCards[0].querySelector('p').textContent = TRANSLATIONS_AZ.analytics.law1Desc;

            insightCards[1].querySelector('.insight-num').textContent = TRANSLATIONS_AZ.analytics.law2Num;
            insightCards[1].querySelector('h4').textContent = TRANSLATIONS_AZ.analytics.law2Title;
            insightCards[1].querySelector('p').textContent = TRANSLATIONS_AZ.analytics.law2Desc;

            insightCards[2].querySelector('.insight-num').textContent = TRANSLATIONS_AZ.analytics.law3Num;
            insightCards[2].querySelector('h4').textContent = TRANSLATIONS_AZ.analytics.law3Title;
            insightCards[2].querySelector('p').textContent = TRANSLATIONS_AZ.analytics.law3Desc;
          }
        }
      }
    }

    // ==========================================
    // PAGE 3: EXPLORER (/explorer)
    // ==========================================
    else if (pathname === '/explorer') {
      if (isAz) {
        // Header
        const headerSub = document.querySelector('.explorer-header div > div:first-child > div:first-child');
        if (headerSub) headerSub.textContent = TRANSLATIONS_AZ.explorer.subBadge;

        const headerH1 = document.querySelector('.explorer-header h1');
        if (headerH1) headerH1.innerHTML = 'Orbital Telemetriya <span class="text-gradient">Məlumat Kəşfiyyatı</span>';

        const exportBtn = document.querySelector('.explorer-header .btn-ghost');
        if (exportBtn) {
          const svg = exportBtn.querySelector('svg');
          exportBtn.innerHTML = '';
          if (svg) exportBtn.appendChild(svg);
          exportBtn.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.explorer.btnExport));
        }

        const analyticsBtn = document.querySelector('.explorer-header .btn-neon');
        if (analyticsBtn) {
          const svg = analyticsBtn.querySelector('svg');
          analyticsBtn.innerHTML = '';
          if (svg) analyticsBtn.appendChild(svg);
          analyticsBtn.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.explorer.btnAnalytics));
        }

        // Sidebar
        const filterTitle = document.querySelector('.filter-console-title span');
        if (filterTitle) filterTitle.textContent = TRANSLATIONS_AZ.explorer.sidebarTitle;

        const resetBtn = document.querySelector('.filter-console-title button');
        if (resetBtn) resetBtn.textContent = TRANSLATIONS_AZ.explorer.btnReset;

        const filterLabels = document.querySelectorAll('.filter-console .filter-label');
        if (filterLabels.length >= 4) {
          filterLabels[0].textContent = TRANSLATIONS_AZ.explorer.searchLabel;
          filterLabels[1].textContent = TRANSLATIONS_AZ.explorer.familyLabel;
          filterLabels[2].textContent = TRANSLATIONS_AZ.explorer.fuelLabel;
          filterLabels[3].textContent = TRANSLATIONS_AZ.explorer.outcomeLabel;
          if (filterLabels.length >= 5) filterLabels[4].textContent = TRANSLATIONS_AZ.explorer.o2MinLabel;
        }

        const searchInp = document.getElementById('filter-search');
        if (searchInp) searchInp.setAttribute('placeholder', TRANSLATIONS_AZ.explorer.searchPlaceholder);

        const famSel = document.getElementById('filter-family');
        if (famSel && famSel.options.length > 0) famSel.options[0].textContent = TRANSLATIONS_AZ.explorer.familyDefault;

        const fuelSel = document.getElementById('filter-fuel');
        if (fuelSel && fuelSel.options.length > 0) fuelSel.options[0].textContent = TRANSLATIONS_AZ.explorer.fuelDefault;

        const outSel = document.getElementById('filter-outcome');
        if (outSel && outSel.options.length > 0) outSel.options[0].textContent = TRANSLATIONS_AZ.explorer.outcomeDefault;

        const askAiSideBtn = document.querySelector('.filter-console a.btn-neon');
        if (askAiSideBtn) {
          const svg = askAiSideBtn.querySelector('svg');
          askAiSideBtn.innerHTML = '';
          if (svg) askAiSideBtn.appendChild(svg);
          askAiSideBtn.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.explorer.btnAskAiDataset));
        }

        // Table headers
        const ths = document.querySelectorAll('.orbital-table th');
        if (ths.length >= 9) {
          ths[0].textContent = TRANSLATIONS_AZ.explorer.thId;
          ths[1].textContent = TRANSLATIONS_AZ.explorer.thFamily;
          ths[2].textContent = TRANSLATIONS_AZ.explorer.thFuel;
          ths[3].textContent = TRANSLATIONS_AZ.explorer.thO2;
          ths[4].textContent = TRANSLATIONS_AZ.explorer.thPressure;
          ths[5].textContent = TRANSLATIONS_AZ.explorer.thBurnTime;
          ths[6].textContent = TRANSLATIONS_AZ.explorer.thDe;
          ths[7].textContent = TRANSLATIONS_AZ.explorer.thOutcome;
          ths[8].textContent = TRANSLATIONS_AZ.explorer.thActions;
        }

        // Pagination buttons
        const prevBtn = document.getElementById('btn-prev-page');
        if (prevBtn) prevBtn.textContent = TRANSLATIONS_AZ.explorer.btnPrev;

        const nextBtn = document.getElementById('btn-next-page');
        if (nextBtn) nextBtn.textContent = TRANSLATIONS_AZ.explorer.btnNext;

        // Compare dock
        const runCmpBtn = document.querySelector('.compare-dock .btn-solid-cyan');
        if (runCmpBtn) runCmpBtn.textContent = TRANSLATIONS_AZ.explorer.btnRunCompare;

        const clearCmpBtn = document.querySelector('.compare-dock .btn-ghost');
        if (clearCmpBtn) clearCmpBtn.textContent = TRANSLATIONS_AZ.explorer.btnClearCompare;
      }
    }

    // ==========================================
    // PAGE 4: SIMULATOR (/simulator)
    // ==========================================
    else if (pathname === '/simulator') {
      if (isAz) {
        // Header
        const subBadge = document.querySelector('.sim-header div > div > div:first-child');
        if (subBadge) subBadge.textContent = TRANSLATIONS_AZ.simulator.subBadge;

        const simH1 = document.querySelector('.sim-header h1');
        if (simH1) simH1.textContent = TRANSLATIONS_AZ.simulator.pageTitle;

        const simP = document.querySelector('.sim-header p');
        if (simP) simP.textContent = TRANSLATIONS_AZ.simulator.pageDesc;

        // 4 Preset cards
        const scenBtns = document.querySelectorAll('.scenario-card-btn');
        if (scenBtns.length >= 4) {
          scenBtns[0].querySelector('.scenario-name').textContent = TRANSLATIONS_AZ.simulator.scenIssTitle;
          scenBtns[0].querySelector('.scenario-specs').textContent = TRANSLATIONS_AZ.simulator.scenIssSub;

          scenBtns[1].querySelector('.scenario-name').textContent = TRANSLATIONS_AZ.simulator.scenLunarTitle;
          scenBtns[1].querySelector('.scenario-specs').textContent = TRANSLATIONS_AZ.simulator.scenLunarSub;

          scenBtns[2].querySelector('.scenario-name').textContent = TRANSLATIONS_AZ.simulator.scenHypoxicTitle;
          scenBtns[2].querySelector('.scenario-specs').textContent = TRANSLATIONS_AZ.simulator.scenHypoxicSub;

          scenBtns[3].querySelector('.scenario-name').textContent = TRANSLATIONS_AZ.simulator.scenCustomTitle;
          scenBtns[3].querySelector('.scenario-specs').textContent = TRANSLATIONS_AZ.simulator.scenCustomSub;
        }

        // Custom sliders headers
        const sliderHeaders = document.querySelectorAll('.slider-header span:first-child');
        if (sliderHeaders.length >= 2) {
          sliderHeaders[0].textContent = TRANSLATIONS_AZ.simulator.sliderO2;
          sliderHeaders[1].textContent = TRANSLATIONS_AZ.simulator.sliderPressure;
        }

        // Ask AI Button
        const askAiBtn = document.querySelector('.sim-controls-panel .btn-neon');
        if (askAiBtn) {
          const svg = askAiBtn.querySelector('svg');
          askAiBtn.innerHTML = '';
          if (svg) askAiBtn.appendChild(svg);
          askAiBtn.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.simulator.btnAskAiSim));
        }

        // 6 Metrics Cards
        const metricCards = document.querySelectorAll('.sim-metric-card');
        if (metricCards.length >= 6) {
          metricCards[0].querySelector('.metric-card-label').textContent = TRANSLATIONS_AZ.simulator.metO2Title;
          metricCards[0].querySelector('.metric-card-sub').textContent = TRANSLATIONS_AZ.simulator.metO2Sub;

          metricCards[1].querySelector('.metric-card-label').textContent = TRANSLATIONS_AZ.simulator.metPressTitle;
          metricCards[1].querySelector('.metric-card-sub').textContent = TRANSLATIONS_AZ.simulator.metPressSub;

          metricCards[2].querySelector('.metric-card-label').textContent = TRANSLATIONS_AZ.simulator.metPo2Title;
          metricCards[2].querySelector('.metric-card-sub').textContent = TRANSLATIONS_AZ.simulator.metPo2Sub;

          metricCards[3].querySelector('.metric-card-label').textContent = TRANSLATIONS_AZ.simulator.metDeTitle;
          metricCards[3].querySelector('.metric-card-sub').textContent = TRANSLATIONS_AZ.simulator.metDeSub;

          metricCards[4].querySelector('.metric-card-label').textContent = TRANSLATIONS_AZ.simulator.metMultTitle;
          metricCards[4].querySelector('.metric-card-sub').textContent = TRANSLATIONS_AZ.simulator.metMultSub;

          metricCards[5].querySelector('.metric-card-label').textContent = TRANSLATIONS_AZ.simulator.metPurgeTitle;
          metricCards[5].querySelector('.metric-card-sub').textContent = TRANSLATIONS_AZ.simulator.metPurgeSub;
        }

        // Advisory Header
        const advHeader = document.querySelector('.advisory-header');
        if (advHeader) {
          const svg = advHeader.querySelector('svg');
          advHeader.innerHTML = '';
          if (svg) advHeader.appendChild(svg);
          advHeader.appendChild(document.createTextNode(' ' + TRANSLATIONS_AZ.simulator.advisoryHeader));
        }
      }
    }

    // ==========================================
    // PAGE 5: ABOUT (/about)
    // ==========================================
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

  // --- CONTROLLER INITIALIZATION ---
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
