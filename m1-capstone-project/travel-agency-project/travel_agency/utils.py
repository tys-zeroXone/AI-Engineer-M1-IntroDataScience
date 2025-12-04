import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime, date
from typing import Sequence, List, Any, Iterable, Optional
from openpyxl import Workbook

from rich.console import Console
from rich.table import Table

console = Console()

# Palet warna korporat untuk semua visualisasi
CORPORATE_COLORS = {
    "primary": "#0052CC",
    "secondary": "#172B4D",
    "accent": "#36B37E",
    "muted": "#97A0AF",
}


# =========================================================
# HELPER UMUM
# =========================================================

def timestamp() -> str:
    """Return timestamp string untuk nama file, dll."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def input_optional(prompt: str) -> str:
    """Input biasa, boleh kosong."""
    return console.input(prompt).strip()


def input_yes_no(prompt: str, default: bool = False) -> bool:
    """Helper input yes/no → bool."""
    suffix = "[Y/n]" if default else "[y/N]"
    raw = console.input(f"{prompt} {suffix} ").strip().lower()
    if not raw:
        return default
    return raw.startswith("y")


def parse_int(value: str) -> Optional[int]:
    """
    Parse bilangan bulat.
    - Jika input kosong (user tekan Enter) -> return None tanpa warning
    - Jika diisi tetapi bukan integer -> tampilkan warning dan return None
    """
    raw = (value or "").strip()
    if raw == "":
        return None

    try:
        return int(raw)
    except ValueError:
        console.print(
            f"[yellow]Nilai bukan bilangan bulat yang valid: {raw}[/yellow]"
        )
        return None


def parse_date(value: str) -> Optional[date]:
    """
    Parse tanggal format YYYY-MM-DD.
    - Jika input kosong (user tekan Enter) -> langsung return None tanpa warning
    - Jika diisi tetapi format salah -> tampilkan warning dan return None
    """
    # Jika user tidak isi apa-apa, kembalikan None tanpa pesan
    raw = (value or "").strip()
    if raw == "":
        return None

    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        console.print(
            f"[yellow]Format tanggal tidak valid: {raw} (gunakan YYYY-MM-DD)[/yellow]"
        )
        return None


# =========================================================
# TABEL & PAGINATION (RICH.TABLE)
# =========================================================

def _show_table(
    title: str,
    headers: Sequence[str],
    rows: Iterable[Sequence[Any]],
    page_size: int = 20,
) -> bool:
    """
    Tampilkan table dengan Rich + pagination sederhana.
    Return True kalau ada data, False kalau rows kosong.
    """
    rows = list(rows)
    total = len(rows)

    if total == 0:
        console.print("[yellow]Tidak ada data untuk ditampilkan.[/yellow]")
        return False

    current_start = 0
    while current_start < total:
        current_end = min(current_start + page_size, total)
        page = rows[current_start:current_end]

        page_title = (
            f"{title} (Rows {current_start+1}–{current_end} dari {total})"
            if total > page_size
            else title
        )

        table = Table(
            title=page_title,
            show_header=True,
            header_style="bold cyan",
            show_lines=False,
        )

        for h in headers:
            table.add_column(h, overflow="fold")

        for r in page:
            table.add_row(
                *[("" if v is None else str(v)) for v in r]
            )

        console.print("\n")
        console.print(table)

        if current_end >= total:
            break

        choice = console.input(
            "\n[dim]Tekan Enter untuk melihat halaman berikutnya, atau ketik 'q' untuk berhenti lihat:[/dim] "
        ).strip().lower()
        if choice == "q":
            break

        current_start = current_end

    return True


# =========================================================
# EXPORT → EXCEL
# =========================================================

def _export_to_excel(headers, rows, base_name="export"):
    from openpyxl import Workbook
    from datetime import datetime
    import os

    wb = Workbook()
    ws = wb.active
    ws.append(headers)

    for row in rows:
        ws.append(row)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Ensure exports folder exists
    export_dir = "exports"
    os.makedirs(export_dir, exist_ok=True)

    filename = os.path.join(export_dir, f"export_{base_name}_{timestamp}.xlsx")

    wb.save(filename)

    console.print(f"\n✅ File berhasil dibuat: {filename}", markup=False)


# =========================================================
# HELPER VISUALISASI (MATPLOTLIB)
# =========================================================

def _create_figure(title: str, figsize=(10, 5)):
    """
    Helper standar untuk membuat figure matplotlib dengan gaya korporat.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontsize=12, fontweight="bold", color=CORPORATE_COLORS["secondary"])
    return fig, ax


def _format_axis(
    ax,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    grid_y: bool = True,
    rotate_xticks: bool = False,
):
    """
    Format axis: label, grid, dan tampilan x-tick.
    """
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    if grid_y:
        ax.grid(True, axis="y", alpha=0.3)

    if rotate_xticks:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha("right")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
