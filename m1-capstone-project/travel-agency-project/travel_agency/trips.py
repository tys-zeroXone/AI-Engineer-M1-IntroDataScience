from mysql.connector import Error
from datetime import datetime, date
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from . import maintenance
from .utils import _show_table

console = Console()


# ==========================
# HELPER: PILIH / DAFTARKAN USER
# ==========================

def _select_or_create_user(conn):
    """Tanya dulu apakah user sudah terdaftar, lalu pilih atau daftarkan."""
    while True:
        ans = console.input(
            "[cyan]Apakah pengguna sudah terdaftar sebelumnya? (y/n): [/cyan]"
        ).strip().lower()
        if ans == "y":
            uid = _search_and_select_user(conn)
            return uid
        elif ans == "n":
            # Gunakan fungsi yang sudah ada di maintenance.py
            maintenance._add_user(conn)
            
            # Setelah menambahkan pengguna, tanya apakah ingin memilih pengguna tersebut
            use_new = console.input(
                "\n[cyan]Apakah ingin menggunakan pengguna baru ini untuk pemesanan? (y/n): [/cyan]"
            ).strip().lower()
            
            if use_new == 'y':
                # Cari pengguna terbaru yang baru saja ditambahkan
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT MAX(user_id) FROM users")
                    new_user_id = cursor.fetchone()[0]
                    if new_user_id:
                        console.print(f"[green]Menggunakan pengguna baru dengan ID: {new_user_id}[/green]")
                        return new_user_id
                    else:
                        console.print("[yellow]Tidak dapat menemukan ID pengguna baru.[/yellow]")
                        return _search_and_select_user(conn)
                finally:
                    cursor.close()
            else:
                # Kembali ke pencarian pengguna
                return _search_and_select_user(conn)
        else:
            console.print("[yellow]Jawaban hanya 'y' atau 'n'.[/yellow]")


def _search_and_select_user(conn):
    """Cari user dari hasil pencarian di maintenance.py, lalu pilih satu."""
    # Gunakan fungsi pencarian yang sudah ada di maintenance.py
    rows = maintenance._search_users(conn)
    if not rows:
        console.print("[yellow]Tidak ada pengguna yang cocok dengan kriteria.[/yellow]")
        return None

    while True:
        uid_str = console.input(
            "\n[bold cyan]Pilih ID Pengguna yang akan dipakai (kosongkan untuk batal): [/bold cyan]"
        ).strip()
        if uid_str == "":
            console.print("[yellow]Pemilihan pengguna dibatalkan.[/yellow]")
            return None
        try:
            uid = int(uid_str)
        except ValueError:
            console.print("[red]ID harus berupa angka.[/red]")
            continue

        if any(r[0] == uid for r in rows):
            return uid
        else:
            console.print("[red]ID tersebut tidak ada di hasil pencarian, coba lagi.[/red]")


def _select_city(conn, title: str = "Pilih Kota"):
    """Pilih satu kota dari hasil pencarian di maintenance.py."""
    # Gunakan fungsi pencarian yang sudah ada di maintenance.py
    rows = maintenance._search_cities(conn)
    if not rows:
        console.print("[yellow]Tidak ada kota yang cocok dengan kriteria.[/yellow]")
        return None

    console.print(f"\n[bold]{title}[/bold]")
    # TIDAK PERLU _show_table() lagi karena sudah ditampilkan di maintenance._search_cities()
    
    while True:
        cid_str = console.input(
            "[bold cyan]Pilih ID Kota (kosongkan untuk batal): [/bold cyan]"
        ).strip()
        if cid_str == "":
            console.print("[yellow]Pemilihan kota dibatalkan.[/yellow]")
            return None
        try:
            cid = int(cid_str)
        except ValueError:
            console.print("[red]ID kota harus angka.[/red]")
            continue

        if any(r[0] == cid for r in rows):
            # Cari detail kota yang dipilih
            for r in rows:
                if r[0] == cid:
                    return cid, f"{r[2]}, {r[4]}"
        else:
            console.print("[red]ID kota tersebut tidak ada di hasil pencarian, coba lagi.[/red]")


def _select_hotel_in_city(conn, city_id: int):
    """Tampilkan daftar hotel di kota tertentu menggunakan fungsi pencarian."""
    cursor = conn.cursor()
    try:
        # Dapatkan informasi kota terlebih dahulu
        cursor.execute("SELECT name FROM cities WHERE city_id = %s", (city_id,))
        city_row = cursor.fetchone()
        city_name = city_row[0] if city_row else "Unknown City"
  
        # Gunakan fungsi pencarian hotel dengan filter kota
        # Karena _search_hotels tidak menerima parameter city_id, kita akan query langsung
        cursor.execute(
            """
            SELECT 
                h.hotel_id,
                h.hotel_name,
                h.price_per_day,
                REPEAT('★', h.star_rating)
            FROM hotels h
            WHERE h.city_id = %s
            ORDER BY h.star_rating DESC, h.hotel_name
            """,
            (city_id,),
        )
        rows = cursor.fetchall()
        
        if not rows:
            console.print("[yellow]Tidak ada hotel di kota tersebut.[/yellow]")
            return None

        _show_table(
            "Daftar Hotel di Kota Tujuan",
            ["ID Hotel", "Nama Hotel", "Harga per Malam (usd)", "Star Rating"],
            rows,
        )

        while True:
            hid_str = console.input(
                "[bold cyan]Pilih ID Hotel (kosongkan untuk batal): [/bold cyan]"
            ).strip()
            if hid_str == "":
                return None
            try:
                hid = int(hid_str)
            except ValueError:
                console.print("[red]ID hotel harus angka.[/red]")
                continue

            for r in rows:
                if r[0] == hid:
                    return hid, r[1], float(r[2])
            console.print("[red]ID hotel tidak terdapat di daftar, coba lagi.[/red]")

    except Error as e:
        console.print(f"[red]Error saat memilih hotel:[/red] {e}")
        return None
    finally:
        cursor.close()


def _select_flight_for_route(conn, from_city_id: int, to_city_id: int, direction: str):
    """
    Pilih penerbangan berdasarkan rute & arah (outbound/return).
    """
    cursor = conn.cursor()
    try:
        # Dapatkan informasi kota
        cursor.execute("SELECT name FROM cities WHERE city_id = %s", (from_city_id,))
        from_city = cursor.fetchone()
        from_city_name = from_city[0] if from_city else "Unknown"
        
        cursor.execute("SELECT name FROM cities WHERE city_id = %s", (to_city_id,))
        to_city = cursor.fetchone()
        to_city_name = to_city[0] if to_city else "Unknown"
        
        console.print(f"\n[cyan]Mencari penerbangan {direction}: {from_city_name} → {to_city_name}[/cyan]")
        
        # Query untuk mencari penerbangan
        cursor.execute(
            """
            SELECT
                f.flight_id,
                al.name       AS airline,
                c_from.name   AS from_city,
                c_to.name     AS to_city,
                f.flight_type,
                f.price,
                f.flight_time_hours,
                f.flight_date
            FROM flights f
            JOIN airlines al   ON f.airline_id   = al.airline_id
            JOIN cities   c_from ON f.from_city_id = c_from.city_id
            JOIN cities   c_to   ON f.to_city_id   = c_to.city_id
            WHERE f.from_city_id = %s
              AND f.to_city_id   = %s
              AND f.direction    = %s
            ORDER BY f.flight_date, al.name
            """,
            (from_city_id, to_city_id, direction),
        )
        rows = cursor.fetchall()
        
        if not rows:
            console.print("[yellow]Tidak ada penerbangan untuk rute & arah tersebut.[/yellow]")
            return None

        _show_table(
            f"Daftar Penerbangan ({direction})",
            ["ID Penerbangan", "Maskapai", "Dari", "Ke", "Tipe", "Harga (usd)", "Durasi (jam)", "Tanggal"],
            rows,
        )

        while True:
            fid_str = console.input(
                "[bold cyan]Pilih ID Penerbangan (kosongkan untuk batal): [/bold cyan]"
            ).strip()
            if fid_str == "":
                return None
            try:
                fid = int(fid_str)
            except ValueError:
                console.print("[red]ID flight harus angka.[/red]")
                continue

            for r in rows:
                if r[0] == fid:
                    fdate = r[7]
                    if isinstance(fdate, datetime):
                        fdate = fdate.date()
                    return fid, float(r[5]), fdate
            console.print("[red]ID flight tidak terdapat di daftar, coba lagi.[/red]")

    except Error as e:
        console.print(f"[red]Error saat memilih penerbangan:[/red] {e}")
        return None
    finally:
        cursor.close()


# =========================================================
#  BOOKING TRIPS
# =========================================================

def create_trip(conn):
    cursor = conn.cursor()
    try:
        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold cyan]PEMESANAN PERJALANAN BARU[/bold cyan]",
            subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
            border_style="cyan",
        )
        console.print(header, justify="center")

        # ==========================================
        # 1. PILIH JENIS PEMESANAN
        # ==========================================
        menu_panel = Panel(
            "\n".join(
                [
                    "[bold white][1][/bold white] Hanya Pesan Hotel",
                    "[bold white][2][/bold white] Hanya Pesan Penerbangan",
                    "[bold white][3][/bold white] Pesan Hotel + Penerbangan",
                    "",
                    "[dim]powered by Purwadhika - Digital Technology School[/dim]",
                ]
            ),
            title="[bold green]Pemilihan Jenis Pemesanan[/bold green]",
            border_style="green",
        )
        console.print(menu_panel)

        mode = console.input("[bold cyan]Pilih Jenis Pemesanan (Pilihan: 1/2/3): [/bold cyan]").strip()
        if mode not in {"1", "2", "3"}:
            console.print("[red]Pilihan tidak valid.[/red]")
            return

        hotel_only = (mode == "1")
        flight_only = (mode == "2")
        hotel_and_flight = (mode == "3")

        book_hotel = hotel_only or hotel_and_flight
        book_flight = flight_only or hotel_and_flight

        # ==========================================
        # 2. PILIH / DAFTARKAN USER
        # ==========================================

        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Pemilihan Pengguna[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        user_id = _select_or_create_user(conn)
        if not user_id:
            console.print("[magenta]Pemesanan dibatalkan karena pengguna belum dipilih.[/magenta]")
            return

        cursor.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        user_name = row[0] if row else f"User #{user_id}"
        console.print(f"\nPemesanan untuk pengguna: [bold yellow]{user_name}[/bold yellow]\n")

        # ==========================================
        # 3. TENTUKAN RUTE (JIKA PAKAI FLIGHT)
        # ==========================================

        from_city_id = None
        from_city_label = None
        dest_city_id = None
        dest_city_label = None

        if book_flight:

            console.print("\n")
            header = Panel.fit(
                "[bold magenta]Pemilihan kota asal dan tujuan penerbangan[/bold magenta]",
                border_style="magenta",
            )
            console.print(header, justify="center")

            from_sel = _select_city(conn, title="Pilih Kota Asal Penerbangan")
            if not from_sel:
                console.print("[yellow]Kota asal tidak dipilih, pemesanan dibatalkan.[/yellow]")
                return
            from_city_id, from_city_label = from_sel

            dest_sel = _select_city(conn, title="Pilih Kota Tujuan Penerbangan")
            if not dest_sel:
                console.print("[yellow]Kota tujuan tidak dipilih, pemesanan dibatalkan.[/yellow]")
                return
            dest_city_id, dest_city_label = dest_sel

        # Jika hotel-only, tentukan kota tujuan untuk hotel
        if hotel_only:

            console.print("\n")
            header = Panel.fit(
                "[bold magenta]Pemilihan kota tujuan hotel[/bold magenta]",
                border_style="magenta",
            )
            console.print(header, justify="center")

            dest_sel = _select_city(conn, title="Pilih Kota untuk Menginap (Hotel-only)")
            if not dest_sel:
                console.print("[yellow]Kota tujuan hotel tidak dipilih, pemesanan dibatalkan.[/yellow]")
                return
            dest_city_id, dest_city_label = dest_sel

        # ==========================================
        # 4. PILIH FLIGHT OUTBOUND & RETURN (JIKA PERLU)
        # ==========================================
        outbound_flight_id = None
        outbound_price = 0.0
        outbound_date = None

        return_flight_id = None
        return_price = 0.0
        return_date = None

        if book_flight:

            console.print("\n")
            header = Panel.fit(
                "[bold magenta]Pemilihan maskapai keberangkatan[/bold magenta]",
                border_style="magenta",
            )
            console.print(header, justify="center")

            # OUTBOUND
            outbound_sel = _select_flight_for_route(
                conn,
                from_city_id=from_city_id,
                to_city_id=dest_city_id,
                direction="outbound",
            )
            if outbound_sel:
                outbound_flight_id, outbound_price, outbound_date = outbound_sel
            else:
                console.print("[yellow]Tidak ada outbound flight yang dipilih.[/yellow]")

            # RETURN (opsional)

            console.print("\n")
            header = Panel.fit(
                "[bold magenta]Pemilihan maskapai kepulangan[/bold magenta]",
                border_style="magenta",
            )
            console.print(header, justify="center")

            want_return = console.input(
                "\n[cyan]Apakah ingin memesan return flight (pulang)? (y/n): [/cyan]"
            ).strip().lower()

            if want_return == "y":
                return_sel = _select_flight_for_route(
                    conn,
                    from_city_id=dest_city_id,
                    to_city_id=from_city_id,
                    direction="return",
                )
                if return_sel:
                    return_flight_id, return_price, return_date = return_sel
                else:
                    console.print("[yellow]Tidak ada return flight yang dipilih.[/yellow]")

        # ==========================================
        # 5. PILIH HOTEL (JIKA PESAN HOTEL)
        # ==========================================
        hotel_id = None
        hotel_name = None
        total_hotel_price = 0.0
        check_in_date = None
        check_out_date = None

        if book_hotel:

            console.print("\n")
            header = Panel.fit(
                "[bold magenta]Pemilihan hotel[/bold magenta]",
                border_style="magenta",
            )
            console.print(header, justify="center")

            # Jika ada flight, gunakan kota tujuan flight sebagai kota hotel
            hotel_city_id = dest_city_id
            console.print(
                f"\nPilih hotel di kota tujuan: [bold yellow]{dest_city_label}[/bold yellow]"
            )

            hotel_sel = _select_hotel_in_city(conn, hotel_city_id)
            if not hotel_sel:
                console.print("[yellow]Tidak ada hotel yang dipilih, pemesanan hotel dibatalkan.[/yellow]")
            else:
                hotel_id, hotel_name, price_per_day = hotel_sel

                # Minta tanggal check-in/out
                console.print(
                    "\n[bold cyan]Masukkan tanggal menginap hotel[/bold cyan]"
                )
                check_in_raw = console.input("  Check-in   (Format: YYYY-MM-DD): ").strip()
                check_out_raw = console.input("  Check-out  (Format: YYYY-MM-DD): ").strip()

                try:
                    check_in_date = datetime.strptime(check_in_raw, "%Y-%m-%d").date()
                    check_out_date = datetime.strptime(check_out_raw, "%Y-%m-%d").date()
                    if check_out_date <= check_in_date:
                        console.print("[red]Check-out harus setelah check-in.[/red]")
                        return
                except ValueError:
                    console.print("[red]Format tanggal check-in/out tidak valid.[/red]")
                    return

                stay_days = (check_out_date - check_in_date).days
                total_hotel_price = price_per_day * stay_days

        # ==========================================
        # 6. HITUNG TANGGAL TRIP, DAYS, TOTAL HARGA
        # ==========================================
        candidates_start = []
        candidates_end = []

        if check_in_date:
            candidates_start.append(check_in_date)
        if outbound_date:
            candidates_start.append(outbound_date)

        if check_out_date:
            candidates_end.append(check_out_date)
        if return_date:
            candidates_end.append(return_date)
        elif outbound_date:
            candidates_end.append(outbound_date)

        if not candidates_start or not candidates_end:
            console.print("[red]Tanggal trip tidak dapat ditentukan (tidak ada hotel maupun flight dengan tanggal).[/red]")
            return

        trip_start_date = min(candidates_start)
        trip_end_date = max(candidates_end)
        days = (trip_end_date - trip_start_date).days
        if days < 0:
            console.print("[red]Perhitungan hari trip tidak valid.[/red]")
            return

        total_flight_price = float(outbound_price) + float(return_price)
        total_trip_cost = total_hotel_price + total_flight_price

        # ==========================================
        # 7. REVIEW ORDER
        # ==========================================
        header = Panel.fit(
            "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
            subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
            border_style="cyan",
        )
        console.print(header, justify="center")

        review_table = Table(show_header=True, header_style="bold magenta")
        review_table.add_column("Item", style="bold", width=28)
        review_table.add_column("Detail", style="white")

        review_table.add_row("Nama Pengguna", user_name)
        if from_city_label and dest_city_label:
            review_table.add_row("Rute Perjalanan", f"{from_city_label} → {dest_city_label}")
        else:
            review_table.add_row("Rute Perjalanan", "[dim]Tidak ada penerbangan[/dim]")

        review_table.add_row(
            "Periode Perjalanan",
            f"{trip_start_date} s/d {trip_end_date}",
        )

        if hotel_id:
            review_table.add_row("ID Hotel", str(hotel_id))
            review_table.add_row("Nama Hotel", hotel_name)
            review_table.add_row(
                "Check-in / Check-out",
                f"{check_in_date} s/d {check_out_date}",
            )
            review_table.add_row(
                "Total Biaya Hotel",
                f"{total_hotel_price:,.2f}",
            )
        else:
            review_table.add_row("Hotel", "[dim]Tidak dipesan[/dim]")

        if outbound_flight_id:
            review_table.add_row("Penerbangan Outbound", str(outbound_flight_id))
            review_table.add_row("Tanggal Outbound", str(outbound_date))
            review_table.add_row("Harga Outbound (usd)", f"{outbound_price:,.2f}")
        else:
            review_table.add_row("Penerbangan Outbound", "[dim]Tidak dipesan[/dim]")

        if return_flight_id:
            review_table.add_row("Penerbangan Return", str(return_flight_id))
            review_table.add_row("Tanggal Return", str(return_date))
            review_table.add_row("Harga Return (usd)", f"{return_price:,.2f}")
        else:
            review_table.add_row("Penerbangan Return", "[dim]Tidak dipesan[/dim]")

        review_table.add_row(
            "Total Biaya Flight",
            f"{total_flight_price:,.2f}",
        )
        review_table.add_row(
            "TOTAL BIAYA TRIP",
            f"[bold green]{total_trip_cost:,.2f}[/bold green]",
        )

        review_panel = Panel(
            review_table,
            title="[bold green]Review Pemesanan Perjalanan[/bold green]",
            border_style="green",
        )
        console.print(review_panel)

        confirm = console.input(
            "\n[bold cyan]Apakah informasi pemesanan perjalanan dikonfirmasi pengguna? (y/n): [/bold cyan]"
        ).strip().lower()
        if confirm != "y":
            console.print("[yellow]Pemesanan dibatalkan oleh pengguna sebelum disimpan.[/yellow]")
            try:
                conn.rollback()
            except Exception:
                pass
            return

        # ==========================================
        # 8. INSERT KE TABEL trips
        # ==========================================
        cursor.execute(
            """
            INSERT INTO trips (
                trip_start_date,
                trip_end_date,
                user_id,
                hotel_id,
                days,
                total_hotel_price,
                check_in_date,
                check_out_date,
                outbound_flight_id,
                return_flight_id,
                total_flight_price,
                status,
                total_trip_cost
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                trip_start_date,
                trip_end_date,
                user_id,
                hotel_id,
                days,
                total_hotel_price,
                check_in_date,
                check_out_date,
                outbound_flight_id,
                return_flight_id,
                total_flight_price,
                "confirmed",
                total_trip_cost,
            ),
        )
        conn.commit()
        console.print("\n[bold green]✅ Pemesanan Perjalanan Berhasil, Silahkan Lanjut Proses Pembayaran![/bold green]")

    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        console.print(f"[red]Terjadi error saat membuat trip:[/red] {e}")
    finally:
        cursor.close()

    
def reschedule_trip(conn):
    """
    Reschedule trip yang sudah ada:
    - Cari dan pilih trip menggunakan fungsi di maintenance.py
    - Identifikasi jenis booking (flight only, hotel only, atau both)
    - Ubah sesuai pilihan user
    """
    cursor = conn.cursor()
    try:
        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Reschedule Perjalanan[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        # Cari trip yang akan direschedule menggunakan fungsi yang sudah ada
        rows = maintenance._search_trips(conn)
        if not rows:
            console.print("[yellow]Tidak ada trip yang ditemukan.[/yellow]")
            return

        try:
            trip_id = int(console.input("[bold cyan]\nPilih ID Perjalanan yang akan diubah: [/bold cyan]").strip())
        except ValueError:
            console.print("[red]ID Perjalanan tidak valid.[/red]")
            return

        # Ambil detail trip lengkap
        cursor.execute(
            """
            SELECT 
                t.trip_id,
                t.user_id,
                u.name AS user_name,
                t.hotel_id,
                h.hotel_name,
                t.check_in_date,
                t.check_out_date,
                t.total_hotel_price,
                t.outbound_flight_id,
                t.return_flight_id,
                t.total_flight_price,
                t.trip_start_date,
                t.trip_end_date,
                t.days,
                t.total_trip_cost,
                t.status
            FROM trips t
            JOIN users u ON t.user_id = u.user_id
            LEFT JOIN hotels h ON t.hotel_id = h.hotel_id
            WHERE t.trip_id = %s
            """,
            (trip_id,),
        )
        trip_data = cursor.fetchone()
        
        if not trip_data:
            console.print("[red]Perjalanan tidak ditemukan.[/red]")
            return

        # Unpack trip data
        (trip_id, user_id, user_name, hotel_id, hotel_name, 
         check_in_date, check_out_date, total_hotel_price,
         outbound_flight_id, return_flight_id, total_flight_price,
         trip_start_date, trip_end_date, days, total_trip_cost, status) = trip_data

        # Tampilkan detail trip saat ini
        _display_current_trip_details(trip_data)

        # Identifikasi jenis booking
        has_hotel = hotel_id is not None
        has_flight = outbound_flight_id is not None

        if not has_hotel and not has_flight:
            console.print("[red]Trip ini tidak memiliki hotel maupun penerbangan.[/red]")
            return

        # Tentukan apa yang akan diubah
        if has_hotel and has_flight:
            what_to_change = _ask_what_to_reschedule()
            if what_to_change is None:
                console.print("[yellow]Reschedule dibatalkan.[/yellow]")
                return
        elif has_hotel:
            what_to_change = "hotel"
            console.print("\n[cyan]Trip ini hanya memiliki hotel. Akan melakukan reschedule hotel.[/cyan]")
        else:  # has_flight
            what_to_change = "flight"
            console.print("\n[cyan]Trip ini hanya memiliki penerbangan. Akan melakukan reschedule penerbangan.[/cyan]")

        # Proses reschedule sesuai pilihan
        new_trip_data = {}
        cancelled = False  # Flag untuk menandai apakah user membatalkan
        
        if what_to_change in ["hotel", "both"]:
            hotel_result = _reschedule_hotel(conn, cursor, hotel_id, user_name)
            if hotel_result:
                new_trip_data.update(hotel_result)
            else:
                # Jika hanya hotel dan tidak ada perubahan, tanya apakah ingin melanjutkan
                if what_to_change == "hotel":
                    proceed = console.input(
                        "\n[bold cyan]Lanjutkan tanpa perubahan? (y/n): [/bold cyan]"
                    ).strip().lower()
                    if proceed != 'y':
                        console.print("[yellow]Reschedule hotel dibatalkan.[/yellow]")
                        cancelled = True

        # Hanya proses flight jika reschedule hotel tidak dibatalkan atau jika kita dalam mode "both"
        if not cancelled and what_to_change in ["flight", "both"]:
            flight_result = _reschedule_flight(conn, cursor, outbound_flight_id, return_flight_id)
            if flight_result:
                new_trip_data.update(flight_result)
            else:
                console.print("[yellow]Tidak ada perubahan pada penerbangan.[/yellow]")
                # Jika hanya flight dan tidak ada perubahan, tanya apakah ingin melanjutkan
                if what_to_change == "flight":
                    proceed = console.input(
                        "\n[cyan]Tidak ada perubahan pada penerbangan. Lanjutkan tanpa perubahan? (y/n): [/cyan]"
                    ).strip().lower()
                    if proceed != 'y':
                        console.print("[yellow]Reschedule penerbangan dibatalkan.[/yellow]")
                        cancelled = True

        # Cek apakah user membatalkan atau benar-benar tidak ada perubahan
        if cancelled:
            console.print("[yellow]Reschedule dibatalkan oleh pengguna.[/yellow]")
            return
            
        if not new_trip_data:
            console.print("\n[bold magenta]⚠️ Tidak ada perubahan yang dilakukan pada trip. Reschedule dibatalkan[/bold magenta]")
            return

        # Hitung ulang total biaya dan tanggal trip
        new_total_hotel = new_trip_data.get('total_hotel_price', total_hotel_price or 0)
        new_total_flight = new_trip_data.get('total_flight_price', total_flight_price or 0)
        new_total_trip = new_total_hotel + new_total_flight

        # Tentukan tanggal mulai dan selesai trip
        dates_list = []
        if 'check_in_date' in new_trip_data:
            dates_list.append(new_trip_data['check_in_date'])
        elif check_in_date:
            dates_list.append(check_in_date)
            
        if 'outbound_date' in new_trip_data:
            dates_list.append(new_trip_data['outbound_date'])
        elif outbound_flight_id:
            cursor.execute("SELECT flight_date FROM flights WHERE flight_id = %s", (outbound_flight_id,))
            old_out = cursor.fetchone()
            if old_out:
                dates_list.append(old_out[0])

        dates_end = []
        if 'check_out_date' in new_trip_data:
            dates_end.append(new_trip_data['check_out_date'])
        elif check_out_date:
            dates_end.append(check_out_date)
            
        if 'return_date' in new_trip_data:
            dates_end.append(new_trip_data['return_date'])
        elif return_flight_id:
            cursor.execute("SELECT flight_date FROM flights WHERE flight_id = %s", (return_flight_id,))
            old_ret = cursor.fetchone()
            if old_ret:
                dates_end.append(old_ret[0])

        if dates_list and dates_end:
            new_trip_start = min(dates_list)
            new_trip_end = max(dates_end)
            new_days = (new_trip_end - new_trip_start).days
        else:
            new_trip_start = trip_start_date
            new_trip_end = trip_end_date
            new_days = days

        # Tampilkan konfirmasi perubahan
        _display_reschedule_confirmation(
            trip_data, new_trip_data, new_total_hotel, 
            new_total_flight, new_total_trip, new_trip_start, 
            new_trip_end, new_days
        )

        confirm = console.input(
            "\n[bold cyan]Apakah perubahan perjalanan sudah sesuai? (y/n): [/bold cyan]"
        ).strip().lower()
        
        if confirm != "y":
            console.print("[yellow]Reschedule dibatalkan.[/yellow]")
            return

        # Update database
        update_fields = []
        update_params = []

        if 'hotel_id' in new_trip_data:
            update_fields.append("hotel_id = %s")
            update_params.append(new_trip_data['hotel_id'])
        if 'check_in_date' in new_trip_data:
            update_fields.append("check_in_date = %s")
            update_params.append(new_trip_data['check_in_date'])
        if 'check_out_date' in new_trip_data:
            update_fields.append("check_out_date = %s")
            update_params.append(new_trip_data['check_out_date'])
        if 'total_hotel_price' in new_trip_data:
            update_fields.append("total_hotel_price = %s")
            update_params.append(new_trip_data['total_hotel_price'])

        if 'outbound_flight_id' in new_trip_data:
            update_fields.append("outbound_flight_id = %s")
            update_params.append(new_trip_data['outbound_flight_id'])
        if 'return_flight_id' in new_trip_data:
            update_fields.append("return_flight_id = %s")
            update_params.append(new_trip_data['return_flight_id'])
        if 'total_flight_price' in new_trip_data:
            update_fields.append("total_flight_price = %s")
            update_params.append(new_trip_data['total_flight_price'])

        update_fields.extend([
            "trip_start_date = %s",
            "trip_end_date = %s",
            "days = %s",
            "total_trip_cost = %s"
        ])
        update_params.extend([new_trip_start, new_trip_end, new_days, new_total_trip])
        update_params.append(trip_id)

        query = f"UPDATE trips SET {', '.join(update_fields)} WHERE trip_id = %s"
        cursor.execute(query, tuple(update_params))
        conn.commit()

        console.print("[bold green]✅ Reschedule berhasil disimpan![/bold green]")

    except Exception as e:
        conn.rollback()
        console.print(f"[red]Error saat reschedule trip:[/red] {e}")
    finally:
        cursor.close()


def _ask_what_to_reschedule():
    """Tanya user mau reschedule apa"""
    console.print("\n[bold cyan]Perjalanan ini memiliki hotel dan penerbangan.[/bold cyan]")
    console.print("[cyan]Apa yang ingin Anda reschedule?[/cyan]")
    console.print("  [1] Hotel saja")
    console.print("  [2] Penerbangan saja")
    console.print("  [3] Hotel dan Penerbangan")
    console.print("  [0] Batal")

    choice = console.input("\n[cyan]Pilihan (1/2/3/0): [/cyan]").strip()
    
    if choice == "1":
        return "hotel"
    elif choice == "2":
        return "flight"
    elif choice == "3":
        return "both"
    else:
        return None


def _reschedule_hotel(conn, cursor, current_hotel_id, user_name):
    """Reschedule hotel - cari hotel baru dan/atau tanggal baru"""
    console.print("\n")
    header = Panel.fit(
        "[bold cyan]SISTEM MANAJEMEN TRAVEL [/bold cyan]",
        subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
        border_style="cyan",
    )
    console.print(header, justify="center")
    # TAMPILKAN MENU RESCHEDULE
    menu_panel = Panel(
        "\n".join(
            [
                "[bold white][1][/bold white] Hotel saja",
                "[bold white][2][/bold white] Tanggal check-in saja",
                "[bold white][3][/bold white] Tanggal check-out saja",
                "[bold white][4][/bold white] Kedua tanggal (check-in & check-out)",
                "[bold white][5][/bold white] Hotel dan kedua tanggal",
                "",
                "[bold white][0][/bold white] Batal reschedule hotel",
                "",
                "[dim]powered by Purwadhika - Digital Technology School[/dim]",
            ]
        ),
        title="[bold green]Menu Reschedule Hotel[/bold green]",
        border_style="green",
    )
    console.print(menu_panel)
    
 
    # Dapatkan info hotel lama
    cursor.execute(
        """
        SELECT h.hotel_name, c.name as city_name, h.city_id, h.price_per_day
        FROM hotels h
        JOIN cities c ON h.city_id = c.city_id
        WHERE h.hotel_id = %s
        """,
        (current_hotel_id,)
    )
    old_hotel = cursor.fetchone()
    if old_hotel:
        console.print(f"Hotel saat ini: [bold yellow]{old_hotel[0]} di {old_hotel[1]}[/bold yellow]")
        city_id = old_hotel[2]
        old_price_per_day = float(old_hotel[3])
    else:
        console.print("[yellow]Info hotel lama tidak ditemukan.[/yellow]")
        return None

    # Dapatkan tanggal lama terlebih dahulu
    cursor.execute(
        "SELECT check_in_date, check_out_date FROM trips WHERE hotel_id = %s ORDER BY trip_id DESC LIMIT 1",
        (current_hotel_id,)
    )
    old_dates = cursor.fetchone()
    old_check_in = old_dates[0] if old_dates else None
    old_check_out = old_dates[1] if old_dates else None
    
    if old_check_in and old_check_out:
        console.print(f"Tanggal lama: [bold yellow]{old_check_in} s/d {old_check_out}[/bold yellow]")

    choice = console.input("\n[bold cyan]Pilih perubahan yang diinginkan:[/bold cyan] ").strip()
    
    if choice == "0":
        console.print("[yellow]Reschedule hotel dibatalkan.[/yellow]")
        return None
    
    # Inisialisasi variabel
    hotel_id = current_hotel_id
    hotel_name = old_hotel[0]
    price_per_day = old_price_per_day
    new_check_in = old_check_in
    new_check_out = old_check_out
    
    # PROSES PERUBAHAN HOTEL
    if choice in ["1", "5"]:
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Pemilihan Hotel Baru[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")
        
        hotel_sel = _select_hotel_in_city(conn, city_id)
        if hotel_sel:
            hotel_id, hotel_name, price_per_day = hotel_sel
            if hotel_id == current_hotel_id:
                console.print("[bold magenta]\nHotel yang dipilih sama dengan hotel saat ini.[/bold magenta]")
        else:
            console.print("[yellow]Pemilihan hotel dibatalkan.[/yellow]")
            if choice == "1":  # Jika hanya ingin ganti hotel, batalkan seluruhnya
                return None
    
    # PROSES PERUBAHAN CHECK-IN
    if choice in ["2", "4", "5"]:
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Perubahan Tanggal Check-in[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")
        
        console.print("\n[dim]Kosongkan untuk menggunakan tanggal lama[/dim]")
        check_in_str = console.input(f"[cyan]Check-in baru (YYYY-MM-DD, saat ini {old_check_in}): [/cyan]").strip()
        
        if check_in_str == "":
            new_check_in = old_check_in
            console.print(f"[dim]Menggunakan tanggal check-in lama: {new_check_in}[/dim]")
        elif check_in_str:
            try:
                new_check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
                # Validasi: check-in baru tidak boleh setelah check-out lama
                if old_check_out and new_check_in > old_check_out:
                    console.print("[red]Check-in baru tidak boleh setelah check-out lama.[/red]")
                    return None
            except ValueError:
                console.print("[red]Format tanggal tidak valid.[/red]")
                return None
        else:
            console.print("[red]Tanggal check-in tidak valid.[/red]")
            return None
    
    # PROSES PERUBAHAN CHECK-OUT
    if choice in ["3", "4", "5"]:
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Perubahan Tanggal Check-out[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")
        
        console.print("\n[dim]Kosongkan untuk menggunakan tanggal lama[/dim]")
        check_out_str = console.input(f"[cyan]Check-out baru (YYYY-MM-DD, saat ini {old_check_out}): [/cyan]").strip()
        
        if check_out_str == "":
            new_check_out = old_check_out
            console.print(f"[dim]Menggunakan tanggal check-out lama: {new_check_out}[/dim]")
        elif check_out_str:
            try:
                new_check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()
                # Validasi: check-out baru tidak boleh sebelum check-in (baru atau lama)
                if new_check_out <= (new_check_in if 'new_check_in' in locals() else old_check_in):
                    console.print("[red]Check-out harus setelah check-in.[/red]")
                    return None
            except ValueError:
                console.print("[red]Format tanggal tidak valid.[/red]")
                return None
        else:
            console.print("[red]Tanggal check-out tidak valid.[/red]")
            return None
    
    # Jika hanya mengubah check-in saja, perlu validasi dengan check-out lama
    if choice == "2" and new_check_in and old_check_out:
        if new_check_in > old_check_out:
            console.print("[red]Check-in baru tidak boleh setelah check-out lama.[/red]")
            return None
    
    # Jika hanya mengubah check-out saja, perlu validasi dengan check-in lama
    if choice == "3" and old_check_in and new_check_out:
        if new_check_out <= old_check_in:
            console.print("[red]Check-out baru harus setelah check-in lama.[/red]")
            return None
    
    # Cek apakah ada perubahan
    hotel_changed = (hotel_id != current_hotel_id)
    check_in_changed = (new_check_in != old_check_in) if old_check_in else False
    check_out_changed = (new_check_out != old_check_out) if old_check_out else False
    
    if not hotel_changed and not check_in_changed and not check_out_changed:
        console.print("\n[bold magenta]Tidak ada perubahan yang dilakukan pada pemesanan hotel.[/bold magenta]")
        return None
    
    # Hitung harga baru SEBELUM menampilkan ringkasan
    stay_days = (new_check_out - new_check_in).days
    new_hotel_price = price_per_day * stay_days
    console.print("\n")
    
    return {
        'hotel_id': hotel_id,
        'hotel_name': hotel_name,
        'check_in_date': new_check_in,
        'check_out_date': new_check_out,
        'total_hotel_price': new_hotel_price
    }


def _reschedule_flight(conn, cursor, current_outbound_id, current_return_id):
    """Reschedule penerbangan - cari penerbangan baru untuk outbound, return, atau keduanya"""
    console.print("\n")
    header = Panel.fit(
        "[bold cyan]RESCHEDULE PEMESANAN PENERBANGAN[/bold cyan]",
        subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
        border_style="cyan",
    )
    console.print(header, justify="center")
    console.print("\n")
    
    result = {}
    
    # TAMPILKAN MENU RESCHEDULE PENERBANGAN
    console.print("\n")
    menu_title = "[bold green]Menu Reschedule Penerbangan[/bold green]"
    menu_items = []
    
    # Tentukan opsi berdasarkan apakah ada outbound dan/atau return
    if current_outbound_id:
        menu_items.append("[bold white][1][/bold white] Outbound flight saja")
    if current_return_id:
        menu_items.append("[bold white][2][/bold white] Return flight saja")
    if current_outbound_id and current_return_id:
        menu_items.append("[bold white][3][/bold white] Kedua penerbangan (outbound & return)")
    
    if not menu_items:
        console.print("[yellow]Tidak ada penerbangan yang dapat direschedule.[/yellow]")
        return None
    
    menu_items.extend([
        "",
        "[bold white][0][/bold white] Batal reschedule penerbangan",
        "",
        "[dim]powered by Purwadhika - Digital Technology School[/dim]"
    ])
    
    menu_panel = Panel(
        "\n".join(menu_items),
        title=menu_title,
        border_style="green",
    )
    console.print(menu_panel)
    
    choice = console.input("\n[bold cyan]Pilih menu:[/bold cyan] ").strip()
    
    if choice == "0":
        console.print("[yellow]Reschedule penerbangan dibatalkan.[/yellow]")
        return None
    
    # PROSES RESCHEDULE OUTBOUND
    if choice in ["1", "3"] and current_outbound_id:
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Reschedule Outbound Flight[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")
        
        # Dapatkan info outbound lama
        cursor.execute(
            """
            SELECT 
                f.from_city_id, 
                f.to_city_id,
                c1.name as from_city,
                c2.name as to_city,
                f.flight_date,
                f.price,
                f.direction
            FROM flights f
            JOIN cities c1 ON f.from_city_id = c1.city_id
            JOIN cities c2 ON f.to_city_id = c2.city_id
            WHERE f.flight_id = %s
            """,
            (current_outbound_id,)
        )
        old_outbound = cursor.fetchone()
        
        if old_outbound:
            from_city_id, to_city_id, from_city, to_city, old_outbound_date, old_outbound_price, direction = old_outbound
            
            console.print(f"\n[cyan]Outbound flight saat ini:[/cyan]")
            console.print(f"  Rute: [bold yellow]{from_city} → {to_city}[/bold yellow]")
            console.print(f"  Tanggal: {old_outbound_date}")
            console.print(f"  Harga: ${old_outbound_price:,.2f}")
            console.print(f"  Arah: {direction}")
            
            # Tampilkan menu pilihan untuk outbound
            console.print("\n")
            outbound_menu_panel = Panel(
                "\n".join([
                    "[bold white][1][/bold white] Cari penerbangan lain untuk rute yang sama",
                    "[bold white][2][/bold white] Tetap menggunakan penerbangan ini (tidak berubah)",
                    "",
                    "[bold white][0][/bold white] Batal ubah outbound",
                    "",
                    "[dim]powered by Purwadhika - Digital Technology School[/dim]"
                ]),
                title="[bold green]Pilihan Outbound Flight[/bold green]",
                border_style="green",
            )
            console.print(outbound_menu_panel)
            
            outbound_choice = console.input("\n[bold cyan]Pilih menu:[/bold cyan] ").strip()
            
            if outbound_choice == "1":
                flight_sel = _select_flight_for_route(conn, from_city_id, to_city_id, direction)
                if flight_sel:
                    flight_id, price, flight_date = flight_sel
                    # Cek apakah ada perubahan
                    if flight_id != current_outbound_id or flight_date != old_outbound_date:
                        result['outbound_flight_id'] = flight_id
                        result['outbound_price'] = price
                        result['outbound_date'] = flight_date
                        console.print("\n[green]✓ Outbound flight berhasil diubah.[/green]")
                    else:
                        console.print("\n[yellow]Flight yang dipilih sama dengan flight saat ini.[/yellow]")
                        result['outbound_price'] = float(old_outbound_price)
                        result['outbound_date'] = old_outbound_date
                else:
                    console.print("\n[yellow]Tidak ada flight yang dipilih. Menggunakan flight lama.[/yellow]")
                    result['outbound_price'] = float(old_outbound_price)
                    result['outbound_date'] = old_outbound_date
            elif outbound_choice == "2":
                console.print("\n[yellow]Outbound flight tidak diubah.[/yellow]")
                result['outbound_price'] = float(old_outbound_price)
                result['outbound_date'] = old_outbound_date
            else:
                console.print("\n[yellow]Perubahan outbound dibatalkan.[/yellow]")
                result['outbound_price'] = float(old_outbound_price)
                result['outbound_date'] = old_outbound_date
        else:
            console.print("\n[red]Info outbound flight lama tidak ditemukan.[/red]")
            return None
    
    # PROSES RESCHEDULE RETURN
    if choice in ["2", "3"] and current_return_id:
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Reschedule Return Flight[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")
        
        # Dapatkan info return lama
        cursor.execute(
            """
            SELECT 
                f.from_city_id, 
                f.to_city_id,
                c1.name as from_city,
                c2.name as to_city,
                f.flight_date,
                f.price,
                f.direction
            FROM flights f
            JOIN cities c1 ON f.from_city_id = c1.city_id
            JOIN cities c2 ON f.to_city_id = c2.city_id
            WHERE f.flight_id = %s
            """,
            (current_return_id,)
        )
        old_return = cursor.fetchone()
        
        if old_return:
            from_city_id, to_city_id, from_city, to_city, old_return_date, old_return_price, direction = old_return
            
            console.print(f"\n[cyan]Return flight saat ini:[/cyan]")
            console.print(f"  Rute: [bold yellow]{from_city} → {to_city}[/bold yellow]")
            console.print(f"  Tanggal: {old_return_date}")
            console.print(f"  Harga: ${old_return_price:,.2f}")
            console.print(f"  Arah: {direction}")
            
            # Tampilkan menu pilihan untuk return
            console.print("\n")
            return_menu_panel = Panel(
                "\n".join([
                    "[bold white][1][/bold white] Cari penerbangan lain untuk rute yang sama",
                    "[bold white][2][/bold white] Tetap menggunakan penerbangan ini (tidak berubah)",
                    "[bold white][3][/bold white] Hapus return flight (tidak jadi pulang)",
                    "",
                    "[bold white][0][/bold white] Batal ubah return",
                    "",
                    "[dim]powered by Purwadhika - Digital Technology School[/dim]"
                ]),
                title="[bold green]Pilihan Return Flight[/bold green]",
                border_style="green",
            )
            console.print(return_menu_panel)
            
            return_choice = console.input("\n[bold cyan]Pilih menu:[/bold cyan] ").strip()
            
            if return_choice == "1":
                flight_sel = _select_flight_for_route(conn, from_city_id, to_city_id, direction)
                if flight_sel:
                    flight_id, price, flight_date = flight_sel
                    # Cek apakah ada perubahan
                    if flight_id != current_return_id or flight_date != old_return_date:
                        result['return_flight_id'] = flight_id
                        result['return_price'] = price
                        result['return_date'] = flight_date
                        console.print("\n[green]✓ Return flight berhasil diubah.[/green]")
                    else:
                        console.print("\n[yellow]Flight yang dipilih sama dengan flight saat ini.[/yellow]")
                        result['return_price'] = float(old_return_price)
                        result['return_date'] = old_return_date
                else:
                    console.print("\n[yellow]Tidak ada flight yang dipilih. Menggunakan flight lama.[/yellow]")
                    result['return_price'] = float(old_return_price)
                    result['return_date'] = old_return_date
            elif return_choice == "2":
                console.print("\n[yellow]Return flight tidak diubah.[/yellow]")
                result['return_price'] = float(old_return_price)
                result['return_date'] = old_return_date
            elif return_choice == "3":
                console.print("\n[magenta]Return flight dihapus.[/magenta]")
                result['return_flight_id'] = None
                result['return_price'] = 0.0
                result['return_date'] = None
            else:
                console.print("\n[yellow]Perubahan return dibatalkan.[/yellow]")
                result['return_price'] = float(old_return_price)
                result['return_date'] = old_return_date
        else:
            console.print("\n[red]Info return flight lama tidak ditemukan.[/red]")
            return None
    
    # Cek apakah benar-benar ada perubahan pada ID flight
    outbound_changed = 'outbound_flight_id' in result and result['outbound_flight_id'] != current_outbound_id
    return_changed = 'return_flight_id' in result and result['return_flight_id'] != current_return_id
    
    # Simpan ID lama jika tidak diubah
    if not outbound_changed and current_outbound_id:
        result['outbound_flight_id'] = current_outbound_id
    
    if not return_changed and current_return_id and 'return_flight_id' not in result:
        result['return_flight_id'] = current_return_id
    
    # Hitung total flight price
    outbound_price = result.get('outbound_price', 0)
    return_price = result.get('return_price', 0)
    result['total_flight_price'] = outbound_price + return_price
    
    # Tampilkan ringkasan perubahan
    console.print("\n")
    summary_items = ["[bold green]Ringkasan Perubahan Penerbangan:[/bold green]"]
    
    if 'outbound_flight_id' in result:
        if result['outbound_flight_id'] != current_outbound_id:
            summary_items.append(f"  [cyan]Outbound:[/cyan] Diubah (ID baru: {result.get('outbound_flight_id', 'N/A')})")
        else:
            summary_items.append("  [cyan]Outbound:[/cyan] Tidak berubah")
    
    if 'return_flight_id' in result:
        if result['return_flight_id'] != current_return_id:
            if result['return_flight_id'] is None:
                summary_items.append("  [cyan]Return:[/cyan] Dihapus (tidak ada penerbangan pulang)")
            else:
                summary_items.append(f"  [cyan]Return:[/cyan] Diubah (ID baru: {result.get('return_flight_id', 'N/A')})")
        else:
            summary_items.append("  [cyan]Return:[/cyan] Tidak berubah")
    
    summary_items.append(f"  [cyan]Total biaya penerbangan:[/cyan] ${result['total_flight_price']:,.2f}")
    
    summary_panel = Panel(
        "\n".join(summary_items),
        title="[bold yellow]Konfirmasi Perubahan[/bold yellow]",
        border_style="yellow"
    )
    console.print(summary_panel)
    
    return result if result else None


def _display_current_trip_details(trip_data):
    """Tampilkan detail trip saat ini"""
    (trip_id, user_id, user_name, hotel_id, hotel_name, 
     check_in_date, check_out_date, total_hotel_price,
     outbound_flight_id, return_flight_id, total_flight_price,
     trip_start_date, trip_end_date, days, total_trip_cost, status) = trip_data

    console.print("\n")
    header = Panel.fit(
        "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
        subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
        border_style="cyan",
    )
    console.print(header, justify="center")

    table = Table(show_header=True, header_style="bold green")
    table.add_column("Item", style="bold", width=25)
    table.add_column("Detail", style="white")

    table.add_row("ID Trip", str(trip_id))
    table.add_row("Nama Pengguna", user_name)
    table.add_row("Status", status)
    table.add_row("Periode Trip", f"{trip_start_date} s/d {trip_end_date} ({days} hari)")
    
    if hotel_id:
        table.add_row("Hotel", f"{hotel_name} (ID: {hotel_id})")
        table.add_row("Check-in / Check-out", f"{check_in_date} s/d {check_out_date}")
        table.add_row("Total Biaya Hotel", f"${total_hotel_price:,.2f}")
    else:
        table.add_row("Hotel", "[dim]Tidak ada[/dim]")

    if outbound_flight_id:
        table.add_row("Flight Outbound", f"ID: {outbound_flight_id}")
    else:
        table.add_row("Flight Outbound", "[dim]Tidak ada[/dim]")

    if return_flight_id:
        table.add_row("Flight Return", f"ID: {return_flight_id}")
    else:
        table.add_row("Flight Return", "[dim]Tidak ada[/dim]")

    if outbound_flight_id or return_flight_id:
        table.add_row("Total Biaya Flight", f"${total_flight_price:,.2f}")

    table.add_row("TOTAL BIAYA", f"[bold green]${total_trip_cost:,.2f}[/bold green]")

    panel = Panel(table, title="[bold green]Detail Trip Saat Ini[/bold green]", border_style="green")
    console.print(panel)


def _display_reschedule_confirmation(trip_data, new_data, new_hotel_total, 
                                     new_flight_total, new_trip_total,
                                     new_start, new_end, new_days):
    """Tampilkan konfirmasi perubahan"""
    (trip_id, user_id, user_name, hotel_id, hotel_name, 
     check_in_date, check_out_date, total_hotel_price,
     outbound_flight_id, return_flight_id, total_flight_price,
     trip_start_date, trip_end_date, days, total_trip_cost, status) = trip_data

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Item", style="bold", width=25)
    table.add_column("Sebelum", style="yellow")
    table.add_column("Sesudah", style="cyan")

    # Hotel changes
    if 'hotel_id' in new_data:
        table.add_row(
            "Hotel",
            f"{hotel_name} (ID: {hotel_id})",
            f"{new_data.get('hotel_name', 'N/A')} (ID: {new_data['hotel_id']})"
        )
    
    if 'check_in_date' in new_data:
        table.add_row(
            "Check-in / Check-out",
            f"{check_in_date} / {check_out_date}",
            f"{new_data['check_in_date']} / {new_data['check_out_date']}"
        )
    
    if 'total_hotel_price' in new_data:
        table.add_row(
            "Total Biaya Hotel",
            f"${total_hotel_price:,.2f}",
            f"${new_hotel_total:,.2f}"
        )

    # Flight changes
    if 'outbound_flight_id' in new_data:
        table.add_row(
            "Flight Outbound",
            f"ID: {outbound_flight_id}",
            f"ID: {new_data['outbound_flight_id']}"
        )
        table.add_row(
            "Tanggal Outbound",
            "-",
            str(new_data.get('outbound_date', '-'))
        )
    
    if 'return_flight_id' in new_data:
        table.add_row(
            "Flight Return",
            f"ID: {return_flight_id}" if return_flight_id else "-",
            f"ID: {new_data['return_flight_id']}"
        )
        table.add_row(
            "Tanggal Return",
            "-",
            str(new_data.get('return_date', '-'))
        )
    
    if 'total_flight_price' in new_data:
        table.add_row(
            "Total Biaya Flight",
            f"${total_flight_price:,.2f}",
            f"${new_flight_total:,.2f}"
        )

    console.print("\n")
    header = Panel.fit(
        "[bold cyan]SISTEM MANAJEMEN TRAVEL[/bold cyan]",
        subtitle="[yellow]Capstone M1 - Tyson[/yellow]",
        border_style="cyan",
    )
    console.print(header, justify="center")

    # Trip summary
    table.add_row(
        "Periode Trip",
        f"{trip_start_date} s/d {trip_end_date} ({days} hari)",
        f"{new_start} s/d {new_end} ({new_days} hari)"
    )
    
    table.add_row(
        "TOTAL BIAYA",
        f"[bold yellow]${total_trip_cost:,.2f}[/bold yellow]",
        f"[bold cyan]${new_trip_total:,.2f}[/bold cyan]"
    )

    panel = Panel(table, title="[bold green]Konfirmasi Perubahan Reschedule[/bold green]", border_style="green")
    console.print(panel)
