from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


@dataclass(frozen=True)
class PdfStyle:
    page_size: tuple[float, float] = (8.27, 11.69)
    margin_left: float = 0.07
    margin_right: float = 0.07
    margin_top: float = 0.06
    margin_bottom: float = 0.06
    line_height: float = 0.030
    font_family: str = "DejaVu Sans"


def markdown_to_pdf(
    markdown_path: Path,
    output_pdf_path: Path,
    *,
    style: PdfStyle | None = None,
) -> Path:
    style = style or PdfStyle()
    text = markdown_path.read_text(encoding="utf-8").splitlines()

    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    def new_page() -> tuple[plt.Figure, plt.Axes, float]:
        fig = plt.figure(figsize=style.page_size)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        y = 1.0 - style.margin_top
        return fig, ax, y

    def draw_line(ax: plt.Axes, y: float, line: str, *, size: int, weight: str = "normal") -> float:
        ax.text(
            style.margin_left,
            y,
            line,
            fontsize=size,
            fontweight=weight,
            family=style.font_family,
            va="top",
            ha="left",
            wrap=True,
        )
        return y - style.line_height

    def wrap_lines(s: str, max_chars: int) -> list[str]:
        if not s.strip():
            return [""]
        return wrap(s, width=max_chars, break_long_words=False, replace_whitespace=False)

    def max_chars_for_font(size: int) -> int:
        if size >= 18:
            return 68
        if size >= 14:
            return 88
        return 104

    with PdfPages(output_pdf_path) as pdf:
        fig, ax, y = new_page()

        for raw in text:
            line = raw.rstrip("\n")

            if y < style.margin_bottom:
                pdf.savefig(fig)
                plt.close(fig)
                fig, ax, y = new_page()

            if line.startswith("# "):
                y = draw_line(ax, y, line[2:].strip(), size=20, weight="bold")
                y -= style.line_height * 0.3
                continue

            if line.startswith("## "):
                y = draw_line(ax, y, line[3:].strip(), size=16, weight="bold")
                y -= style.line_height * 0.15
                continue

            if line.startswith("### "):
                y = draw_line(ax, y, line[4:].strip(), size=13, weight="bold")
                continue

            if line.startswith("- "):
                bullet = "• " + line[2:].strip()
                for wline in wrap_lines(bullet, max_chars_for_font(11)):
                    y = draw_line(ax, y, wline, size=11)
                continue

            if not line.strip():
                y -= style.line_height * 0.6
                continue

            for wline in wrap_lines(line, max_chars_for_font(11)):
                y = draw_line(ax, y, wline, size=11)

        pdf.savefig(fig)
        plt.close(fig)

    return output_pdf_path

