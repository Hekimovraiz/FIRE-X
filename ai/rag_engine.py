import sqlite3
import pandas as pd
import os

def get_combustion_context(query: str):
    # Bazadan məlumatları çəkib AI üçün kontekst hazırlayırıq
    conn = sqlite3.connect('nasa_combustion_data.db')
    
    # Sadə bir nümunə olaraq cədvəllərdən bəzi sətirləri oxuyuruq
    flex_df = pd.read_sql("SELECT * FROM flex_data LIMIT 5", conn)
    bass_df = pd.read_sql("SELECT * FROM bass_ii_data LIMIT 5", conn)
    saffire_df = pd.read_sql("SELECT * FROM saffire_1_data LIMIT 5", conn)
    
    conn.close()
    
    context = f"""
    Here is partial data from NASA microgravity combustion experiments (FIRE-X project):
    - FLEX Data sample: {flex_df.to_dict(orient='records')}
    - BASS-II Data sample: {bass_df.to_dict(orient='records')}
    - SAFFIRE-1 Data sample: {saffire_df.to_dict(orient='records')}
    """
    return context
