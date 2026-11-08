# Age reporting in curated circadian transcriptome datasets

Coded table, coding protocol and analysis code for the manuscript
*"Age is reported but rarely usable: an audit of animal and donor age in curated
circadian transcriptome datasets"* (submitted).

## What this is

That circadian rhythms change with age is tested, in practice, by comparing time
courses across studies, which requires knowing how old the animals or donors were.

Every entry of CircaKB was read manually and coded for **where** the age is
recorded, **in what form** it is expressed, and **to what moment** it refers.
Collapsing database rows to deposited series gives 54 GEO series plus one
ArrayExpress entry; 48 series have age as an applicable attribute.

Headline result: age is present in the deposited record for 23% of those series,
is expressed in eleven distinct forms, and is usable for comparison between
studies in 17%.

The coded table is **original data**. It records readings of public GEO records and
their publications that did not exist in machine-readable form before. The
underlying GEO records are public and can be inspected independently; this
repository records how each one was read.

## Contents

| Path | What it is |
|---|---|
| `data/circadian_age_audit.xlsx` | the coded table, one row per deposited series, with the protocol and the computed summary on separate sheets |
| `protocol/protocol.md` | the coding protocol in English, with the dated revision log: every rule, the dataset that prompted it, and two codings later withdrawn as errors |
| `analyze.py` | reads the table and regenerates every number, the table and all three figures of the manuscript |
| `results.json` | the computed values, for checking the manuscript text against the data |
| `figures/` | the three figures as submitted, 300 dpi |

No number in the manuscript is typed by hand. All are produced by `analyze.py`
from the coded table.

## Reproducing the analysis

```
pip install -r requirements.txt
python analyze.py
```

This rewrites `results.json` and the three figures in `figures/`. Expected output:

```
n applicable: 48 | not machine-readable: 37 (77.1%)
usable for comparison: 8 (16.7%)
forms: 11 | width n=31 median=2 max=52.2
mouse 33 (in GEO 8) | human 9 (in GEO 2)
```

Tested with Python 3.13. The script has no network access and needs none: the
coded table is the input.

## A note on language

The coding sheet was kept in Russian, so the category labels inside the table and
in the code are Russian strings. They are the literal cell values and must match
the table exactly. `protocol/protocol.md` is the English rendering of the protocol,
and `FORM_EN` in `analyze.py` maps each category to the wording used in the
manuscript.

## Coding protocol and its history

Categories were not specified in advance. Each was added when a record failed to
fit the existing set, and five of the eleven occurred exactly once.

Because the coding was done by one person, the revision log matters as much as the
rules: it shows the date of each rule and the dataset that forced it, so a reader
can see that rules followed cases rather than results. Two codings were entered,
used, and later withdrawn as errors; both are recorded rather than quietly
repaired.

## Licence

Code: MIT. Data and protocol: CC BY 4.0.

## Citation

<!-- Zenodo DOI badge goes here after the first release -->
cff-version: 1.1.0
message: "If you use this software, please cite it as below."
authors:
- family-names: Kuatov
  given-names: Rassul
orcid: https://orcid.org/0009-0004-2879-5316
title:RassulKuatov/circadian-age-audit: v1.0.0 — manuscript submission
version: v1.0.0
date-released: 2026-11-08
