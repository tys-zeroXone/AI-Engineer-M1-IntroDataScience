from rich.console import Console
from rich.panel import Panel

from .db import get_connection
from . import reports
from . import visualizations as viz
from . import maintenance
from . import trips
from . import exports

console = Console()


class TravelAgencyApp:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = get_connection()
        if self.connection:
            console.print("\n[green]✅ Berhasil terhubung ke database[/green]")
        else:
            console.print("[red]❌ Gagal terhubung ke database[/red]")

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            console.print("[yellow]🔌 Koneksi ke database ditutup.[/yellow]")

    # =========================================================
    # MAIN MENU
    # =========================================================
    def main_menu(self):
        self.connect()
        if not self.connection:
            return

        while True:
            console.clear()
            console.print("\n")
            header = Panel.fit(
                "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
                subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
                border_style="cyan",
            )
            console.print(header, justify="center")

            menu_panel = Panel(
                "\n".join(
                    [
                        "[bold white][1][/bold white] Pencarian Data Master",
                        "[bold white][2][/bold white] Pengelolaan Data Master",
                        "[bold magenta][3] Pengelolan Transaksi Pemesanan Perjalanan[/bold magenta]",
                        "[bold magenta][4] Laporan & Ringkasan[/bold magenta]",
                        "[bold magenta][5] Visualisasi Data[/bold magenta]",
                        "[bold white][6][/bold white] Export Data Master dan Transaksi",
                        "",
                        "[bold white][0][/bold white] Keluar Aplikasi",
                        "",
                        "[dim]powered by Purwadhika - Digital Technology School[/dim]",
                    ]
                ),
                title="[bold green]Menu Utama[/bold green]",
                border_style="green",
            )
            console.print(menu_panel)

            choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ")

            if choice == "1":
                self.view_database_menu()
            elif choice == "2":
                self.manage_database_menu()
            elif choice == "3":
                self.trip_management_menu()
            elif choice == "4":
                self.reports_menu()
            elif choice == "5":
                self.visualize_menu()
            elif choice == "6":
                self.export_menu()
            elif choice == "0":
                break
            else:
                console.print("[red]Pilihan tidak valid, silakan coba lagi.[/red]")
                console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

        self.close()

    # =========================================================
    # SUBMENU 1: MENCARI & MENAMPILKAN DATABASE
    # =========================================================
    def view_database_menu(self):
        while True:
            console.clear()

            console.print("\n")
            header = Panel.fit(
                "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
                subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
                border_style="cyan",
            )
            console.print(header, justify="center")

            menu_panel = Panel(
                "\n".join(
                    [
                        "[bold white][1][/bold white] Pencarian Data Perjalanan",
                        "[bold white][2][/bold white] Pencarian Data Penerbangan",
                        "[bold white][3][/bold white] Pencarian Data Hotel",
                        "[bold white][4][/bold white] Pencarian Data Pengguna",
                        "[bold white][5][/bold white] Pencarian Data Maskapai",
                        "[bold white][6][/bold white] Pencarian Data Kota",
                        "",
                        "[bold white][0][/bold white] Kembali ke Menu Utama",
                        "",
                        "[dim]powered by Purwadhika - Digital Technology School[/dim]",
                    ]
                ),
                title="[bold green]Menu Menampilkan Data Master dan Transaksi[/bold green]",
                border_style="green",
            )
            console.print(menu_panel)

            choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()

            if choice == "1":

                console.print("\n")
                header = Panel.fit(
                    "[bold magenta]Menampilkan Perjalanan[/bold magenta]",
                    border_style="magenta",
                )
                console.print(header, justify="center")
                console.print("\n")

                maintenance._search_trips(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "2":

                console.print("\n")
                header = Panel.fit(
                    "[bold magenta]Menampilkan Penerbangan[/bold magenta]",
                    border_style="magenta",
                )
                console.print(header, justify="center")
                console.print("\n")

                maintenance._search_flights(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "3":

                console.print("\n")
                header = Panel.fit(
                    "[bold magenta]Menampilkan Hotel[/bold magenta]",
                    border_style="magenta",
                )
                console.print(header, justify="center")
                console.print("\n")

                maintenance._search_hotels(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "4":

                console.print("\n")
                header = Panel.fit(
                    "[bold magenta]Menampilkan Pengguna[/bold magenta]",
                    border_style="magenta",
                )
                console.print(header, justify="center")
                console.print("\n")

                maintenance._search_users(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "5":

                console.print("\n")
                header = Panel.fit(
                    "[bold magenta]Menampilkan Maskapai[/bold magenta]",
                    border_style="magenta",
                )
                console.print(header, justify="center")
                console.print("\n")

                maintenance._search_airlines(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "6":

                console.print("\n")
                header = Panel.fit(
                    "[bold magenta]Menampilkan Kota[/bold magenta]",
                    border_style="magenta",
                )
                console.print(header, justify="center")
                console.print("\n")

                maintenance._search_cities(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")    
            elif choice == "0":
                break
            else:
                console.print("[red]Pilihan tidak valid, silakan coba lagi.[/red]")
                console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

    # =========================================================
    # SUBMENU 2: PERUBAHAN DATABASE
    # =========================================================
    def manage_database_menu(self):
        while True:
            console.clear()

            console.print("\n")
            header = Panel.fit(
            "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
            subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
            border_style="cyan",
            )
            console.print(header, justify="center")

            menu_panel = Panel(
                "\n".join(
                    [
                        "[bold white][1][/bold white] Mengelola Data Master Penerbangan",
                        "[bold white][2][/bold white] Mengelola Data Master Hotel",
                        "[bold white][3][/bold white] Mengelola Data Master Pengguna",
                        "[bold white][4][/bold white] Mengelola Data Master Maskapai",
                        "[bold white][5][/bold white] Mengelola Data Master Kota",
                        
                        "",
                        "[bold white][0][/bold white] Kembali ke Menu Utama",
                        "",
                        "[dim]powered by Purwadhika - Digital Technology School[/dim]",
                    ]
                ),
                title="[bold green]Menu Pengelolaan Data Master dan Transaksi[/bold green]",
                border_style="green",
            )
            console.print(menu_panel)

            choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()

            if choice == "1":
                maintenance.manage_flights(self.connection)
            elif choice == "2":
                maintenance.manage_hotels(self.connection)
            elif choice == "3":
                maintenance.manage_users(self.connection)
            elif choice == "4":
                maintenance.manage_airlines(self.connection)
            elif choice == "5":
                maintenance.manage_cities(self.connection)
            elif choice == "0":
                break
            else:
                console.print("[red]Pilihan tidak valid, silakan coba lagi.[/red]")
                console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

    # =========================================================
    # SUBMENU 3: TRIP MANAGEMENT (NEW!)
    # =========================================================
    def trip_management_menu(self):
        while True:
            console.clear()

            console.print("\n")
            header = Panel.fit(
                "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
                subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
                border_style="cyan",
            )
            console.print(header, justify="center")

            menu_panel = Panel(
                "\n".join(
                    [
                        "[bold white][1][/bold white] Pemesanan Perjalanan Baru",
                        "[bold white][2][/bold white] Perubahan Perjalanan",
                        "",
                        "[bold white][0][/bold white] Kembali ke Menu Utama",
                        "",
                        "[dim]powered by Purwadhika - Digital Technology School[/dim]",
                    ]
                ),
                title="[bold green]Menu Transaksi Pemesanan Perjalanan[/bold green]",
                border_style="green",
            )
            console.print(menu_panel)

            choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()

            if choice == "1":
                trips.create_trip(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "2":
                trips.reschedule_trip(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "0":
                break
            else:
                console.print("[red]Pilihan tidak valid, silakan coba lagi.[/red]")
                console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

    # =========================================================
    # SUBMENU 4: MENAMPILKAN LAPORAN 
    # =========================================================
    def reports_menu(self):
        while True:
            console.clear()
            console.print("\n")
            header = Panel.fit(
                "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
                subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
                border_style="cyan",
            )
            console.print(header, justify="center")

            menu_panel = Panel(
                "\n".join(
                    [
                        "[bold white][1][/bold white] Rute Teratas berdasarkan Pendapatan",
                        "[bold white][2][/bold white] Destinasi Paling Populer",
                        "[bold white][3][/bold white] Rata-rata Pengeluaran per Pengguna",
                        "[bold white][4][/bold white] Maskapai dengan Pendapatan Tertinggi",
                        "[bold white][5][/bold white] Peringkat Hotel berdasarkan Penggunaan",
                        "[bold white][6][/bold white] Rata-rata Durasi Perjalanan per Destinasi",
                        "[bold white][7][/bold white] Pola Perjalanan Populer",
                        "[bold white][8][/bold white] Rata-rata Harga Tiket per Maskapai",
                        "[bold white][9][/bold white] Segmentasi Pengguna berdasarkan Profesi",
                        "[bold white][10][/bold white] Pendapatan Bulanan",
                        "",
                        "[bold white][0][/bold white] Kembali ke Menu Utama",
                        "",
                        "[dim]powered by Purwadhika - Digital Technology School[/dim]",
                    ]
                ),
                title="[bold green]Menu Laporan dan Ringkasan[/bold green]",
                border_style="green",
            )
            console.print(menu_panel)

            choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ")

            if choice == "1":
                reports.report_top_routes_by_revenue(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "2":
                reports.report_most_popular_destinations(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "3":
                reports.report_average_spend_per_user(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "4":
                reports.report_top_airlines_by_revenue(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "5":
                reports.report_hotel_occupancy(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "6":
                reports.report_average_trip_duration_per_destination(
                    self.connection
                )
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "7":
                reports.report_popular_city_pairs(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "8":
                reports.report_avg_flight_price_by_airline(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "9":
                reports.report_user_segmentation_by_occupation(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "10":
                reports.report_monthly_revenue(self.connection)
                console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
            elif choice == "0":
                break
            else:
                console.print("[red]Pilihan tidak valid, silakan coba lagi.[/red]")
                console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

    # =========================================================
    # SUBMENU 5: VISUALISASI DATA
    # =========================================================
    def visualize_menu(self):
        while True:
            console.clear()
            console.print("\n")
            header = Panel.fit(
                "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
                subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
                border_style="cyan",
            )
            console.print(header, justify="center")

            menu_panel = Panel(
                "\n".join(
                    [
                        "[bold white][1][/bold white] Ringkasan KPI Utama (Scorecard)",
                        "[bold white][2][/bold white] Rute Teratas berdasarkan Pendapatan",
                        "[bold white][3][/bold white] Destinasi Paling Populer",
                        "[bold white][4][/bold white] Tren Pendapatan Bulanan",
                        "",
                        "[bold white][0][/bold white] Kembali ke Menu Utama",
                        "",
                        "[dim]powered by Purwadhika - Digital Technology School[/dim]",
                    ]
                ),
                title="[bold green]Menu Dashboard[/bold green]",
                border_style="green",
            )
            console.print(menu_panel)

            choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ")

            if choice == "1":
                viz.viz_key_metrics_overview(self.connection)
            elif choice == "2":
                viz.viz_top_routes_by_revenue(self.connection)
            elif choice == "3":
                viz.viz_most_popular_destinations(self.connection)
            elif choice == "4":
                viz.viz_monthly_revenue(self.connection)
            elif choice == "0":
                break
            else:
                console.print("[red]Pilihan tidak valid, silakan coba lagi.[/red]")

            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")

    # =========================================================
    # SUBMENU 6: EXPORT DATA 
    # =========================================================
    def export_menu(self):
            while True:
                console.clear()
                console.print("\n")
                header = Panel.fit(
                "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
                subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
                border_style="cyan",
                )
                console.print(header, justify="center")

                menu_panel = Panel(
                    "\n".join(
                        [
                            "[bold white][1][/bold white] Export Data Perjalanan",
                            "[bold white][2][/bold white] Export Data Penerbangan",
                            "[bold white][3][/bold white] Export Data Hotel",
                            "[bold white][4][/bold white] Export Data Pengguna",
                            "[bold white][5][/bold white] Export Data Maskapai",
                            "[bold white][6][/bold white] Export Data Kota",
                            "",
                            "[bold white][0][/bold white] Kembali ke Menu Utama",
                            "",
                            "[dim]powered by Purwadhika - Digital Technology School[/dim]",
                        ]
                    ),
                    title="[bold green]Menu Export Data[/bold green]",
                    border_style="green",
                )
                console.print(menu_panel)

                choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()

                if choice == "1":
                    exports.export_trips(self.connection)
                elif choice == "2":
                    exports.export_flights(self.connection)
                elif choice == "3":
                    exports.export_hotels(self.connection)
                elif choice == "4":
                    exports.export_users(self.connection)
                elif choice == "5":
                    exports.export_airlines(self.connection)
                elif choice == "6":
                    exports.export_cities(self.connection)
                elif choice == "0":
                    break
                else:
                    console.print("[red]Pilihan tidak valid, silakan coba lagi.[/red]")
                    console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")