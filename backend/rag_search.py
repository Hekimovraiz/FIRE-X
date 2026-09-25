import sqlite3
import pandas as pd

def search_fire_data(query_fuel):
    # SQLite bazasına qoşuluruq
    conn = sqlite3.connect('fire_safety.db')
    
    # Bazadan həmin yanacaq növünə uyğun eksperimentləri axtarırıq (SQL Injection-ın qarşısını almaq üçün parameterli sorğu)
    query = "SELECT * FROM flex_experiments WHERE fuel_material LIKE ?;"
    result = pd.read_sql(query, conn, params=(f"%{query_fuel}%",))
    
    conn.close()
    
    if result.empty:
        print(f"'{query_fuel}' üzrə heç bir eksperiment tapılmadı.")
    else:
        print(f"\n--- '{query_fuel}' ÜZRƏ TAPILAN NASA EKSPERİMENTLƏRİ ---")
        print(result.to_string(index=False))
        print("\n[AI Sül-Cavab Simulyasiyası]: Bu məlumatlar NASA mikroqravitasiya yanma tədqiqatlarına əsaslanır.")

if __name__ == "__main__":
    # Test olaraq 'PMMA' yanacağı üçün axtarış edirik
    search_fire_data("PMMA")
