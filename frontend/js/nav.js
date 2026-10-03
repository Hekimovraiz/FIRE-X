(function() {
  'use strict';

  // --- BILINGUAL TRANSLATION DICTIONARY (EN -> AZ) ---
  const AZ_DICT = {
    // Navigation
    "Home": "Ana Səhifə",
    "Analytics": "Analitika",
    "Data Explorer": "Məlumat Kəşfiyyatı",
    "Simulator": "Simulyator",
    "AI Assistant": "AI Köməkçi",
    "About": "Haqqında",
    "LIVE": "CANLI",
    "Documentation": "Sənədləşmə",
    "MICROGRAVITY COMBUSTION INTEL": "MİKROYERÇƏKİM YANMA İNTELLEKTİ",

    // Common Buttons & Actions
    "Explore Data": "Məlumatları Kəşf Et",
    "Launch Simulator": "Simulyatoru Başlat",
    "View All Data →": "Bütün Datalara Bax →",
    "Send Query": "Sorğunu Göndər",
    "Clear Session": "Sessiyanı Təmizlə",
    "Reset Filters": "Filtrləri Sıfırla",
    "Inspect": "Bax",
    "+ Compare": "+ Müqayisə et",
    "Scroll": "Aşağı",

    // Hero & Home Section
    "NASA SPACE APPS CHALLENGE 2026 \u00a0·\u00a0 FIRE SAFETY IN SPACE": "NASA SPACE APPS CHALLENGE 2026 \u00a0·\u00a0 KOSMOSDA YANĞIN TƏHLÜKƏSİZLİYİ",
    "FLAME IN FREEFALL": "ALOV SƏRBƏST DÜŞMƏDƏ",
    "FIRE-X Intelligence Platform": "FIRE-X İntellekt Platforması",
    "879 verified microgravity combustion experiments analyzed by AI — powering the future of spacecraft fire safety aboard the ISS, Artemis Lunar Habitat, and beyond.": "AI tərəfindən təhlil edilmiş 879 yoxlanılmış mikroqravitasiya yanma eksperimenti — BKS, Artemis Ay Modulu və gələcək kosmik missiyalarda yanğın təhlükəsizliyini təmin edir.",
    "Canonical Experiments": "Kanonik Eksperimentlər",
    "Flight Families": "Uçuş Ailələri",
    "Mission Scenarios": "Missiya Ssenariləri",
    "Data Integrity": "Məlumat Dəqiqliyi",
    "MISSION TIME (UTC):": "MİSSİYA VAXTI (UTC):",
    "About the Project": "Layihə Haqqında",
    "Fire Safety Science in Orbit": "Orbitdə Yanğın Təhlükəsizliyi Elmi",
    "879 Verified Experiments": "879 Yoxlanılmış Eksperiment",
    "AI-Powered Analysis": "Süni İntellekt Analitikası",
    "Mission Scenario Simulator": "Missiya Ssenari Simulyatoru",
    "Flight Investigations": "Uçuş Tədqiqatları",
    "24 Experiment Families": "24 Təcrübə Ailəsi",
    "Planetary Fire Risk": "Planetar Yanğın Riski",
    "Mission Environments": "Missiya Mühitləri",
    "Standard": "Standart",
    "ISS Atmosphere": "BKS Atmosferi",
    "Artemis Program": "Artemis Proqramı",
    "Lunar Habitat": "Ay Yaşayış Modulu",
    "Emergency Protocol": "Fövqəladə Protokol",
    "Hypoxic Safe-Haven": "Hipoqsik Sığınacaq",
    "Oxygen": "Oksigen",
    "Fire Hazard Index": "Yanğın Təhlükəsi İndeksi",
    "NOMINAL RISK": "MÖTƏDİL RİSK",
    "ELEVATED HAZARD": "YÜKSƏK TƏHLÜKƏ",
    "SUPPRESSED": "SÖNDÜRÜLMÜŞ",
    "Platform Modules": "Platforma Modulları",
    "Explore the Platform": "Platformanı Kəşf Edin",
    "Analytics Hub": "Analitika Mərkəzi",

    // Analytics Page
    "Combustion Analytics Hub": "Yanma Analitikası Mərkəzi",
    "3D scientific telemetry from 879 NASA experiments": "879 NASA eksperimentindən 3D elmi telemetriya",
    "ORBITAL TELEMETRY 3D VISUALIZER": "ORBİTAL TELEMETRİYA 3D VİZUALİZATORU",
    "TELEMETRY SCATTER 4D": "4D TELEMETRİYA SAÇILMASI",
    "SPHERICAL FLAME 3D": "3D KÜRƏVİ ALOV",
    "AIRFLOW DUCT 3D": "3D HAVA AXINI KANALI",
    "RESET CAMERA": "KAMERANI SIFIRLA",
    "TOGGLE ROTATION": "FIRLANMANI DƏYİŞ",
    "FLAME EXTINCTION DIAMETER VS. OXYGEN": "ALOV SÖNMƏ DİAMETRİ VS. OKSİGEN",
    "BURN DURATION VS. FORCED CONVECTIVE AIRFLOW": "YANMA MÜDDƏTİ VS. MƏCBURİ HAVA AXINI",
    "FUEL FLAMMABILITY MATRIX & SAMPLE DISTRIBUTION": "YANACAQ ALOVLANMA MATRİSİ VƏ NÜMUNƏ BÖLGÜSÜ",
    "EXTINCTION OUTCOME FREQUENCIES": "SÖNMƏ NƏTİCƏLƏRİNİN TEZLİYİ",

    // Explorer Page
    "EXPERIMENT DATA EXPLORER": "EKSPERİMENT MƏLUMAT KƏŞFİYYATÇISI",
    "Flight & Research Family (24 Total)": "Uçuş və Tədqiqat Ailəsi (Cəmi 24)",
    "Fuel / Material (106 Types)": "Yanacaq / Material (106 Növ)",
    "Extinction Outcome": "Sönmə Nəticəsi",
    "Search telemetry records...": "Telemetriya qeydlərində axtarın...",

    // Simulator Page
    "Planetary Mission Fire Hazard Simulator": "Planetar Missiya Yanğın Riski Simulyatoru",
    "Simulate fire behavior across lunar, martian, and custom spacecraft atmospheres": "Ay, Mars və fərdi kosmik atmosferlərdə alov davranışını simulyasiya edin",
    "Atmospheric Preset Scenarios": "Atmosfer Ssenariləri",
    "Standard ISS Baseline": "Standart BKS Əsası",
    "Artemis Lunar Habitat": "Artemis Ay Modulu",
    "Hypoxic Safe-Haven Protocol": "Hipoqsik Sığınacaq Protokolu",
    "Custom Research Environment": "Fərdi Tədqiqat Mühiti",

    // AI Page
    "FIRE-X AI Research Assistant": "FIRE-X AI Tədqiqat Köməkçisi",
    "RECOMMENDED SCIENTIFIC INQUIRIES": "TÖVSİYƏ OLUNAN ELMİ SUALLAR",
    "Ask about microgravity combustion, flame dynamics, or experiment IDs...": "Mikroyerçəkimdə yanma, alov dinamikası və ya eksperiment ID-ləri haqqında soruşun...",
    "PRESS ENTER TO SEND": "GÖNDƏRMƏK ÜÇÜN ENTER BASIN",
    "CONFIDENTIAL FLIGHT DATA ANALYZED THROUGH SECURE BACKEND PROXY": "MƏXFİ UÇUŞ DATALARI TƏHLÜKƏSİZ SERVER VASİTƏSİLƏ TƏHLİL OLUNUR"
  };

  function applyLanguage(lang) {
    if (lang !== 'az') return;

    // 1. Navbar Links
    document.querySelectorAll('.nav-link').forEach(link => {
      const text = link.textContent.trim();
      if (AZ_DICT[text]) link.textContent = AZ_DICT[text];
    });

    // 2. Nav brand subtitle
    const brandSub = document.querySelector('.nav-brand-sub');
    if (brandSub && AZ_DICT[brandSub.textContent.trim()]) {
      brandSub.textContent = AZ_DICT[brandSub.textContent.trim()];
    }

    // 3. Translate all elements matching dict keys
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;
    while ((node = walker.nextNode())) {
      const trimmed = node.nodeValue.trim();
      if (AZ_DICT[trimmed]) {
        node.nodeValue = node.nodeValue.replace(trimmed, AZ_DICT[trimmed]);
      }
    }

    // 4. Input placeholders
    document.querySelectorAll('input[placeholder]').forEach(input => {
      const ph = input.getAttribute('placeholder');
      if (AZ_DICT[ph]) input.setAttribute('placeholder', AZ_DICT[ph]);
    });
  }

  // Progress bar
  const progressBar = document.getElementById('nav-progress');
  if (progressBar) {
    window.addEventListener('scroll', () => {
      const total = document.body.scrollHeight - window.innerHeight;
      const pct = total > 0 ? (window.scrollY / total) * 100 : 0;
      progressBar.style.width = pct + '%';
    });
  }

  // Navbar scroll shrink
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 40);
    });
  }

  // Active link
  const path = window.location.pathname.replace(/\/+$/, '') || '/';
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === path || (path === '/' && href === '/') || (href !== '/' && path.startsWith(href))) {
      link.classList.add('active');
    }
  });

  // Page transitions
  document.querySelectorAll('a[href^="/"]').forEach(link => {
    link.addEventListener('click', e => {
      const href = link.getAttribute('href');
      if (href && !href.startsWith('#') && !link.target) {
        e.preventDefault();
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.25s ease';
        setTimeout(() => { window.location.href = href; }, 250);
      }
    });
  });

  // Body fade in & apply language
  document.addEventListener('DOMContentLoaded', () => {
    document.body.style.opacity = '0';
    requestAnimationFrame(() => {
      document.body.style.transition = 'opacity 0.4s ease';
      document.body.style.opacity = '1';
    });

    const currentLang = localStorage.getItem('firex_lang') || 'en';
    applyLanguage(currentLang);
  });

  // Mobile menu
  const mobileBtn = document.getElementById('mobile-menu-btn');
  const navLinks = document.getElementById('nav-links-list');
  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => navLinks.classList.toggle('open'));
  }

  // Intersection observer for .reveal elements
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // Language toggle button handler
  const langBtn = document.getElementById('nav-lang-btn') || document.getElementById('lang-btn-ai');
  if (langBtn) {
    const current = localStorage.getItem('firex_lang') || 'en';
    langBtn.textContent = current.toUpperCase();
    langBtn.addEventListener('click', () => {
      const next = (localStorage.getItem('firex_lang') || 'en') === 'az' ? 'en' : 'az';
      localStorage.setItem('firex_lang', next);
      langBtn.textContent = next.toUpperCase();
      window.location.reload();
    });
  }
})();
