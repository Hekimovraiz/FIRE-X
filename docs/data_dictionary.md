# FIRE-X Canonical Data Dictionary

Bu sənəd **FIRE-X (NASA Space Apps Challenge 2026)** platformasının vahid verilənlər sxemini (Canonical Schema) və NASA PSI cədvəllərindən necə transformasiya edildiyini müəyyən edir.

---

## 1. Vahid Kanonik Sxem (Canonical Schema)

Fərqli NASA eksperimentləri (`FLEX`, `BASS-II`, `SAFFIRE`) fərqli sütun adları, vahidlər və formatlardan istifadə edir. Bütün sınaqları ortaq məxrəcə gətirmək üçün aşağıdakı kanonik cədvəl qurulur:

| Kanonik Sütun | Tip | Məna / Təsvir | Standart Vahid | Nümunə |
| :--- | :--- | :--- | :--- | :--- |
| `experiment_id` | TEXT (PK) | Unikal eksperiment identifikatoru | - | `FLEX-001`, `BASS-B1`, `SAF-S1` |
| `dataset_family` | TEXT | NASA tədqiqat ailəsi | - | `FLEX`, `BASS-II`, `SAFFIRE-I` |
| `investigation_id`| TEXT | NASA PSI tədqiqat kodu | - | `PSI-69`, `PSI-25`, `PSI-98` |
| `original_test_id`| TEXT | NASA cədvəlindəki orijinal test kodu | - | `1`, `B1`, `S1` |
| `fuel_material` | TEXT | Yanacaq və ya materialın standart adı | - | `Methanol`, `PMMA`, `SIBAL Fabric` |
| `material_category`| TEXT | Materialın fiziki kateqoriyası | - | `Liquid Droplet`, `Solid Polymer`, `Fabric` |
| `sample_description`| TEXT | Ölçülər, forma və qalınlıq detalları | - | `100 micron film, 2 cm wide`, `Droplet 1.69mm` |
| `oxygen_pct` | REAL | İlkin Oksigen qatılığı ($O_2$) | `% by vol` (0-100) | `21.0`, `22.2`, `18.0` |
| `pressure_mmhg` | REAL | Kamera təzyiqi | `mmHg` | `757.7`, `760.0`, `500.0` |
| `pressure_kpa` | REAL | Hesablanmış kamera təzyiqi | `kPa` | `101.0`, `66.7` |
| `burn_time_s` | REAL | Müşahidə olunan yanma müddəti | `saniyə (s)` | `4.3`, `45.5`, `420.0` |
| `extinction_outcome`| TEXT | Alovun sönmə və ya testin bitmə mexanizmi | - | `Flame Extinction`, `Blowoff`, `Burnout` |
| `extinction_diameter_mm`| REAL | Sönmə anındakı damcı diametri (FLEX) | `mm` | `0.89` |
| `initial_diameter_mm` | REAL | İlkin damcı diametri (FLEX) | `mm` | `1.69` |
| `burning_rate_mms`| REAL | Yanma sürəti | `mm/s` | `0.52` |
| `airflow_velocity_cms`| REAL | Məcburi və ya təbii hava axını sürəti | `cm/s` | `20.0`, `5.0` |
| `gravity_condition`| TEXT | Qravitasiya mühiti | - | `Microgravity (~0g)` |
| `ignition_power_w`| REAL | Alovlandırma gücü (SAFFIRE) | `Watt (W)` | `182.0` |
| `ignition_time_s` | REAL | Alovlandırma impulsu müddəti | `saniyə (s)` | `8.0` |
| `co2_pct` | REAL | Yanma sonrası $CO_2$ qatılığı | `% by vol` | `0.44` |
| `co_ppm` | REAL | Yanma sonrası Dəm qazı ($CO$) | `ppm` | `6.0` |
| `test_date` | TEXT | Eksperimentin keçirilmə tarixi | `YYYY-MM-DD` | `2009-03-05` |
| `source_name` | TEXT | Mənbə təşkilat/arxiv | - | `NASA Physical Sciences Informatics` |
| `source_url` | TEXT | Birbaşa NASA PSI/NTRS sübut linki | `URL` | `https://psi.nasa.gov/...` |
| `notes` | TEXT | Əlavə fiziki qeydlər və müşahidələr | - | `Test end: Disruption` |

---

## 2. NASA Cədvəllərindən Kanonik Sxemə Xəritələnmə (Mapping)

### A. FLEX (PSI-69)
* `FLEX Test #` ➔ `original_test_id`, `experiment_id` = `FLEX-{num:03d}`
* `Fuel` ➔ `fuel_material`
* `O initial ambient composition; mole fraction` ➔ `oxygen_pct` ($mole\_fraction \times 100$)
* `Ambient pressure; mmHg` ➔ `pressure_mmhg`, $kpa = mmHg \times 0.133322$
* `Burn time; s` ➔ `burn_time_s`
* `Test end` ➔ `extinction_outcome`
* `Visible flame extinction diameter; mm` ➔ `extinction_diameter_mm`
* `Droplet initial diameter; mm` ➔ `initial_diameter_mm`
* `Burning rate; mm` ➔ `burning_rate_mms`

### B. BASS-II (PSI-25)
* `Test #` ➔ `original_test_id`, `experiment_id` = `BASS-{test_no}`
* `Fuel Sample Material` ➔ `fuel_material` və `sample_description`
* `Calibrated initial O2 % by vol` ➔ `oxygen_pct`
* `Air display` / `Fan display` ➔ `airflow_velocity_cms`
* `Final CO2 % by vol` ➔ `co2_pct`
* `Final CO (ppm)` ➔ `co_ppm`
* Bərk materiallar üçün təzyiq standart olaraq ISS kabin mühiti: $760 \ mmHg$ (101.3 kPa).

### C. SAFFIRE-1 (PSI-98)
* `Sample Number` ➔ `original_test_id`, `experiment_id` = `SAF-{sample_no}`
* `Material` ➔ `fuel_material`
* `Percent O2` ➔ `oxygen_pct` (orta qiymət)
* `Air Flow (cm/s)` ➔ `airflow_velocity_cms`
* `Burn Time (s)` ➔ `burn_time_s`
* `Ignition Power (W)` ➔ `ignition_power_w`
* `Ignition Time (s)` ➔ `ignition_time_s`
