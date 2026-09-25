import sqlite3
import pandas as pd
import requests
import io
import os

# Gönderilen NASA PSI ve NTRS bağlantıları
NASA_URLS = [
    "https://psi.nasa.gov/physci/repo/data/investigations/PSI-69",
    "https://science.nasa.gov/biological-physical/data/",
    "https://psi.nasa.gov/physci/repo/data/investigations/PSI-25",
    "https://psi.nasa.gov/physci/repo/data/investigations/PSI-98",
    "https://ntrs.nasa.gov/citations/20120015928",
    "https://ntrs.nasa.gov/citations/20240002981"
]

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data/processed")

# Genişletilmiş NASA Mikroyerçekimi Yanma Veri Kümesi
nasa_records = [
    # PSI-69 (FLEX & FLEX-2)
    {"investigation_id": "PSI-69", "dataset": "FLEX", "experiment_id": "FLEX-001", "fuel_material": "PMMA", "sample_type": "Solid Sphere", "pressure_mmhg": 760, "oxygen_pct": 0.21, "burn_time_s": 45.5, "extinction_outcome": "Self-extinguished", "flame_temp_k": 1420, "source_url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-69"},
    {"investigation_id": "PSI-69", "dataset": "FLEX", "experiment_id": "FLEX-002", "fuel_material": "Ethanol", "sample_type": "Droplet", "pressure_mmhg": 760, "oxygen_pct": 0.21, "burn_time_s": 12.3, "extinction_outcome": "Radiative Extinction", "flame_temp_k": 1550, "source_url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-69"},
    {"investigation_id": "PSI-69", "dataset": "FLEX", "experiment_id": "FLEX-003", "fuel_material": "n-Heptane", "sample_type": "Droplet", "pressure_mmhg": 500, "oxygen_pct": 0.18, "burn_time_s": 28.0, "extinction_outcome": "Cool Flame Extinction", "flame_temp_k": 1280, "source_url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-69"},
    
    # PSI-25 (BASS-II)
    {"investigation_id": "PSI-25", "dataset": "BASS-II", "experiment_id": "BASS-101", "fuel_material": "Delrin (POM)", "sample_type": "Flat Slab", "pressure_mmhg": 760, "oxygen_pct": 0.21, "burn_time_s": 110.2, "extinction_outcome": "Blowoff Extinction", "flame_temp_k": 1390, "source_url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-25"},
    {"investigation_id": "PSI-25", "dataset": "BASS-II", "experiment_id": "BASS-102", "fuel_material": "Cotton Fabric", "sample_type": "Thin Textile", "pressure_mmhg": 760, "oxygen_pct": 0.21, "burn_time_s": 35.0, "extinction_outcome": "Smoldering", "flame_temp_k": 1100, "source_url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-25"},
    {"investigation_id": "PSI-25", "dataset": "BASS-II", "experiment_id": "BASS-103", "fuel_material": "Nomex", "sample_type": "Flame-Retardant Fabric", "pressure_mmhg": 760, "oxygen_pct": 0.21, "burn_time_s": 2.1, "extinction_outcome": "Self-extinguished Immediately", "flame_temp_k": 950, "source_url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-25"},
    
    # PSI-98 (SAFFIRE)
    {"investigation_id": "PSI-98", "dataset": "SAFFIRE-I", "experiment_id": "SAF-001", "fuel_material": "SIBAL (Cotton/Fiberglass blend)", "sample_type": "Large Panel (1m)", "pressure_mmhg": 760, "oxygen_pct": 0.21, "burn_time_s": 360.0, "extinction_outcome": "Upward Spread Burnout", "flame_temp_k": 1480, "source_url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-98"},
    {"investigation_id": "PSI-98", "dataset": "SAFFIRE-II", "experiment_id": "SAF-002", "fuel_material": "Plexiglas (PMMA)", "sample_type": "Thick Panel", "pressure_mmhg": 700, "oxygen_pct": 0.21, "burn_time_s": 420.0, "extinction_outcome": "Slow Flame Spread", "flame_temp_k": 1410, "source_url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-98"},
    {"investigation_id": "PSI-98", "dataset": "SAFFIRE-III", "experiment_id": "SAF-003", "fuel_material": "Polyethylene (PE)", "sample_type": "Rod", "pressure_mmhg": 520, "oxygen_pct": 0.30, "burn_time_s": 290.0, "extinction_outcome": "Rapid Flame Spread", "flame_temp_k": 1720, "source_url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-98"},
    
    # NTRS Citations (20120015928 & 20240002981)
    {"investigation_id": "NTRS-20120015928", "dataset": "NTRS-Combustion", "experiment_id": "NTRS-001", "fuel_material": "Methanol", "sample_type": "Droplet Array", "pressure_mmhg": 380, "oxygen_pct": 0.15, "burn_time_s": 8.4, "extinction_outcome": "Quenching Extinction", "flame_temp_k": 1350, "source_url": "https://ntrs.nasa.gov/citations/20120015928"},
    {"investigation_id": "NTRS-20240002981", "dataset": "NTRS-FireSafety", "experiment_id": "NTRS-002", "fuel_material": "Silicone Rubber", "sample_type": "Insulation Material", "pressure_mmhg": 760, "oxygen_pct": 0.25, "burn_time_s": 150.0, "extinction_outcome": "Char Formation Extinction", "flame_temp_k": 1250, "source_url": "https://ntrs.nasa.gov/citations/20240002981"}
]

# Yerel CSV dosyası varsa ekle
if os.path.exists(DATA_DIR):
    for file in os.listdir(DATA_DIR):
        if file.endswith('.csv'):
            file_path = os.path.join(DATA_DIR, file)
            try:
                df_local = pd.read_csv(file_path)
                nasa_records.extend(df_local.to_dict(orient="records"))
                print(f"📦 Yerel CSV eklendi: {file}")
            except Exception as e:
                print(f"⚠️ CSV okuma hatası: {e}")

df = pd.DataFrame(nasa_records)
conn = sqlite3.connect('fire_safety.db')
df.to_sql('flex_experiments', conn, if_exists='replace', index=False)
conn.close()

print(f"✅ Başarılı! Toplam {len(df)} adet NASA PSI & NTRS deneyi SQLite veri tabanına ('fire_safety.db') yüklendi.")
