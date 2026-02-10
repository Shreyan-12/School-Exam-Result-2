from __future__ import annotations

import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

SUBJECTS: List[str] = [
    "Bangla",
    "English",
    "Mathematics",
    "Science",
    "Historical and Social Science",
    "Digital Technology",
    "Life and Livelihood",
    "Art and Culture",
    "Wellbeing",
    "Religion",
]


@dataclass
class ResultData:
    student_name: str
    raw_marks: Dict[str, int]
    converted_marks: Dict[str, float]
    total_raw: int
    total_converted: float
    average_raw: float
    average_converted: float
    grade: str
    strongest: str
    weakest: str


def convert_mark(raw_mark: int) -> float:
    return (raw_mark * 70 / 100) + 30


def calculate_grade(converted_average: float) -> str:
    if converted_average >= 80:
        return "A+"
    if converted_average >= 70:
        return "A"
    if converted_average >= 60:
        return "B"
    if converted_average >= 50:
        return "C"
    if converted_average >= 40:
        return "D"
    return "F"


def build_result(student_name: str, marks: Dict[str, int]) -> ResultData:
    converted = {subject: convert_mark(mark) for subject, mark in marks.items()}
    total_raw = sum(marks.values())
    total_converted = sum(converted.values())
    average_raw = total_raw / len(SUBJECTS)
    average_converted = total_converted / len(SUBJECTS)
    strongest = max(marks, key=marks.get)
    weakest = min(marks, key=marks.get)

    return ResultData(
        student_name=student_name,
        raw_marks=marks,
        converted_marks=converted,
        total_raw=total_raw,
        total_converted=total_converted,
        average_raw=average_raw,
        average_converted=average_converted,
        grade=calculate_grade(average_converted),
        strongest=strongest,
        weakest=weakest,
    )


def _chart_files(result: ResultData, workdir: Path) -> Tuple[Path, Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    bar_file = workdir / "bar_chart.png"
    pie_file = workdir / "pie_chart.png"

    plt.figure(figsize=(10, 4.5))
    plt.bar(result.raw_marks.keys(), result.raw_marks.values(), color="#4F81BD")
    plt.ylim(0, 100)
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("Raw Marks")
    plt.title("Subject-wise Raw Marks")
    plt.tight_layout()
    plt.savefig(bar_file, dpi=140)
    plt.close()

    labels = ["Excellent (80+)", "Good (60-79)", "Needs Work (<60)"]
    excellent = sum(1 for m in result.raw_marks.values() if m >= 80)
    good = sum(1 for m in result.raw_marks.values() if 60 <= m < 80)
    needs_work = len(SUBJECTS) - excellent - good

    plt.figure(figsize=(6, 6))
    plt.pie(
        [excellent, good, needs_work],
        labels=labels,
        autopct="%1.0f%%",
        startangle=90,
        colors=["#4CAF50", "#FFC107", "#F44336"],
    )
    plt.title("Performance Distribution")
    plt.tight_layout()
    plt.savefig(pie_file, dpi=140)
    plt.close()

    return bar_file, pie_file


def export_pdf(result: ResultData, output_file: Path) -> None:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    with tempfile.TemporaryDirectory() as temp_dir:
        bar_chart, pie_chart = _chart_files(result, Path(temp_dir))

        doc = SimpleDocTemplate(str(output_file), pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("<b>School Exam Result Report</b>", styles["Title"]))
        story.append(Paragraph(f"Student: <b>{result.student_name}</b>", styles["Heading3"]))
        story.append(Spacer(1, 8))

        data = [["Subject", "Raw", "Converted"]]
        for subject in SUBJECTS:
            data.append([subject, str(result.raw_marks[subject]), f"{result.converted_marks[subject]:.2f}"])

        data.append(["Total", str(result.total_raw), f"{result.total_converted:.2f}"])
        data.append(["Average (%)", f"{result.average_raw:.2f}", f"{result.average_converted:.2f}"])

        table = Table(data, colWidths=[250, 90, 100])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E88E5")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, -2), (-1, -1), "Helvetica-Bold"),
                    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ]
            )
        )

        story.append(table)
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Final Grade: <b>{result.grade}</b>", styles["Heading3"]))
        story.append(
            Paragraph(
                f"Strongest Subject: <b>{result.strongest}</b> | Focus Subject: <b>{result.weakest}</b>",
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 10))

        story.append(Paragraph("<b>Bar Chart (Raw Marks)</b>", styles["Heading4"]))
        story.append(Image(str(bar_chart), width=470, height=210))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Pie Chart (Performance Distribution)</b>", styles["Heading4"]))
        story.append(Image(str(pie_chart), width=260, height=260))

        doc.build(story)


class ExamResultApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("School Exam Result Calculator - GUI")
        self.root.geometry("980x720")

        self.entries: Dict[str, tk.Entry] = {}
        self.current_result: ResultData | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        title = ttk.Label(self.root, text="School Exam Result Calculator", font=("Segoe UI", 18, "bold"))
        title.pack(pady=10)

        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=20)

        ttk.Label(top_frame, text="Student Name:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=4)
        self.student_name_entry = ttk.Entry(top_frame, width=40)
        self.student_name_entry.grid(row=0, column=1, sticky="w", padx=6)

        input_frame = ttk.LabelFrame(self.root, text="Enter Subject Marks (0-100)")
        input_frame.pack(fill="x", padx=20, pady=10)

        for i, subject in enumerate(SUBJECTS):
            row, col = divmod(i, 2)
            base_col = col * 2
            ttk.Label(input_frame, text=f"{subject}:").grid(row=row, column=base_col, sticky="w", padx=8, pady=4)
            entry = ttk.Entry(input_frame, width=12)
            entry.grid(row=row, column=base_col + 1, sticky="w", padx=8, pady=4)
            self.entries[subject] = entry

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=20, pady=8)

        ttk.Button(button_frame, text="Calculate Result", command=self.calculate).pack(side="left", padx=4)
        ttk.Button(button_frame, text="Export PDF", command=self.export_current_pdf).pack(side="left", padx=4)
        ttk.Button(button_frame, text="Reset", command=self.reset).pack(side="left", padx=4)

        self.summary_label = ttk.Label(self.root, text="", font=("Segoe UI", 11, "bold"), foreground="#0D47A1")
        self.summary_label.pack(anchor="w", padx=24, pady=6)

        columns = ("subject", "raw", "converted", "status")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings", height=13)
        self.table.heading("subject", text="Subject")
        self.table.heading("raw", text="Raw")
        self.table.heading("converted", text="Converted")
        self.table.heading("status", text="Status")
        self.table.column("subject", width=360)
        self.table.column("raw", width=90, anchor="e")
        self.table.column("converted", width=120, anchor="e")
        self.table.column("status", width=120, anchor="center")
        self.table.pack(fill="both", expand=True, padx=20, pady=6)

    def _validate_inputs(self) -> Tuple[str, Dict[str, int]] | None:
        student = self.student_name_entry.get().strip()
        if not student:
            messagebox.showerror("Missing Name", "Please enter a student name.")
            return None

        marks: Dict[str, int] = {}
        for subject in SUBJECTS:
            raw = self.entries[subject].get().strip()
            if not raw:
                messagebox.showerror("Missing Mark", f"Please enter marks for {subject}.")
                return None
            if not raw.isdigit():
                messagebox.showerror("Invalid Mark", f"{subject}: enter a whole number between 0 and 100.")
                return None
            mark = int(raw)
            if not 0 <= mark <= 100:
                messagebox.showerror("Out of Range", f"{subject}: mark must be between 0 and 100.")
                return None
            marks[subject] = mark

        return student, marks

    def calculate(self) -> None:
        validated = self._validate_inputs()
        if validated is None:
            return

        student, marks = validated
        result = build_result(student, marks)
        self.current_result = result

        for item in self.table.get_children():
            self.table.delete(item)

        for subject in SUBJECTS:
            raw = result.raw_marks[subject]
            converted = result.converted_marks[subject]
            status = "Excellent" if raw >= 80 else "Good" if raw >= 60 else "Needs Work"
            self.table.insert("", "end", values=(subject, raw, f"{converted:.2f}", status))

        self.summary_label.config(
            text=(
                f"Grade: {result.grade}   |   Average: {result.average_raw:.2f}%   |   "
                f"Converted Avg: {result.average_converted:.2f}%   |   "
                f"Strongest: {result.strongest}   |   Focus: {result.weakest}"
            )
        )

    def export_current_pdf(self) -> None:
        if self.current_result is None:
            messagebox.showwarning("No Result", "Calculate result first, then export PDF.")
            return

        default_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", self.current_result.student_name.lower()).strip("_")
        default_name = default_name or "student"

        output_path = filedialog.asksaveasfilename(
            title="Save PDF Report",
            defaultextension=".pdf",
            initialfile=f"result_{default_name}.pdf",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not output_path:
            return

        try:
            export_pdf(self.current_result, Path(output_path))
            messagebox.showinfo("Success", f"PDF report generated successfully:\n{output_path}")
        except ModuleNotFoundError:
            messagebox.showerror(
                "Missing Dependency",
                "PDF/chart export requires matplotlib and reportlab.\nInstall with: pip install matplotlib reportlab",
            )
        except OSError as err:
            messagebox.showerror("Export Failed", f"Could not generate PDF:\n{err}")

    def reset(self) -> None:
        self.student_name_entry.delete(0, tk.END)
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        for item in self.table.get_children():
            self.table.delete(item)
        self.summary_label.config(text="")
        self.current_result = None


def main() -> None:
    root = tk.Tk()
    ExamResultApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
