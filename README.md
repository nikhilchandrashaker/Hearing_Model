# Cumulative Noise Exposure and the Ears

An interactive, single-file HTML visualization of how loud noise over time can damage
hearing. Three sliders (sound level, hours per day, years) plus a hearing-protection
toggle drive a cochlea illustration and an audiogram.

**Files**
- `noise_ear_model.html`: the interactive. Open in any browser, no build step.
- `noise_dataset.csv`: 2,500-row **synthetic** dataset in the same spirit as `health_dataset.csv`.
- `make_noise_dataset.py`: the generator, so every assumption is inspectable.

## What it does

- Daily dose follows the NIOSH convention: 85 dBA for 8 hours = 100%, and every +3 dB
  halves the safe time. Dose % = (hours ÷ 8) × 2^((level − 85) / 3) × 100.
- Noise-years = daily dose ÷ 100 × years.
- Injury `f = 1 − e^(−noise-years / 15)`, fast early, flattening later.
- Loss at 4 kHz = 50f dB above a 5 dB baseline. Other frequencies scale by a fixed
  profile that peaks at 4 kHz, mimicking the classic noise-induced "notch".
- Hair cells lost = 0.8f, shown as dots dying from the high-pitch outer end of the
  spiral inward.
- Hearing protection subtracts 15 dB when the level is 85 or above.
- The stats show daily dose, safe time at the chosen level, estimated 4 kHz loss and
  hair cells lost.

## Design note: model vs. data, kept separate on purpose

The 85 dBA / 8 h / 3 dB exchange-rate rule is a real occupational standard. The
direction of the effect (louder and longer means more loss, starting around 4 kHz)
matches general audiology knowledge. The specific constants (15, 50, 0.8, the frequency
profile) are **my illustrative choices**, not fitted to any study. The model ignores age,
genetics, medications and sudden loud events.

`noise_dataset.csv` is **fully synthetic**, with a dose-response built in plus small
effects from age, headphone volume and family history. Each row has a simulated 4 kHz
hearing threshold, and "Damaged" means above 25 dB. The panel shows what the generator
does, not evidence about real people.

| Exposure | Level | Damaged | Total | Rate | Mean 4 kHz |
|---|---|---|---|---|---|
| Quiet | 60–75 dB | 22 | 754 | 2.9% | 10.5 dB |
| Moderate | 76–85 dB | 154 | 751 | 20.5% | 17.7 dB |
| Loud | 86–100 dB | 393 | 667 | 58.9% | 35.6 dB |
| Very Loud | 101+ dB | 315 | 328 | 96.0% | 55.9 dB |

The relationship saturates, so the linear correlation of noise-years with threshold is
only r ≈ 0.34, but on a log scale (log of 1 + noise-years) it is r ≈ 0.89.

## Dataset columns

Patient_ID, Age, Gender, Noise_Exposure (Quiet, Moderate, Loud, Very Loud), Avg_Noise_dB,
Hours_Per_Day, Years_Exposed, Hearing_Protection, Daily_Dose_Pct, Noise_Years,
Threshold_4kHz_dB, Ear_Condition (Healthy or Damaged), Headphone_Volume,
Family_History_Risk.

## Caveats

Illustrative and educational only, not medical advice. Anyone worried about their own
hearing should see an audiologist or doctor.

## Possible next steps

- [ ] Replace the synthetic file with a real occupational-health dataset
- [ ] Add a sudden-blast (impulse noise) mode
- [ ] Add tinnitus risk as a second outcome
