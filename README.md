# 🎮 School Exam Result Calculator (Gaming Vibe GUI)

This project now has a **fully gaming-vibe desktop GUI** with:

- 💜 Violet themed interface
- 😍 Attractive emojis throughout UI
- 📊 Subject result table with status badges
- 🧾 PDF export support
- 📉 Bar chart + 🥧 Pie chart in PDF report

## Features

- 🕹️ Interactive Tkinter GUI form
- ✅ Input validation (required, numeric, 0-100)
- 🧠 Original conversion and grade logic preserved
- 🏆 Instant summary: grade, average, strongest, focus subject
- 🎨 Gaming style color palette (dark violet + neon accents)

## PDF report includes

- Student details and result table
- Bar chart for subject-wise raw marks
- Pie chart for performance distribution

## Grading rules

- Converted mark per subject: `(raw_mark * 70 / 100) + 30`
- Final grade based on converted average:
  - `80+` → `A+`
  - `70+` → `A`
  - `60+` → `B`
  - `50+` → `C`
  - `40+` → `D`
  - `<40` → `F`

## Run

```bash
python3 grade.py
```

## Dependencies

- `tkinter` (usually included with Python)
- `matplotlib`
- `reportlab`

Install if needed:

```bash
pip install matplotlib reportlab
```
