"""Generate a SYNTHETIC noise-exposure-and-hearing dataset (same spirit as health_dataset.csv).
Dose-response is built in on purpose (qualitative direction only: more cumulative noise
dose -> higher hearing threshold at 4 kHz). Effect sizes are illustrative, not fitted.
Noise dose uses the NIOSH convention: 85 dBA for 8 h = 100% daily dose, 3 dB exchange rate."""
import numpy as np, pandas as pd
rng = np.random.default_rng(23); N = 2500
age = np.clip(rng.normal(42, 15, N).round(), 18, 89).astype(int)
gender = rng.choice(["Male", "Female"], N)
cat = rng.choice(["Quiet", "Moderate", "Loud", "Very Loud"], N, p=[.30, .30, .28, .12])
rng_db = {"Quiet": (60, 75), "Moderate": (76, 85), "Loud": (86, 100), "Very Loud": (101, 115)}
db = np.array([rng.integers(*rng_db[c]) for c in cat])
hours = np.clip(rng.gamma(3, 1.3, N).round(1), 0.5, 12)
years = np.array([int(min(rng.integers(1, 36), max(age[i] - 16, 1))) for i in range(N)])
prot = rng.choice(["No", "Yes"], N, p=[.65, .35])
prot = np.where(db < 85, "No", prot)
eff = db - np.where(prot == "Yes", 15, 0)
dose = np.round(hours / 8 * 2 ** ((eff - 85) / 3) * 100, 1)       # daily dose %
ny = np.round(dose / 100 * years, 1)                              # noise-years
phones = rng.choice(["Low", "Moderate", "High"], N, p=[.4, .4, .2])
fam = rng.choice(["No", "Yes"], N, p=[.8, .2])
thr = (5 + .22 * np.maximum(age - 30, 0)
       + 50 * (1 - np.exp(-ny / 15))
       + np.array([{"Low": 0, "Moderate": 1.5, "High": 4}[p] for p in phones])
       + 4 * (fam == "Yes") + rng.normal(0, 6, N))
thr = np.clip(thr, -5, 90).round(1)
df = pd.DataFrame({"Patient_ID": np.arange(1, N+1), "Age": age, "Gender": gender,
    "Noise_Exposure": cat, "Avg_Noise_dB": db, "Hours_Per_Day": hours, "Years_Exposed": years,
    "Hearing_Protection": prot, "Daily_Dose_Pct": dose, "Noise_Years": ny,
    "Threshold_4kHz_dB": thr, "Ear_Condition": np.where(thr > 25, "Damaged", "Healthy"),
    "Headphone_Volume": phones, "Family_History_Risk": fam})
df.to_csv("noise_dataset.csv", index=False)
print(df.groupby("Noise_Exposure").Ear_Condition.agg(lambda s: [int((s=="Damaged").sum()), len(s)]).to_dict())
print(df.groupby("Noise_Exposure").Threshold_4kHz_dB.mean().round(1).to_dict())
print("r(Noise_Years,thr) =", round(np.corrcoef(df.Noise_Years, df.Threshold_4kHz_dB)[0,1], 3),
      " r(log1p NY,thr) =", round(np.corrcoef(np.log1p(df.Noise_Years), df.Threshold_4kHz_dB)[0,1], 3))
