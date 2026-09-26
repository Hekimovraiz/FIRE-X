import os
import pandas as pd
from sqlalchemy import create_engine

# Köhnə bazanı təmizləyirik
if os.path.exists("nasa_combustion_data.db"):
    os.remove("nasa_combustion_data.db")

engine = create_engine('sqlite:///nasa_combustion_data.db')

# Hər faylın öz cədvəl adı və uyğun encoding ayarı
files_config = {
    "flex_data": {
        "path": "Nasa_data/PSI-69_Experimental table_FLEX.csv",
        "encoding": "latin-1"
    },
    "bass_ii_data": {
        "path": "Nasa_data/PSI-25_Experimental table_BASS-II.csv",
        "encoding": "utf-8-sig"
    },
    "saffire_1_data": {
        "path": "Nasa_data/PSI-98_Experimental table_SAFFIRE-1.csv",
        "encoding": "utf-8-sig"
    }
}

# Hər faylı oxuyub öz cədvəlinə yazırıq
for table_name, config in files_config.items():
    try:
        df = pd.read_csv(config["path"], encoding=config["encoding"])
        df.columns = df.columns.str.strip()
        
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"[+] {config['path']} uğurla '{table_name}' cədvəlinə yazıldı.")
        
    except Exception as e:
        print(f"[-] {config['path']} xətası: {e}")
