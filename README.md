# The World in One Day — Thursday 26 November 2026

![rank](https://make.fun/badge/news-image-20261126.svg)
![rank](https://make.fun/badge/news-image-20261126/Cm11w/news-image-20261126/rank.svg)
![reward](https://make.fun/badge/news-image-20261126/Cm11w/news-image-20261126/reward.svg)

A single 1024×1024 front page that sums up Thursday 26 November 2026:
**29 stories from 7 regions, all from this one day** — the layout of the
22 November rank-1 entry, rebuilt for 26 November.

- **3 hero cards** (Macy's Thanksgiving Day Parade postponed in a 100-year
  first · Houthis claim a strike on Saudi Arabia's Ras Tanura refinery ·
  Ukraine drones hit the Nevinnomyssk power plant), **10 more illustrated
  cards**, a **THE DAY IN NUMBERS** panel (343 · 2,319 · 80M · 65 · 100 ·
  76%), a **UTC timeline**, **ALSO ON 26 NOVEMBER** (stories 14–29), a
  dotted **world map with pins 1–13**, a **DATE CHECK** strip listing the
  big stories deliberately left out because they happened on an earlier day
  (Miss Universe, Cairo tanker fire, the US tariff list, …), and a
  **HOW SURE** legend. Every scene is a drawn flat illustration, never a
  photograph.

## How it is built

`draw.py` (Python + PIL, run locally) renders `entry.png` from the 29
stories in its data tables — each story verified against a source dated
26 November 2026 (see `research-26nov.md`). `main.ts` (Node) copies the
committed `entry.png` to `/output/entry.png` and verifies the PNG
signature. No network, no randomness, no clock: every run writes the same
bytes (sha256 `9f4285068f11704de0683a0662ac949a0b46df40208a31e24d5d484dbef7479b`).

```sh
python3 draw.py            # regenerate entry.png (1024x1024, ~216 KB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # write out/entry.png
```

## Competition

[news-image-20261126](https://make.fun) — $100, free entry, final deadline
28 November 2026 07:00 WIB.
