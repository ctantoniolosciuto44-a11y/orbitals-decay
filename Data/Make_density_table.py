import numpy as np
import pymsis

alts_km = np.array([150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 700, 800])
idx = int(pymsis.Variable.MASS_DENSITY)

def mean_density_profile(day):
    """Densità di massa media [kg/m^3] a ogni quota, mediata su 24 ore
    e su una griglia di longitudini e latitudini."""
    start = np.datetime64(f"{day}T00:00")
    dates = np.arange(start, start + np.timedelta64(1, "D"), np.timedelta64(1, "h"))
    lons = np.arange(-180, 180, 60)      # 6 valori
    lats = np.arange(-60, 61, 30)        # 5 valori
    data = pymsis.calculate(dates, lons, lats, alts_km, geomagnetic_activity=-1)
    rho = data[..., idx]
    print("forma dell'array rho:", rho.shape)   # atteso: (24, 6, 5, 12)
    return rho.mean(axis=(0, 1, 2))

results = {}
for label, day in [("quiet", "2008-12-15"), ("active", "2014-04-15")]:
    results[label] = mean_density_profile(day)
    print(label, day)
    print(", ".join(f"{r:.2e}" for r in results[label]))

# salva anche in CSV (utile per il README e per la riproducibilità)
import csv, os
os.makedirs("../data", exist_ok=True)
with open("../data/density_table.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["altitude_km", "rho_quiet_kg_m3", "rho_active_kg_m3"])
    for a, q, ac in zip(alts_km, results["quiet"], results["active"]):
        w.writerow([int(a), f"{q:.3e}", f"{ac:.3e}"])
