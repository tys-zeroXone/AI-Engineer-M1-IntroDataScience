from mysql.connector import Error

from rich.console import Console
from rich.panel import Panel

from .utils import _export_to_excel
from . import maintenance

console = Console()



# ===== EXPORT CITIES =====
def export_cities(conn):
    """
    Export data master kota:
    - Cari data dengan maintenance._search_cities
    - Tampilkan hasil (ditangani oleh fungsi search)
    - Tanya konfirmasi, lalu export ke Excel jika ya
    """
    try:
        console.clear()
        console.print("\n")
        header_panel = Panel.fit(
            "[bold magenta]Export Data Master Kota[/bold magenta]",
            border_style="magenta",
        )
        console.print(header_panel, justify="center")

        rows = maintenance._search_cities(conn)

        if not rows:
            return

        # Setelah hasil pencarian tampil, tanya konfirmasi export
        confirm = console.input(
            "\n[bold cyan]Ingin export hasil pencarian ke Excel? (y/n): [/bold cyan]"
        ).strip().lower()

        if confirm != "y":
            console.print("[dim]Export dibatalkan.[/dim]")
            return

        headers = [
            "ID Kota",
            "Kode Kota",
            "Nama Kota",
            "Kode Negara",
            "Nama Negara",
        ]

        _export_to_excel(headers, rows, base_name="cities")

    except Error as e:
        console.print(f"[red]Error export cities:[/red] {e}")


# ===== EXPORT USERS =====
def export_users(conn):
    """
    Export data pengguna:
    - Cari data dengan maintenance._search_users
    - Tampilkan hasil
    - Tanya konfirmasi, lalu export ke Excel jika ya
    """
    try:
        console.clear()
        console.print("\n")
        header_panel = Panel.fit(
            "[bold magenta]Export Data Pengguna[/bold magenta]",
            border_style="magenta",
        )
        console.print(header_panel, justify="center")

        rows = maintenance._search_users(conn)

        if not rows:
            return

        confirm = console.input(
            "\n[bold cyan]Ingin export hasil pencarian ke Excel? (y/n): [/bold cyan]"
        ).strip().lower()

        if confirm != "y":
            console.print("[dim]Export dibatalkan.[/dim]")
            return

        headers = [
            "ID",
            "Nama",
            "Jenis Kelamin",
            "Tanggal Lahir",
            "Status",
            "Pekerjaan",
            "Perusahaan",
            "Dibuat",
        ]

        _export_to_excel(headers, rows, base_name="users")

    except Error as e:
        console.print(f"[red]Error export users:[/red] {e}")


# ===== EXPORT AIRLINES =====
def export_airlines(conn):
    """
    Export data maskapai:
    - Cari data dengan maintenance._search_airlines
    - Tampilkan hasil
    - Tanya konfirmasi, lalu export ke Excel jika ya
    """
    try:
        console.clear()
        console.print("\n")
        header_panel = Panel.fit(
            "[bold magenta]Export Data Maskapai[/bold magenta]",
            border_style="magenta",
        )
        console.print(header_panel, justify="center")

        rows = maintenance._search_airlines(conn)

        if not rows:
            return

        confirm = console.input(
            "\n[bold cyan]Ingin export hasil pencarian ke Excel? (y/n): [/bold cyan]"
        ).strip().lower()

        if confirm != "y":
            console.print("[dim]Export dibatalkan.[/dim]")
            return

        headers = [
            "ID",
            "Kode",
            "Nama Maskapai",
            "Negara",
        ]

        _export_to_excel(headers, rows, base_name="airlines")

    except Error as e:
        console.print(f"[red]Error export airlines:[/red] {e}")


# ===== EXPORT FLIGHTS =====
def export_flights(conn):
    """
    Export data penerbangan:
    - Cari data dengan maintenance._search_flights
    - Tampilkan hasil
    - Tanya konfirmasi, lalu export ke Excel jika ya
    """
    try:
        console.clear()
        console.print("\n")
        header_panel = Panel.fit(
            "[bold magenta]Export Data Penerbangan[/bold magenta]",
            border_style="magenta",
        )
        console.print(header_panel, justify="center")

        rows = maintenance._search_flights(conn)

        if not rows:
            return

        confirm = console.input(
            "\n[bold cyan]Ingin export hasil pencarian ke Excel? (y/n): [/bold cyan]"
        ).strip().lower()

        if confirm != "y":
            console.print("[dim]Export dibatalkan.[/dim]")
            return

        headers = [
            "ID",
            "Dari Kota",
            "Ke Kota",
            "Maskapai",
            "Tipe",
            "Arah",
            "Harga (usd)",
            "Tanggal",
        ]

        _export_to_excel(headers, rows, base_name="flights")

    except Error as e:
        console.print(f"[red]Error export flights:[/red] {e}")


# ===== EXPORT HOTELS =====
def export_hotels(conn):
    """
    Export data hotel:
    - Cari data dengan maintenance._search_hotels
    - Tampilkan hasil
    - Tanya konfirmasi, lalu export ke Excel jika ya
    """
    try:
        console.clear()
        console.print("\n")
        header_panel = Panel.fit(
            "[bold magenta]Export Data Hotel[/bold magenta]",
            border_style="magenta",
        )
        console.print(header_panel, justify="center")

        rows = maintenance._search_hotels(conn)

        if not rows:
            return

        confirm = console.input(
            "\n[bold cyan]Ingin export hasil pencarian ke Excel? (y/n): [/bold cyan]"
        ).strip().lower()

        if confirm != "y":
            console.print("[dim]Export dibatalkan.[/dim]")
            return

        headers = [
            "ID",
            "Nama Hotel",
            "Kota",
            "Negara",
            "Harga/Malam (usd)",
            "Star",
            "Tgl Berdiri",
        ]

        _export_to_excel(headers, rows, base_name="hotels")

    except Error as e:
        console.print(f"[red]Error export hotels:[/red] {e}")


# ===== EXPORT TRIPS =====
def export_trips(conn):
    """
    Export data perjalanan:
    - Cari data dengan maintenance._search_trips
    - Tampilkan hasil
    - Tanya konfirmasi, lalu export ke Excel jika ya
    """
    try:
        console.clear()
        console.print("\n")
        header_panel = Panel.fit(
            "[bold magenta]Export Data Perjalanan[/bold magenta]",
            border_style="magenta",
        )
        console.print(header_panel, justify="center")

        rows = maintenance._search_trips(conn)

        if not rows:
            return

        confirm = console.input(
            "\n[bold cyan]Ingin export hasil pencarian ke Excel? (y/n): [/bold cyan]"
        ).strip().lower()

        if confirm != "y":
            console.print("[dim]Export dibatalkan.[/dim]")
            return

        headers = [
            "ID Perjalanan",
            "Nama Pengguna",
            "Kota Tujuan",
            "Mulai",
            "Selesai",
            "Status",
            "Total Biaya",
        ]

        _export_to_excel(headers, rows, base_name="trips")

    except Error as e:
        console.print(f"[red]Error export trips:[/red] {e}")
