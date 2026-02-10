# School Exam Result Calculator (GUI + Charts + PDF)

This project now includes a **full GUI interface** where users can:

- Enter student marks in an easy form
- Instantly calculate result summary
- View subject-level status in a table
- Generate a **PDF report**
- Include both **bar chart** and **pie chart** inside the PDF

## Features

- ✅ Desktop GUI using Tkinter
- ✅ Input validation (required, numeric, 0-100 range)
- ✅ Grade and converted marks based on original rule
- ✅ Subject-wise table view (`Raw`, `Converted`, `Status`)
- ✅ PDF export with:
  - Subject table
  - Bar chart (subject-wise raw marks)
  - Pie chart (performance distribution)

## Formula / grading

- Converted mark per subject: `(raw_mark * 70 / 100) + 30`
- Final grade (based on converted average):
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

This app uses:

- `tkinter` (usually built into Python)
- `matplotlib`
- `reportlab`

If needed, install missing packages:

```bash
pip install matplotlib reportlab
```
