# FIRE-X Data Sources & Provenance

Bu sənəd **FIRE-X** platformasında istifadə olunan və əlavə olaraq cəlb edilə biləcək bütün NASA mikroyerçəkimi yanma və kosmik yanğın təhlükəsizliyi mənbələrini ehtiva edir.

---

## 1. Əsas NASA Verilənlər Repozitoriyaları

### A. NASA Physical Sciences Informatics (PSI)
NASA-nın mikroyerçəkimi fiziki elmlər üzrə ən böyük rəsmi portalıdır.
* **Portal Linki:** [https://psi.nasa.gov](https://psi.nasa.gov)
* **Axtarış bölməsi:** *Discipline ➔ Combustion Science*
* **Əsas Tədqiqat Qrupları (Investigations):**
  1. **PSI-69 (FLEX & FLEX-2):** *Flame Extinction Experiment*
     * URL: `https://psi.nasa.gov/physci/repo/data/investigations/PSI-69`
     * Tədqiqat növü: Maye damcılarının (Methanol, Heptane, Decane və s.) mikroyerçəkimdə sönmə diametri, buxarlanma və yanma sürəti.
  2. **PSI-25 (BASS & BASS-II):** *Burning and Suppression of Solids*
     * URL: `https://psi.nasa.gov/physci/repo/data/investigations/PSI-25`
     * Tədqiqat növü: Bərk materialların (PMMA, Nomex, Delrin, Cotton Fabric) alov yayılması və sönmə hədləri.
  3. **PSI-98 (SAFFIRE I–VI):** *Spacecraft Fire Safety Demonstration*
     * URL: `https://psi.nasa.gov/physci/repo/data/investigations/PSI-98`
     * Tədqiqat növü: Cygnus kosmik yük gəmisində aparılmış real böyükmiqyaslı (1 metrədək) yanğın sınaqları.
  4. **ACME (Advanced Combustion via Microgravity Experiments):**
     * ISS daxilində CIR (Combustion Integrated Rack) çərçivəsində aparılan BRE, CFI, E-FIELD layihələri.

### B. NASA Technical Reports Server (NTRS)
NASA-nın elmi məqalə, texniki hesabat və təcrübə sınaq jurnallarının mərkəzi arxividir.
* **Portal Linki:** [https://ntrs.nasa.gov](https://ntrs.nasa.gov)
* **Faydalı Axtarış Sözləri:**
  * `"microgravity combustion experiment data"`
  * `"spacecraft fire safety BASS extinction"`
  * `"FLEX droplet extinction diameter PSI"`
  * `"SAFFIRE flammability limit oxygen concentration"`
* **Layihəyə daxil edilmiş NTRS İstinadları:**
  * Citations ID: `20120015928` (Droplet array extinction limits)
  * Citations ID: `20240002981` (Silicone rubber insulation spacecraft fire tests)
  * Citations ID: `20190001859` (SAFFIRE material flammability tests)

### C. NASA Open Data Portal
* **Portal Linki:** [https://data.nasa.gov](https://data.nasa.gov)
* **Açar söz:** `Combustion`, `Fire Safety`, `Microgravity`

---

## 2. Yeni Dataları Necə Əlavə Etməli?

Əgər yuxarıdakı mənbələrdən yeni CSV və ya Excel faylları yükləsəniz:
1. Faylı birbaşa layihənin `Nasa_data/` və ya `data/raw/` qovluğuna yerləşdirin.
2. Vahid data pipeline (`scripts/pipeline.py`) avtomatik olaraq bu faylı oxuyub vahid kanonik sxemə (`canonical_experiments`) çevirəcək.
