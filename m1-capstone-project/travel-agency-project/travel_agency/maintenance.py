from mysql.connector import Error
from datetime import datetime, date

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .utils import _show_table, parse_date, parse_int

console = Console()


# =========================================================
# MANAGE TRIPS
# =========================================================

# ---------- MAINTAIN TRIPS ----------

def manage_trips(conn):
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
                    "[bold white][1][/bold white] Mencari & Mengubah Perjalanan",
                    "[bold white][2][/bold white] Mencari & Menghapus Perjalanan",
                    "",
                    "[bold white][0][/bold white] Kembali",
                ]
            ),
            title="[bold green]Menu Perjalanan (Transaksi)[/bold green]",
            border_style="green",
        )
        console.print(menu_panel)

        choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()
        if choice == "1":
            _search_and_update_trip(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "2":
            _search_and_delete_trip(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "0":
            break
        else:
            console.print("[red]Pilihan tidak valid.[/red]")
            console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

# ---------- LIST TRIPS ----------

def _list_trips(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                t.trip_id,
                u.name               AS user_name,
                COALESCE(c.name, '-') AS destination_city,
                t.trip_start_date,
                t.trip_end_date,
                t.status,
                t.total_trip_cost
            FROM trips t
            JOIN users u       ON t.user_id = u.user_id
            LEFT JOIN hotels h ON t.hotel_id = h.hotel_id
            LEFT JOIN cities c ON h.city_id = c.city_id
            ORDER BY t.trip_start_date DESC, t.trip_id DESC
            """
        )
        rows = cursor.fetchall()
        if not rows:
            console.print("[yellow]Belum ada data perjalanan.[/yellow]")
            return

        _show_table(
            "Daftar Perjalanan (Top 20)",
            ["ID Perjalanan", "Nama Pengguna", "Kota Tujuan", "Mulai", "Selesai", "Status", "Total Biaya"],
            rows,
        )
    except Error as e:
        console.print(f"[red]Error menampilkan perjalanan:[/red] {e}")
    finally:
        cursor.close()

# ---------- SEARCH TRIPS ----------

def _search_trips(conn):
    """
    Pencarian trip berdasarkan:
    - Trip ID
    - Nama pengguna
    - Kota tujuan (nama kota hotel)
    - Status (pending/confirmed/completed/cancelled)
    - Range tanggal (trip_start_date)
    """
    console.print("\n[dim]Silakan masukkan kriteria pencarian perjalanan.[/dim]\n")

    console.print("[bold green]Cari Perjalanan[/bold green]")
    console.print("[dim]Kosongkan field jika tidak ingin dipakai sebagai filter.[/dim]\n")

    trip_id_str = console.input("ID Perjalanan: ").strip()
    user_kw = console.input("Nama Pengguna: ").strip()
    city_kw = console.input("Nama Kota Tujuan: ").strip()
    status_kw = console.input("Status (pending/confirmed/completed/cancelled): ").strip().lower()
    date_from = console.input("Tanggal Mulai Perjalanan (YYYY-MM-DD): ").strip()
    date_to = console.input("Tanggal Selesai Perjalanan (YYY-MM-DD): ").strip()

    where = []
    params = []

    if trip_id_str:
        try:
            tid = int(trip_id_str)
            where.append("t.trip_id = %s")
            params.append(tid)
        except ValueError:
            console.print("[red]ID Perjalanan harus berupa angka.[/red]")
            return []

    if user_kw:
        where.append("u.name LIKE %s")
        params.append(f"%{user_kw}%")

    if city_kw:
        where.append("c.name LIKE %s")
        params.append(f"%{city_kw}%")

    if status_kw in ("pending", "confirmed", "completed", "cancelled"):
        where.append("t.status = %s")
        params.append(status_kw)

    if date_from:
        try:
            datetime.strptime(date_from, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Format tanggal mulai tidak valid.[/red]")
            return []
        where.append("t.trip_start_date >= %s")
        params.append(date_from)

    if date_to:
        try:
            datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Format tanggal akhir tidak valid.[/red]")
            return []
        where.append("t.trip_start_date <= %s")
        params.append(date_to)

    query = """
        SELECT 
            t.trip_id,
            u.name                AS user_name,
            COALESCE(c.name, '-') AS destination_city,
            t.trip_start_date,
            t.trip_end_date,
            t.status,
            t.total_trip_cost
        FROM trips t
        JOIN users u       ON t.user_id = u.user_id
        LEFT JOIN hotels h ON t.hotel_id = h.hotel_id
        LEFT JOIN cities c ON h.city_id = c.city_id
    """
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " ORDER BY t.trip_start_date DESC, t.trip_id DESC LIMIT 50"

    cursor = conn.cursor()
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        if not rows:
            console.print("[magenta]Tidak ada perjalanan yang cocok dengan kriteria.[/magenta]")
            return []
        _show_table(
            "Hasil Pencarian Perjalanan",
            ["ID Perjalanan", "Nama Pengguna", "Kota Tujuan", "Mulai", "Selesai", "Status", "Total Biaya"],
            rows,
        )
        return rows
    except Error as e:
        console.print(f"[red]Error saat mencari Perjalanan:[/red] {e}")
        return []
    finally:
        cursor.close()

# ---------- UPDATE TRIP (via search) ----------

def _search_and_update_trip(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Cari & Update Perjalanan[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_trips(conn)
    if not rows:
        return

    try:
        trip_id = int(console.input("[bold cyan]\nMasukkan ID Perjalanan yang akan Diubah: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID Perjalanan tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                t.trip_id,
                u.name                AS user_name,
                COALESCE(c.name, '-') AS destination_city,
                t.trip_start_date,
                t.trip_end_date,
                t.status,
                t.total_trip_cost,
                t.total_hotel_price,
                t.total_flight_price
            FROM trips t
            JOIN users u       ON t.user_id = u.user_id
            LEFT JOIN hotels h ON t.hotel_id = h.hotel_id
            LEFT JOIN cities c ON h.city_id = c.city_id
            WHERE t.trip_id = %s
            """,
            (trip_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Perjalanan tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Perjalanan Saat Ini",
            [
                "ID Perjalanan", "Nama Pengguna", "Kota Tujuan",
                "Mulai", "Selesai", "Status",
                "Total Perjalanan", "Total Hotel", "Total Penerbangan",
            ],
            [row],
        )

        console.print(
            "\n[cyan]Anda dapat mengubah status dan tanggal perjalanan.[/cyan]"
            "\n[dim]Kosongkan input jika tidak ingin mengubah field tersebut.[/dim]\n"
        )

        new_status = console.input(
            f"Status [{row[5]}] (pending/confirmed/completed/cancelled): "
        ).strip().lower()
        new_start = console.input(
            f"Tanggal Mulai [{row[3]}] (YYYY-MM-DD): "
        ).strip()
        new_end = console.input(
            f"Tanggal Selesai [{row[4]}] (YYYY-MM-DD): "
        ).strip()

        updates = []
        params = []

        if new_status:
            if new_status not in ("pending", "confirmed", "completed", "cancelled"):
                console.print("[red]Status tidak valid.[/red]")
                return
            updates.append("status = %s")
            params.append(new_status)

        # Validasi tanggal
        start_date_val = None
        end_date_val = None

        if new_start:
            try:
                start_date_val = datetime.strptime(new_start, "%Y-%m-%d").date()
            except ValueError:
                console.print("[red]Format tanggal mulai tidak valid.[/red]")
                return
        if new_end:
            try:
                end_date_val = datetime.strptime(new_end, "%Y-%m-%d").date()
            except ValueError:
                console.print("[red]Format tanggal selesai tidak valid.[/red]")
                return

        # Kalau hanya salah satu yang diisi, kita ambil yang lain dari data lama
        if start_date_val or end_date_val:
            if not start_date_val:
                start_date_val = row[3]   # trip_start_date lama
            if not end_date_val:
                end_date_val = row[4]     # trip_end_date lama

            if end_date_val < start_date_val:
                console.print("[red]Tanggal selesai tidak boleh sebelum tanggal mulai.[/red]")
                return

            days = (end_date_val - start_date_val).days

            updates.append("trip_start_date = %s")
            params.append(start_date_val)
            updates.append("trip_end_date = %s")
            params.append(end_date_val)
            updates.append("days = %s")
            params.append(days)

        if not updates:
            console.print("[magenta]Tidak ada perubahan yang dilakukan.[/magenta]")
            return

        params.append(trip_id)
        query = f"UPDATE trips SET {', '.join(updates)} WHERE trip_id = %s"
        cursor.execute(query, tuple(params))
        conn.commit()
        console.print("[bold green]✅ Data Perjalanan Berhasil Diubah.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error update perjalanan:[/red] {e}")
    finally:
        cursor.close()

# ---------- DELETE TRIP (via search) ----------

def _search_and_delete_trip(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Cari & Hapus Perjalanan[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_trips(conn)
    if not rows:
        return

    try:
        trip_id = int(console.input("[bold cyan]\nMasukkan ID Perjalanan yang akan Dihapus: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID Perjalanan tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                t.trip_id,
                u.name                AS user_name,
                COALESCE(c.name, '-') AS destination_city,
                t.trip_start_date,
                t.trip_end_date,
                t.status,
                t.total_trip_cost
            FROM trips t
            JOIN users u       ON t.user_id = u.user_id
            LEFT JOIN hotels h ON t.hotel_id = h.hotel_id
            LEFT JOIN cities c ON h.city_id = c.city_id
            WHERE t.trip_id = %s
            """,
            (trip_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Perjalanan tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Perjalanan yang akan Dihapus",
            ["ID Perjalanan", "Nama Pengguna", "Kota Tujuan", "Mulai", "Selesai", "Status", "Total Biaya"],
            [row],
        )

        confirm = console.input(
            "\n[bold red]Yakin ingin menghapus perjalanan ini? (y/n): [/bold red]"
        ).strip().lower()
        if confirm != "y":
            console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
            return

        # Trips tidak punya child (hanya child dari users/hotels/flights),
        # jadi aman untuk dihapus langsung.
        cursor.execute("DELETE FROM trips WHERE trip_id = %s", (trip_id,))
        conn.commit()
        console.print("[bold green]✅ Perjalanan berhasil dihapus.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error menghapus perjalanan:[/red] {e}")
    finally:
        cursor.close()



# =========================================================
# MANAGE FLIGHTS
# =========================================================

# ---------- MAINTAIN FLIGHTS ----------

def manage_flights(conn):
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
                    "[bold white][1][/bold white] Menambah Data Penerbangan Baru",
                    "[bold white][2][/bold white] Mencari & Mengubah Data Penerbangan",
                    "[bold white][3][/bold white] Mencari & Menghapus Data Penerbangan",
                    "",
                    "[bold white][0][/bold white] Kembali",
                ]
            ),
            title="[bold green]Menu Penerbangan[/bold green]",
            border_style="green",
        )
        console.print(menu_panel)

        choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()
        if choice == "1":
            _add_flight(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "2":
            _search_and_update_flight(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "3":
            _search_and_delete_flight(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "0":
            break
        else:
            console.print("[red]Pilihan tidak valid.[/red]")
            console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

# ---------- LIST FLIGHTS ----------

def _list_flights(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                f.flight_id,
                c_from.name AS from_city,
                c_to.name   AS to_city,
                a.name      AS airline,
                f.flight_type,
                f.direction,
                f.price,
                f.flight_date
            FROM flights f
            JOIN cities   c_from ON f.from_city_id = c_from.city_id
            JOIN cities   c_to   ON f.to_city_id   = c_to.city_id
            JOIN airlines a      ON f.airline_id   = a.airline_id
            ORDER BY f.flight_date, from_city, to_city
            """
        )
        rows = cursor.fetchall()
        if not rows:
            console.print("[yellow]Belum ada data penerbangan.[/yellow]")
            return

        _show_table(
            "Daftar Penerbangan (Top 20)",
            ["ID", "Dari Kota", "Ke Kota", "Maskapai", "Tipe", "Arah", "Harga (usd)", "Tanggal"],
            rows,
        )
    except Error as e:
        console.print(f"[red]Error menampilkan penerbangan:[/red] {e}")
    finally:
        cursor.close()

# ---------- ADD FLIGHT ----------

def _add_flight(conn):
    console.print("\n")
    header = Panel.fit(
    "[bold magenta]Tambah Penerbangan Baru[/bold magenta]",
    border_style="magenta",
    )
    console.print(header, justify="center")

    console.print("[bold magenta]\nMenentukan Maskapai Penerbangan Baru[/bold magenta]")

    rows = _search_airlines(conn)
    if not rows:
        return

    try:
        airline_id = int(console.input("[bold cyan]\nMasukkan ID Maskapai Penerbangan: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID maskapai tidak valid.[/red]")
        return
    
    print("\n")
    
    console.print("[bold magenta]\nMenentukan Rute Penerbangan Maskapai[/bold magenta]")

    rows = _search_cities(conn)
    if not rows:
        return

    try:
        from_city_id = int(console.input("[bold cyan]\nMasukkan ID Kota Asal Penerbangan: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID kota tidak valid.[/red]")
        return

    print("\n")
    rows = _search_cities(conn)
    if not rows:
        return

    try:
        to_city_id = int(console.input("[bold cyan]\nMasukkan ID Kota Tujuan Penerbangan: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID kota tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        # Validasi kota asal
        cursor.execute("SELECT name, country_name FROM cities WHERE city_id = %s", (from_city_id,))
        c_from = cursor.fetchone()
        if not c_from:
            console.print("[red]Kota asal tidak ditemukan.[/red]")
            return

        # Validasi kota tujuan
        cursor.execute("SELECT name, country_name FROM cities WHERE city_id = %s", (to_city_id,))
        c_to = cursor.fetchone()
        if not c_to:
            console.print("[red]Kota tujuan tidak ditemukan.[/red]")
            return

        console.print(
            f"\n[magenta]Rute:[/magenta] [bold]{c_from[0]}[/bold] → [bold]{c_to[0]}[/bold]"
        )
        
        cursor.execute("SELECT name FROM airlines WHERE airline_id = %s", (airline_id,))
        a_row = cursor.fetchone()
        
        if not a_row:
            console.print("[red]Maskapai tidak ditemukan.[/red]")
            return

        flight_type = console.input(
            "\nTipe Penerbangan (Pilihan: economy/business/first_class): "
        ).strip().lower()
        if flight_type not in ("economy", "business", "first_class"):
            console.print("[red]Tipe penerbangan tidak valid.[/red]")
            return

        direction = console.input(
            "Arah Penerbangan (outbound/return): "
        ).strip().lower()
        if direction not in ("outbound", "return"):
            console.print("[red]Arah penerbangan harus outbound atau return.[/red]")
            return

        price_str = console.input("Harga Tiket (usd): ").strip()
        time_str = console.input("Durasi Penerbangan (jam): ").strip()
        dist_str = console.input("Jarak Penerbangan (km): ").strip()
        flight_date = parse_date(console.input("Tanggal Penerbangan (YYYY-MM-DD): ").strip())

        if not (price_str and time_str and dist_str and flight_date):
            console.print("[red]Semua field wajib diisi.[/red]")
            return

        try:
            price = float(price_str)
            flight_time_hours = float(time_str)
            distance_km = float(dist_str)
        except ValueError:
            console.print("[red]Harga/durasi/jarak tidak valid.[/red]")
            return

        cursor.execute(
            """
            INSERT INTO flights (
                from_city_id,
                to_city_id,
                airline_id,
                flight_type,
                price,
                flight_time_hours,
                distance_km,
                direction,
                flight_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                from_city_id,
                to_city_id,
                airline_id,
                flight_type,
                price,
                flight_time_hours,
                distance_km,
                direction,
                flight_date,
            ),
        )
        conn.commit()
        console.print("[bold green]✅ Penerbangan baru berhasil ditambahkan.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error menambah penerbangan:[/red] {e}")
    finally:
        cursor.close()

# ---------- SEARCH FLIGHTS ----------

def _search_flights(conn):
    """
    Pencarian penerbangan berdasarkan:
    - Kota asal (nama, LIKE)
    - Kota tujuan (nama, LIKE)
    - Maskapai (nama, LIKE)
    - Arah (outbound/return)
    - Range tanggal (flight_date)
    - Range harga
    """
    console.print("\n[dim]Silakan masukkan kriteria pencarian penerbangan.[/dim]\n")

    console.print("[bold green]Cari Penerbangan[/bold green]")
    console.print("[dim]Kosongkan field jika tidak ingin dipakai sebagai filter.[/dim]\n")

    from_city_kw = console.input("Nama Kota Asal: ").strip()
    to_city_kw = console.input("Nama Kota Tujuan: ").strip()
    airline_kw = console.input("Nama Maskapai: ").strip()
    direction = console.input("Arah Penerbangan (outbound/return): ").strip().lower()
    date_from = console.input("Tanggal Keberangkatan (YYYY-MM-DD): ").strip()
    date_to = console.input("Tanggal Ketibaan (YYYY-MM-DD): ").strip()
    price_min_str = console.input("Harga minimum (usd): ").strip()
    price_max_str = console.input("Harga maksimum (usd): ").strip()

    where = []
    params = []

    if from_city_kw:
        where.append("c_from.name LIKE %s")
        params.append(f"%{from_city_kw}%")
    if to_city_kw:
        where.append("c_to.name LIKE %s")
        params.append(f"%{to_city_kw}%")
    if airline_kw:
        where.append("a.name LIKE %s")
        params.append(f"%{airline_kw}%")
    if direction in ("outbound", "return"):
        where.append("f.direction = %s")
        params.append(direction)

    if date_from:
        try:
            datetime.strptime(date_from, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Format tanggal mulai tidak valid.[/red]")
            return []
        where.append("f.flight_date >= %s")
        params.append(date_from)

    if date_to:
        try:
            datetime.strptime(date_to, "%Y-%m-%d")
        except ValueError:
            console.print("[red]Format tanggal akhir tidak valid.[/red]")
            return []
        where.append("f.flight_date <= %s")
        params.append(date_to)

    if price_min_str:
        try:
            pmin = float(price_min_str)
        except ValueError:
            console.print("[red]Harga minimum tidak valid.[/red]")
            return []
        where.append("f.price >= %s")
        params.append(pmin)

    if price_max_str:
        try:
            pmax = float(price_max_str)
        except ValueError:
            console.print("[red]Harga maksimum tidak valid.[/red]")
            return []
        where.append("f.price <= %s")
        params.append(pmax)

    query = """
        SELECT 
            f.flight_id,
            c_from.name AS from_city,
            c_to.name   AS to_city,
            a.name      AS airline,
            f.flight_type,
            f.direction,
            f.price,
            f.flight_date
        FROM flights f
        JOIN cities   c_from ON f.from_city_id = c_from.city_id
        JOIN cities   c_to   ON f.to_city_id   = c_to.city_id
        JOIN airlines a      ON f.airline_id   = a.airline_id
    """
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " ORDER BY f.flight_date, from_city, to_city LIMIT 50"

    cursor = conn.cursor()
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        if not rows:
            console.print("[magenta]Tidak ada penerbangan yang cocok dengan kriteria.[/magenta]")
            return []
        _show_table(
            "Hasil Pencarian Penerbangan",
            ["ID", "Dari Kota", "Ke Kota", "Maskapai", "Tipe", "Arah", "Harga (usd)", "Tanggal"],
            rows,
        )
        return rows
    except Error as e:
        console.print(f"[red]Error saat mencari penerbangan:[/red] {e}")
        return []
    finally:
        cursor.close()

# ---------- UPDATE FLIGHT (via search) ----------

def _search_and_update_flight(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Cari & Update Penerbangan[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_flights(conn)
    if not rows:
        return

    try:
        flight_id = int(console.input("[bold cyan]\nMasukkan ID Penerbangan yang akan Diubah: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID penerbangan tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                f.flight_id,
                f.from_city_id,
                c_from.name AS from_city,
                f.to_city_id,
                c_to.name   AS to_city,
                f.airline_id,
                a.name      AS airline,
                f.flight_type,
                f.price,
                f.flight_time_hours,
                f.distance_km,
                f.direction,
                f.flight_date
            FROM flights f
            JOIN cities   c_from ON f.from_city_id = c_from.city_id
            JOIN cities   c_to   ON f.to_city_id   = c_to.city_id
            JOIN airlines a      ON f.airline_id   = a.airline_id
            WHERE f.flight_id = %s
            """,
            (flight_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Penerbangan tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Penerbangan Saat Ini",
            [
                "ID", "From City ID", "From City",
                "To City ID", "To City",
                "Airline ID", "Airline",
                "Type", "Price", "Time (h)", "Distance (km)",
                "Direction", "Date",
            ],
            [row],
        )

        console.print("[dim]Kosongkan input jika tidak ingin mengubah field tersebut.[/dim]\n")

        
        updates = []
        params = []
        
        # From city
        change_from = console.input("[bold cyan]Ubah Kota Asal? (y/n): [/bold cyan]").strip().lower()
        new_from_city_id = None
        if change_from == "y":

            rows = _search_cities(conn)
            if not rows:
                return

            try:
                new_from_city_id = int(console.input("[bold cyan]Masukkan ID Kota Asal Baru: [/bold cyan]").strip())
            except ValueError:
                console.print("[red]ID kota tidak valid.[/red]")
                return

            if new_from_city_id is not None:
                # validasi FK kota
                cursor.execute("SELECT name, country_name FROM cities WHERE city_id = %s", (new_from_city_id,))
                city_check = cursor.fetchone()
                if not city_check:
                    console.print("[red]Kota asal baru tidak ditemukan.[/red]")
                    return
                
                console.print(
                    f"\nLokasi Kota Asal Baru Penerbangan berada di kota: [bold magenta]{city_check[0]}, {city_check[1]}[/bold magenta]"
                )
                updates.append("from_city_id = %s")
                params.append(new_from_city_id)


        print("\n")
        # To city
        change_to = console.input("Ubah Kota Tujuan? (y/n): ").strip().lower()
        new_to_city_id = None
        if change_to == "y":

            rows = _search_cities(conn)
            if not rows:
                return

            try:
                new_to_city_id = int(console.input("[bold cyan]Masukkan ID Kota Tujuan Baru: [/bold cyan]").strip())
            except ValueError:
                console.print("[red]ID kota tidak valid.[/red]")
                return

            if new_to_city_id is not None:
                # validasi FK kota
                cursor.execute("SELECT name, country_name FROM cities WHERE city_id = %s", (new_to_city_id,))
                city_check = cursor.fetchone()
                if not city_check:
                    console.print("[red]Kota tujuan baru tidak ditemukan.[/red]")
                    return
                
                console.print(
                    f"\nLokasi Kota Tujuan Baru Penerbangan berada di kota: [bold magenta]{city_check[0]}, {city_check[1]}[/bold magenta]"
                )

                updates.append("to_city_id = %s")
                params.append(new_to_city_id)


        print("\n")

        # Airline
        change_airline = console.input("\nUbah Maskapai? (y/n): ").strip().lower()
        new_airline_id = None
        if change_airline == "y":

            rows = _search_airlines(conn)
            if not rows:
                return

            try:
                new_airline_id = int(console.input("[bold cyan]\nMasukkan ID Maskapai Baru: [/bold cyan]").strip())
            except ValueError:
                console.print("[red]ID maskapai tidak valid.[/red]")
                return

        new_type = console.input(f"\nTipe Penerbangan (Pilihan: economy/business/first_class) ([yellow bold]{row[7]}[/yellow bold]): ",
            markup=True
        ).strip().lower()
            
        new_price_str = console.input(f"Harga (usd) ([yellow bold]{row[8]}[/yellow bold]): ",
            markup=True
        ).strip()
            
        new_time_str = console.input(f"Durasi (jam) ([yellow bold]{row[9]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_dist_str = console.input(f"Jarak (km) ([yellow bold]{row[10]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_direction = console.input(f"Arah Penerbangan (Pilihan: outbound/return) ([yellow bold]{row[11]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_date = console.input(f"Tanggal (YYYY-MM-DD) ([yellow bold]{row[12]}[/yellow bold]): ",
            markup=True
        ).strip()


        if new_airline_id is not None:
            cursor.execute("SELECT name FROM airlines WHERE airline_id = %s", (new_airline_id,))
            if not cursor.fetchone():
                console.print("[red]Maskapai baru tidak ditemukan.[/red]")
                return
            updates.append("airline_id = %s")
            params.append(new_airline_id)

        # Non-FK fields
        if new_type:
            if new_type not in ("economy", "business", "first_class"):
                console.print("[red]Tipe penerbangan tidak valid.[/red]")
                return
            updates.append("flight_type = %s")
            params.append(new_type)

        if new_price_str:
            try:
                new_price = float(new_price_str)
            except ValueError:
                console.print("[red]Harga tidak valid.[/red]")
                return
            updates.append("price = %s")
            params.append(new_price)

        if new_time_str:
            try:
                new_time = float(new_time_str)
            except ValueError:
                console.print("[red]Durasi tidak valid.[/red]")
                return
            updates.append("flight_time_hours = %s")
            params.append(new_time)

        if new_dist_str:
            try:
                new_dist = float(new_dist_str)
            except ValueError:
                console.print("[red]Jarak tidak valid.[/red]")
                return
            updates.append("distance_km = %s")
            params.append(new_dist)

        if new_direction:
            if new_direction not in ("outbound", "return"):
                console.print("[red]Arah harus outbound atau return.[/red]")
                return
            updates.append("direction = %s")
            params.append(new_direction)

        if new_date:
            try:
                datetime.strptime(new_date, "%Y-%m-%d")
            except ValueError:
                console.print("[red]Format tanggal tidak valid.[/red]")
                return
            updates.append("flight_date = %s")
            params.append(new_date)

        if not updates:
            console.print("[magenta]Tidak ada perubahan yang dilakukan.[/magenta]")
            return

        params.append(flight_id)
        query = f"UPDATE flights SET {', '.join(updates)} WHERE flight_id = %s"
        cursor.execute(query, tuple(params))
        conn.commit()
        console.print("[bold green]✅ Data Penerbangan Berhasil Diubah.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error update penerbangan:[/red] {e}")
    finally:
        cursor.close()

# ---------- DELETE FLIGHT (via search) ----------

def _search_and_delete_flight(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Cari & Hapus Penerbangan[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_flights(conn)
    if not rows:
        return

    try:
        flight_id = int(console.input("[bold cyan]\nMasukkan ID Penerbangan yang akan Dihapus: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID penerbangan tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        # cek apakah flight dipakai di trips (outbound / return)
        cursor.execute(
            """
            SELECT 
                SUM(CASE WHEN outbound_flight_id = %s THEN 1 ELSE 0 END) AS as_outbound,
                SUM(CASE WHEN return_flight_id   = %s THEN 1 ELSE 0 END) AS as_return
            FROM trips
            """,
            (flight_id, flight_id),
        )
        row_usage = cursor.fetchone()
        as_outbound = row_usage[0] or 0
        as_return = row_usage[1] or 0
        total_usage = as_outbound + as_return

        cursor.execute(
            """
            SELECT 
                f.flight_id,
                c_from.name AS from_city,
                c_to.name   AS to_city,
                a.name      AS airline,
                f.flight_type,
                f.direction,
                f.price,
                f.flight_date
            FROM flights f
            JOIN cities   c_from ON f.from_city_id = c_from.city_id
            JOIN cities   c_to   ON f.to_city_id   = c_to.city_id
            JOIN airlines a      ON f.airline_id   = a.airline_id
            WHERE f.flight_id = %s
            """,
            (flight_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Penerbangan tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Penerbangan yang akan Dihapus",
            ["ID", "Dari Kota", "Ke Kota", "Maskapai", "Tipe", "Arah", "Harga (usd)", "Tanggal"],
            [row],
        )

        console.print(
            f"[yellow]Penerbangan ini digunakan di {total_usage} trip "
            f"(sebagai outbound: {as_outbound}, sebagai return: {as_return}).[/yellow]"
        )

        confirm = console.input(
            "\n[bold red]Yakin ingin menghapus penerbangan ini? (y/n): [/bold red]"
        ).strip().lower()
        if confirm != "y":
            console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
            return

        if total_usage > 0:
            console.print(
                "[red]Tidak dapat menghapus penerbangan yang masih digunakan di perjalanan (FK constraint).[/red]"
            )
            console.print(
                "[dim]Batalkan / ubah perjalanan terkait terlebih dahulu jika benar-benar harus dihapus.[/dim]"
            )
            return

        cursor.execute("DELETE FROM flights WHERE flight_id = %s", (flight_id,))
        conn.commit()
        console.print("[bold green]✅ Penerbangan berhasil dihapus.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error menghapus penerbangan:[/red] {e}")
    finally:
        cursor.close()




# =========================================================
# MANAGE HOTELS
# =========================================================

# ---------- MAINTAIN HOTELS ----------

def manage_hotels(conn):
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
                    "[bold white][1][/bold white] Menambah Data Hotel Baru",
                    "[bold white][2][/bold white] Mencari & Mengubah Data Hotel",
                    "[bold white][3][/bold white] Mencari & Menghapus Data Hotel",
                    "",
                    "[bold white][0][/bold white] Kembali",
                ]
            ),
            title="[bold green]Menu Hotel[/bold green]",
            border_style="green",
        )
        console.print(menu_panel)

        choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()
        if choice == "1":
            _add_hotel(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "2":
            _search_and_update_hotel(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "3":
            _search_and_delete_hotel(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "0":
            break
        else:
            console.print("[red]Pilihan tidak valid.[/red]")
            console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

# ---------- LIST HOTELS ----------

def _list_hotels(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                h.hotel_id,
                h.hotel_name,
                c.name       AS city,
                c.country_name,
                h.price_per_day,
                REPEAT('★', h.star_rating),
                h.established_date
            FROM hotels h
            JOIN cities c ON h.city_id = c.city_id
            ORDER BY c.country_name, c.name, h.hotel_name
            """
        )
        rows = cursor.fetchall()
        if not rows:
            console.print("[yellow]Belum ada data hotel.[/yellow]")
            return

        _show_table(
            "Daftar Hotel (Top 20)",
            ["ID", "Nama Hotel", "Kota", "Negara", "Harga/Malam (usd)", "Star", "Tgl Berdiri"],
            rows,
        )
    except Error as e:
        console.print(f"[red]Error menampilkan hotel:[/red] {e}")
    finally:
        cursor.close()

# ---------- ADD HOTEL ----------

def _add_hotel(conn):
    console.print("\n")
    header = Panel.fit(
    "[bold magenta]Tambah Hotel Baru[/bold magenta]",
    border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_cities(conn)
    if not rows:
        return

    try:
        city_id = int(console.input("[bold cyan]\nMasukkan ID Kota Lokasi Hotel: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID kota tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        # Validasi FK city
        cursor.execute("SELECT name, country_name FROM cities WHERE city_id = %s", (city_id,))
        city_row = cursor.fetchone()
        if not city_row:
            console.print("[red]Kota tidak ditemukan.[/red]")
            return

        console.print(
            f"\nHotel berlokasi di kota:[bold yellow]{city_row[0]}, {city_row[1]}[/bold yellow]"
        )

        hotel_name = console.input("\nNama Hotel: ").strip()
        price_str = console.input("Harga per Malam (usd): ").strip()
        star_str = console.input("Star Rating (1-5): ").strip()
        est_date = parse_date(console.input("Tanggal Berdiri (YYYY-MM-DD): ").strip())

        if not (hotel_name, price_str and star_str and est_date):
            console.print("[red]Harga, star rating, dan tanggal berdiri wajib diisi.[/red]")
            return

        try:
            price_per_day = float(price_str)
            star_rating = int(star_str)
        except ValueError:
            console.print("[red]Harga/star rating tidak valid.[/red]")
            return

        cursor.execute(
            """
            INSERT INTO hotels (hotel_name, city_id, price_per_day, star_rating, established_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (hotel_name, city_id, price_per_day, star_rating, est_date),
        )
        conn.commit()
        console.print("[bold green]✅ Hotel baru berhasil ditambahkan.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error menambah hotel:[/red] {e}")
    finally:
        cursor.close()

# ---------- SEARCH HOTELS ----------

def _search_hotels(conn):
    """
    Pencarian hotel berdasarkan:
    - Nama hotel (LIKE)
    - Nama kota (LIKE)
    - Nama negara (LIKE)
    - Star rating (1-5)
    - Range harga (min/max)
    """
    console.print("\n[dim]Silakan masukkan kriteria pencarian hotel.[/dim]\n")

    console.print("[bold green]Cari Hotel[/bold green]")
    console.print("[dim]Kosongkan input jika tidak ingin menjadikannya filter.[/dim]\n")

    name_kw = console.input("Nama Hotel: ").strip()
    city_kw = console.input("Nama Kota: ").strip()
    country_kw = console.input("Nama Negara: ").strip()
    star_str = console.input("Star rating (1-5): ").strip()
    price_min_str = console.input("Harga Minimum (usd): ").strip()
    price_max_str = console.input("Harga Maksimum (usd): ").strip()

    where = []
    params = []

    if name_kw:
        where.append("h.hotel_name LIKE %s")
        params.append(f"%{name_kw}%")
    if city_kw:
        where.append("c.name LIKE %s")
        params.append(f"%{city_kw}%")
    if country_kw:
        where.append("c.country_name LIKE %s")
        params.append(f"%{country_kw}%")
    if star_str:
        try:
            star_val = int(star_str)
            where.append("h.star_rating = %s")
            params.append(star_val)
        except ValueError:
            console.print("[red]Star rating harus berupa angka 1-5.[/red]")
            return []

    if price_min_str:
        try:
            pmin = float(price_min_str)
            where.append("h.price_per_day >= %s")
            params.append(pmin)
        except ValueError:
            console.print("[red]Harga minimum tidak valid.[/red]")
            return []

    if price_max_str:
        try:
            pmax = float(price_max_str)
            where.append("h.price_per_day <= %s")
            params.append(pmax)
        except ValueError:
            console.print("[red]Harga maksimum tidak valid.[/red]")
            return []

    query = """
        SELECT 
            h.hotel_id,
            h.hotel_name,
            c.name         AS city,
            c.country_name AS country,
            h.price_per_day,
            REPEAT('★', h.star_rating),
            h.established_date
        FROM hotels h
        JOIN cities c ON h.city_id = c.city_id
    """
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " ORDER BY c.country_name, c.name, h.hotel_name LIMIT 50"

    cursor = conn.cursor()
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        if not rows:
            console.print("[magenta]Tidak ada hotel yang cocok dengan kriteria.[/magenta]")
            return []
        _show_table(
            "Hasil Pencarian Hotel",
            ["ID", "Nama Hotel", "Kota", "Negara", "Harga/Malam (usd)", "Star", "Tgl Berdiri"],
            rows,
        )
        return rows
    except Error as e:
        console.print(f"[red]Error saat mencari hotel:[/red] {e}")
        return []
    finally:
        cursor.close()

# ---------- UPDATE HOTEL (via search) ----------

def _search_and_update_hotel(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Mengubah Data Hotel[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_hotels(conn)
    if not rows:
        return

    try:
        hotel_id = int(console.input("[bold cyan]\nMasukkan ID Hotel yang akan Diubah: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID hotel tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                h.hotel_id,
                h.hotel_name,
                h.city_id,
                c.name         AS city_name,
                c.country_name AS country_name,
                h.price_per_day,
                REPEAT('★', h.star_rating),
                h.established_date
            FROM hotels h
            JOIN cities c ON h.city_id = c.city_id
            WHERE h.hotel_id = %s
            """,
            (hotel_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Hotel tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Hotel Saat Ini",
            ["ID", "Nama Hotel", "City ID", "Nama Kota", "Negara", "Harga/Malam (usd)", "Star", "Tgl Berdiri"],
            [row],
        )

        updates = []
        params = []

        console.print("[dim]Kosongkan input jika tidak ingin mengubah field tersebut.[/dim]\n")
        new_name = console.input(f"Nama Hotel ([yellow bold]{row[1]}[/yellow bold]): ",
            markup=True
        ).strip()

        change_city = console.input("Ubah kota? (y/n): ").strip().lower()
        new_city_id = None
        if change_city == "y":

            rows = _search_cities(conn)
            if not rows:
                return

            try:
                new_city_id = int(console.input("[bold cyan]Masukkan ID Kota Baru: [/bold cyan]").strip())
            except ValueError:
                console.print("[red]ID kota tidak valid.[/red]")
                return

            if new_city_id is not None:
                # validasi FK kota
                cursor.execute("SELECT name, country_name FROM cities WHERE city_id = %s", (new_city_id,))
                city_check = cursor.fetchone()
                if not city_check:
                    console.print("[red]Kota baru tidak ditemukan.[/red]")
                    return
                
                console.print(
                    f"\nLokasi baru hotel berada di kota: [bold magenta]{city_check[0]}, {city_check[1]}[/bold magenta]"
                )
                updates.append("city_id = %s")
                params.append(new_city_id)
        
        new_price_str = console.input(f"\nHarga/Malam (usd) ([yellow bold]{row[5]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_star_str = console.input(f"Star Rating (1-5) ([yellow bold]{row[6]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_est_date = console.input(f"Tanggal Berdiri (YYYY-MM-DD) ([yellow bold]{row[7]}[/yellow bold]): ",
            markup=True
        ).strip()


        if new_name:
            updates.append("hotel_name = %s")
            params.append(new_name)

        if new_price_str:
            try:
                new_price = float(new_price_str)
            except ValueError:
                console.print("[red]Harga tidak valid.[/red]")
                return
            updates.append("price_per_day = %s")
            params.append(new_price)

        if new_star_str:
            try:
                new_star = int(new_star_str)
            except ValueError:
                console.print("[red]Star rating tidak valid.[/red]")
                return
            updates.append("star_rating = %s")
            params.append(new_star)

        if new_est_date:
            try:
                datetime.strptime(new_est_date, "%Y-%m-%d")
            except ValueError:
                console.print("[red]Format tanggal tidak valid.[/red]")
                return
            updates.append("established_date = %s")
            params.append(new_est_date)

        if not updates:
            console.print("[magenta]Tidak ada perubahan yang dilakukan.[/magenta]")
            return

        params.append(hotel_id)
        query = f"UPDATE hotels SET {', '.join(updates)} WHERE hotel_id = %s"
        cursor.execute(query, tuple(params))
        conn.commit()
        console.print("[bold green]✅ Data Hotel Berhasil Diubah.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error update hotel:[/red] {e}")
    finally:
        cursor.close()

# ---------- DELETE HOTEL (via search) ----------

def _search_and_delete_hotel(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Cari & Hapus Hotel[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_hotels(conn)
    if not rows:
        return

    try:
        hotel_id = int(console.input("[bold cyan]\nMasukkan ID Hotel yang akan Dihapus: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID hotel tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        # cek apakah hotel dipakai di trips
        cursor.execute("SELECT COUNT(*) FROM trips WHERE hotel_id = %s", (hotel_id,))
        trip_count = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT 
                h.hotel_id,
                h.hotel_name,
                c.name         AS city_name,
                c.country_name AS country_name,
                h.price_per_day,
                REPEAT('★', h.star_rating),
                h.established_date
            FROM hotels h
            JOIN cities c ON h.city_id = c.city_id
            WHERE h.hotel_id = %s
            """,
            (hotel_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Hotel tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Hotel yang akan Dihapus",
            ["ID", "Nama Hotel", "Kota", "Negara", "Harga/Malam (usd)", "Star", "Tgl Berdiri"],
            [row],
        )

        console.print(
            f"[yellow]Hotel ini terkait dengan {trip_count} trip di tabel Perjalanan.[/yellow]"
        )

        confirm = console.input(
            "\n[bold red]Yakin ingin menghapus hotel ini? (y/n): [/bold red]"
        ).strip().lower()
        if confirm != "y":
            console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
            return

        if trip_count > 0:
            console.print(
                "[red]Tidak dapat menghapus hotel yang masih digunakan di perjalanan (FK constraint).[/red]"
            )
            console.print(
                "[dim]Batalkan / hapus perjalanan terkait terlebih dahulu jika memang harus dihapus.[/dim]"
            )
            return

        cursor.execute("DELETE FROM hotels WHERE hotel_id = %s", (hotel_id,))
        conn.commit()
        console.print("[bold green]✅ Hotel berhasil dihapus.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error menghapus hotel:[/red] {e}")
    finally:
        cursor.close()



# =========================================================
# MANAGE USERS
# =========================================================

# ---------- MAINTAIN USERS ----------

def manage_users(conn):
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
                    "[bold white][1][/bold white] Menambah Data Pengguna Baru",
                    "[bold white][2][/bold white] Mencari & Mengubah Data Pengguna",
                    "[bold white][3][/bold white] Mencari & Menghapus Data Pengguna",
                    "",
                    "[bold white][0][/bold white] Kembali",
                ]
            ),
            title="[bold green]Menu Pengguna[/bold green]",
            border_style="green",
        )
        console.print(menu_panel)

        choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()
        if choice == "1":
            _add_user(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "2":
            _search_and_update_user(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "3":
            _search_and_delete_user(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "0":
            break
        else:
            console.print("[red]Pilihan tidak valid.[/red]")
            console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

# ---------- LIST USERS ----------

def _list_users(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT user_id, name, gender, birth_date, marital_status,
                   occupation, company, created_at
            FROM users
            ORDER BY user_id
            """
        )
        rows = cursor.fetchall()
        if not rows:
            console.print("[yellow]Belum ada data pengguna.[/yellow]")
            return
        _show_table(
            "Daftar Pengguna (Top 20)",
            ["ID", "Nama", "Jenis Kelamin", "Tanggal Lahir", "Status", "Pekerjaan", "Perusahaan", "Dibuat"],
            rows,
        )
    except Error as e:
        console.print(f"[red]Error menampilkan pengguna:[/red] {e}")
    finally:
        cursor.close()

# ---------- ADD USER ----------

def _add_user(conn):
 
    console.print("\n")
    header = Panel.fit(
    "[bold magenta]Tambah Pengguna Baru[/bold magenta]",
    border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    name = console.input("Nama lengkap: ").strip()
    gender = console.input("Jenis kelamin (laki-laki/perempuan): ").strip().lower()
    birth_date = parse_date(console.input("Tanggal lahir (YYYY-MM-DD): ").strip().lower())
    marital_status = console.input("Status pernikahan (belum menikah/menikah/cerai): ").strip().lower()
    occupation = console.input("Pekerjaan: ").strip()
    company = console.input("Perusahaan: ").strip()

    if not (name and gender and birth_date and marital_status and occupation and company):
        console.print("[red]Semua field wajib diisi.[/red]")
        return

    if gender not in ("laki-laki", "perempuan"):
        console.print("[red]Jenis kelamin harus laki-laki/perempuan.[/red]")
        return
    if marital_status not in ("belum menikah", "menikah", "cerai"):
        console.print("[red]Status pernikahan harus belum menikah/menikah/cerai.[/red]")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (name, gender, birth_date, marital_status, occupation, company)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (name, gender, birth_date, marital_status, occupation, company),
        )
        conn.commit()
        console.print("[bold green]✅ Pengguna baru berhasil ditambahkan.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error menambah pengguna:[/red] {e}")
    finally:
        cursor.close()

# ---------- SEARCH USERS ----------

def _search_users(conn):
    """
    Pencarian fleksibel berdasarkan:
    - nama (LIKE)
    - company (LIKE)
    - occupation (LIKE)
    - gender
    - marital_status
    """
    console.print("\n[dim]Silakan masukkan kriteria pencarian pengguna.[/dim]\n")

    console.print("[bold green]Cari Pengguna[/bold green]")
    console.print("[dim]Kosongkan field jika tidak ingin dipakai sebagai filter.[/dim]\n")

    name_kw = console.input("Nama: ").strip()
    company_kw = console.input("Perusahaan: ").strip()
    occupation_kw = console.input("Pekerjaan: ").strip()
    gender = console.input("Jenis Kelamin (laki-laki/perempuan): ").strip().lower()
    marital = console.input("Status Pernikahan (belum menikah/menikah/cerai): ").strip().lower()

    where = []
    params = []

    if name_kw:
        where.append("name LIKE %s")
        params.append(f"%{name_kw}%")
    if company_kw:
        where.append("company LIKE %s")
        params.append(f"%{company_kw}%")
    if occupation_kw:
        where.append("occupation LIKE %s")
        params.append(f"%{occupation_kw}%")
    if gender in ("laki-laki", "perempuan"):
        where.append("gender = %s")
        params.append(gender)
    if marital in ("belum menikah", "menikah", "cerai"):
        where.append("marital_status = %s")
        params.append(marital)

    query = """
        SELECT user_id, name, gender, birth_date, marital_status,
               occupation, company, created_at
        FROM users
    """
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " ORDER BY user_id LIMIT 50"

    cursor = conn.cursor()
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        if not rows:
            console.print("[magenta]Tidak ada pengguna yang cocok dengan kriteria.[/magenta]")
            return []
        _show_table(
            "Hasil Pencarian Pengguna",
            ["ID", "Nama", "Jenis Kelamin", "Tanggal Lahir", "Status", "Pekerjaan", "Perusahaan", "Dibuat"],
            rows,
        )
        return rows
    except Error as e:
        console.print(f"[red]Error saat mencari pengguna:[/red] {e}")
        return []
    finally:
        cursor.close()

# ---------- UPDATE USER (via search) ----------

def _search_and_update_user(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Mengubah Data Pengguna [/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_users(conn)
    if not rows:
        return

    try:
        user_id = int(console.input("[bold cyan]\nMasukkan ID Pengguna yang akan Diubah: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT user_id, name, gender, birth_date, marital_status,
                   occupation, company
            FROM users
            WHERE user_id = %s
            """,
            (user_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Pengguna tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Pengguna Saat Ini",
            ["ID", "Nama", "Jenis Kelamin", "Tanggal Lahir", "Status", "Pekerjaan", "Perusahaan"],
            [row],
        )

        console.print("[dim]Kosongkan input jika tidak ingin mengubah field tersebut.[/dim]\n")
        new_name = console.input(
            f"Nama ([yellow bold]{row[1]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_gender = console.input(
            f"Jenis Kelamin (Pilihan: laki-laki/perempuan) ([yellow bold]{row[2]}[/yellow bold]): ",
            markup=True
        ).strip().lower()

        new_birth_date = console.input(
            f"Tanggal Lahir (YYYY-MM-DD) ([yellow bold]{row[3]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_marital = console.input(
            f"Status Pernikahan (Pilihan: belum menikah/kawin/cerai) ([yellow bold]{row[4]}[/yellow bold]): ",
            markup=True
        ).strip().lower()

        new_occ = console.input(
            f"Pekerjaan ([yellow bold]{row[5]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_comp = console.input(
            f"Perusahaan ([yellow bold]{row[6]}[/yellow bold]): ",
            markup=True
        ).strip()

        updates = []
        params = []

        if new_name:
            updates.append("name = %s")
            params.append(new_name)
        if new_gender:
            if new_gender not in ("laki-laki", "perempuan"):
                console.print("[red]Jenis kelamin harus laki-laki/perempuan.[/red]")
                return
            updates.append("gender = %s")
            params.append(new_gender)
        if new_birth_date:
            try:
                datetime.strptime(new_birth_date, "%Y-%m-%d")
            except ValueError:
                console.print("[red]Format tanggal lahir tidak valid.[/red]")
                return
            updates.append("birth_date = %s")
            params.append(new_birth_date)
        if new_marital:
            if new_marital not in ("belum menikah", "menikah", "cerai"):
                console.print("[red]Status pernikahan tidak valid.[/red]")
                return
            updates.append("marital_status = %s")
            params.append(new_marital)
        if new_occ:
            updates.append("occupation = %s")
            params.append(new_occ)
        if new_comp:
            updates.append("company = %s")
            params.append(new_comp)

        if not updates:
            console.print("[magenta]Tidak ada perubahan yang dilakukan.[/magenta]")
            return

        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = %s"
        cursor.execute(query, tuple(params))
        conn.commit()
        console.print("[bold green]✅ Data Pengguna Berhasil Diubah.[/bold green]")

    except Error as e:
        conn.rollback()
        console.print(f"[red]Error update pengguna:[/red] {e}")
    finally:
        cursor.close()

# ---------- DELETE USER (via search) ----------

def _search_and_delete_user(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Cari & Hapus Pengguna[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_users(conn)
    if not rows:
        return

    try:
        user_id = int(console.input("[bold cyan]\nMasukkan ID Pengguna yang akan Dihapus: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID tidak valid.[/red]")
        return

    # Cek apakah user punya trip (FK)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM trips WHERE user_id = %s", (user_id,))
        trip_count = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT user_id, name, gender, birth_date, marital_status,
                   occupation, company
            FROM users
            WHERE user_id = %s
            """,
            (user_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Pengguna tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Pengguna yang akan Dihapus",
            ["ID", "Nama", "Jenis Kelamin", "Tanggal Lahir", "Status", "Pekerjaan", "Perusahaan"],
            [row],
        )
        console.print(f"[yellow]Pengguna ini memiliki {trip_count} trip terkait.[/yellow]")

        confirm = console.input(
            "\n[bold red]Yakin ingin menghapus pengguna ini? (y/n): [/bold red]"
        ).strip().lower()
        if confirm != "y":
            console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
            return

        if trip_count > 0:
            console.print(
                "[red]Tidak dapat menghapus pengguna yang masih memiliki perjalanan terkait (FK constraint).[/red]"
            )
            console.print("[dim]Hapus/cancel perjalanan terlebih dahulu jika memang diperlukan.[/dim]")
            return

        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()
        console.print("[bold green]✅ Pengguna berhasil dihapus.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error menghapus pengguna:[/red] {e}")
    finally:
        cursor.close()



# =========================================================
# MANAGE AIRLINES
# =========================================================

# ---------- MAINTAIN AIRLINES ----------

def manage_airlines(conn):
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
                    "[bold white][1][/bold white] Menambah Data Maskapai Baru",
                    "[bold white][2][/bold white] Mencari & Mengubah Data Maskapai",
                    "[bold white][3][/bold white] Mencari & Menghapus Data Maskapai",
                    "",
                    "[bold white][0][/bold white] Kembali",
                ]
            ),
            title="[bold green]Menu Maskapai[/bold green]",
            border_style="green",
        )
        console.print(menu_panel)

        choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()
        if choice == "1":
            _add_airline(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "2":
            _search_and_update_airline(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "3":
            _search_and_delete_airline(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "0":
            break
        else:
            console.print("[red]Pilihan tidak valid.[/red]")
            console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

# -------- LIST AIRLINES --------

def _list_airlines(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT airline_id, code, name, country, created_at
            FROM airlines
            ORDER BY name
            """
        )
        rows = cursor.fetchall()

        if not rows:
            console.print("[yellow]Belum ada data maskapai.[/yellow]")
            return

        _show_table(
            "Daftar Maskapai (Top 50)",
            ["ID", "Kode", "Nama Maskapai", "Negara", "Dibuat"],
            rows,
        )
    except Error as e:
        console.print(f"[red]Error menampilkan maskapai:[/red] {e}")
    finally:
        cursor.close()

# -------- ADD AIRLINE --------

def _add_airline(conn):
    
    console.print("\n")
    header = Panel.fit(
    "[bold magenta]Tambah Maskapai Baru[/bold magenta]",
    border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    code = console.input("Kode Maskapai (IATA 2–3 huruf): ").strip().upper()
    name = console.input("Nama Maskapai: ").strip()
    country = console.input("Negara Asal Maskapai: ").strip()

    if not code or not name or not country:
        console.print("[red]Semua field wajib diisi.[/red]")
        return

    if len(code) not in (2, 3):
        console.print("[red]Kode maskapai harus 2 atau 3 huruf (IATA).[/red]")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO airlines (code, name, country)
            VALUES (%s, %s, %s)
            """,
            (code, name, country),
        )
        conn.commit()
        console.print("[bold green]✅ Maskapai berhasil ditambahkan.[/bold green]")

    except Error as e:
        conn.rollback()
        if "Duplicate" in str(e):
            console.print(
                "[red]Kode maskapai sudah terdaftar![/red]"
            )
        else:
            console.print(f"[red]Error menambah maskapai:[/red] {e}")
    finally:
        cursor.close()

# -------- SEARCH AIRLINES --------

def _search_airlines(conn):

    console.print("\n[dim]Silakan masukkan kriteria pencarian maskapai.[/dim]\n")

    console.print("[bold green]Cari Maskapai[/bold green]")
    console.print("[dim]Kosongkan field jika tidak ingin digunakan sebagai filter.[/dim]\n")

    code_kw = console.input("Kode Maskapai: ").strip().upper()
    name_kw = console.input("Nama Maskapai: ").strip()
    country_kw = console.input("Negara Maskapai: ").strip()

    where = []
    params = []

    if code_kw:
        where.append("code LIKE %s")
        params.append(f"%{code_kw}%")
    if name_kw:
        where.append("name LIKE %s")
        params.append(f"%{name_kw}%")
    if country_kw:
        where.append("country LIKE %s")
        params.append(f"%{country_kw}%")

    query = """
        SELECT airline_id, code, name, country
        FROM airlines
    """
    if where:
        query += " WHERE " + " AND ".join(where)

    query += " ORDER BY name LIMIT 100"

    cursor = conn.cursor()

    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            console.print("[magenta]Tidak ada maskapai sesuai pencarian.[/magenta]")
            return []

        _show_table(
            "Hasil Pencarian Maskapai",
            ["ID", "Kode", "Nama Maskapai", "Negara"],
            rows,
        )
        return rows

    except Error as e:
        console.print(f"[red]Error mencari maskapai:[/red] {e}")
        return []
    finally:
        cursor.close()

# -------- UPDATE AIRLINE (via search) --------

def _search_and_update_airline(conn):
    console.print("\n")
    
    header = Panel.fit(
        "[bold magenta]Cari & Update Maskapai[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_airlines(conn)
    if not rows:
        return

    try:
        airline_id = int(console.input("[bold cyan]\nMasukkan ID Maskapai yang akan Diubah: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID maskapai tidak valid.[/red]")
        return

    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT airline_id, code, name, country
            FROM airlines
            WHERE airline_id = %s
            """,
            (airline_id,),
        )
        row = cursor.fetchone()

        if not row:
            console.print("[red]Maskapai tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Maskapai Saat Ini",
            ["ID", "Kode", "Nama", "Negara"],
            [row],
        )

        console.print("[dim]Kosongkan field jika tidak ingin mengubah nilainya.[/dim]\n")

        new_code = console.input(f"Kode Maskapai ([yellow bold]{row[1]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_name = console.input(f"Nama Maskapai ([yellow bold]{row[2]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_country = console.input(f"Negara Maskapai ([yellow bold]{row[3]}[/yellow bold]): ",
            markup=True
        ).strip()

        updates = []
        params = []

        if new_code:
            if len(new_code) not in (2, 3):
                console.print("[red]Kode maskapai harus 2–3 huruf.[/red]")
                return
            updates.append("code = %s")
            params.append(new_code)

        if new_name:
            updates.append("name = %s")
            params.append(new_name)

        if new_country:
            updates.append("country = %s")
            params.append(new_country)

        if not updates:
            console.print("[magenta]Tidak ada perubahan dilakukan.[/magenta]")
            return

        params.append(airline_id)

        cursor.execute(
            f"UPDATE airlines SET {', '.join(updates)} WHERE airline_id = %s",
            tuple(params),
        )
        conn.commit()

        console.print("[bold green]✅ Maskapai berhasil diperbarui.[/bold green]")

    except Error as e:
        conn.rollback()
        if "Duplicate" in str(e):
            console.print("[red]Kode maskapai sudah digunakan.[/red]")
        else:
            console.print(f"[red]Error update maskapai:[/red] {e}")
    finally:
        cursor.close()

# -------- DELETE AIRLINE (via search) --------

def _search_and_delete_airline(conn):
    console.print("\n")
    
    header = Panel.fit(
        "[bold magenta]Cari & Hapus Maskapai[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_airlines(conn)
    if not rows:
        return

    try:
        airline_id = int(console.input("[bold cyan]\nMasukkan ID Maskapai yang akan Dihapus: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID maskapai tidak valid.[/red]")
        return

    cursor = conn.cursor()

    try:
        # Cek apakah dipakai di flights
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM flights
            WHERE airline_id = %s
            """,
            (airline_id,),
        )
        usage_count = cursor.fetchone()[0]

        # Ambil data asli
        cursor.execute(
            """
            SELECT airline_id, code, name, country
            FROM airlines
            WHERE airline_id = %s
            """,
            (airline_id,),
        )
        row = cursor.fetchone()

        if not row:
            console.print("[red]Maskapai tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Maskapai yang Akan Dihapus",
            ["ID", "Kode", "Nama", "Negara"],
            [row],
        )

        if usage_count > 0:
            console.print(
                f"[red]Tidak dapat menghapus maskapai.[/red]\n"
                f"[yellow]Karena masih digunakan di {usage_count} data penerbangan (FK constraint).[/yellow]"
            )
            console.print(
                "[dim]Hapus/ubah data penerbangan terkait terlebih dahulu jika ingin menghapus maskapai ini.[/dim]"
            )
            return

        confirm = console.input(
            "\n[bold red]Yakin menghapus maskapai ini? (y/n): [/bold red]"
        ).strip().lower()

        if confirm != "y":
            console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
            return

        cursor.execute("DELETE FROM airlines WHERE airline_id = %s", (airline_id,))
        conn.commit()
        console.print("[bold green]✅ Maskapai berhasil dihapus.[/bold green]")

    except Error as e:
        conn.rollback()
        console.print(f"[red]Error menghapus maskapai:[/red] {e}")
    finally:
        cursor.close()



# =========================================================
# MANAGE CITIES
# =========================================================

# ---------- MAINTAIN CITIES ----------

def manage_cities(conn):
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
                    "[bold white][1][/bold white] Menambah Data Kota Baru",
                    "[bold white][2][/bold white] Mencari & Mengubah Data Kota",
                    "[bold white][3][/bold white] Mencari & Menghapus Kota",
                    "",
                    "[bold white][0][/bold white] Kembali",
                ]
            ),
            title="[bold green]Menu Kota[/bold green]",
            border_style="green",
        )
        console.print(menu_panel)

        choice = console.input("[bold cyan]Pilih menu:[/bold cyan] ").strip()
        if choice == "1":
            _add_city(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "2":
            _search_and_update_city(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "3":
            _search_and_delete_city(conn)
            console.input("\n[dim]Tekan Enter untuk kembali...[/dim]")
        elif choice == "0":
            break
        else:
            console.print("[red]Pilihan tidak valid.[/red]")
            console.input("\n[dim]Tekan Enter untuk melanjutkan...[/dim]")

# ---------- LIST CITIES ----------

def _list_cities(conn):
    """
    Dipakai di banyak tempat (add hotel/flight dll), jadi keep simple & reusable.
    """
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT
                city_id,
                COALESCE(city_code, ''),
                name,
                COALESCE(country_code, ''),
                COALESCE(country_name, ''),
                created_at
            FROM cities
            ORDER BY country_name, name
            """
        )
        rows = cursor.fetchall()
        if not rows:
            console.print("[yellow]Belum ada data kota.[/yellow]")
            return

        _show_table(
            "Daftar Kota (Top 50)",
            ["ID Kota", "Kode Kota", "Nama Kota", "Kode Negara", "Nama Negara", "Dibuat"],
            rows,
        )
    except Error as e:
        console.print(f"[red]Error menampilkan kota:[/red] {e}")
    finally:
        cursor.close()

# ---------- ADD CITY ----------

def _add_city(conn):
    
    console.print("\n")
    header = Panel.fit(
    "[bold magenta]Tambah Kota Baru[/bold magenta]",
    border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    name = console.input("Nama kota: ").strip()
    if not name:
        console.print("[red]Nama kota wajib diisi.[/red]")
        return

    city_code = console.input("Kode Kota: ").strip()
    country_name = console.input("Nama negara: ").strip()
    country_code = console.input("Kode negara: ").strip().upper()

    if not country_name or not country_code:
        console.print("[red]Nama negara dan kode negara wajib diisi.[/red]")
        return

    if len(country_code) != 2:
        console.print("[red]Kode negara harus 2 huruf (ISO2).[/red]")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO cities (city_code, name, country_code, country_name)
            VALUES (%s, %s, %s, %s)
            """,
            (city_code or None, name, country_code, country_name),
        )
        conn.commit()
        console.print("[bold green]✅ Kota baru berhasil ditambahkan.[/bold green]")
    except Error as e:
        conn.rollback()
        # kemungkinan duplicate (UNIQUE(name,country_code))
        if "Duplicate" in str(e):
            console.print(
                "[red]Gagal: kombinasi nama kota + kode negara sudah ada (UNIQUE constraint).[/red]"
            )
        else:
            console.print(f"[red]Error menambah kota:[/red] {e}")
    finally:
        cursor.close()

# ---------- SEARCH CITIES ----------

def _search_cities(conn):
    """
    Pencarian kota berdasarkan:
    - Nama kota (LIKE)
    - Kode kota (LIKE)
    - Nama negara (LIKE)
    - Kode negara (persis)
    """
    console.print("\n[dim]Silakan masukkan kriteria pencarian kota.[/dim]\n")

    console.print("[bold green]Cari Kota[/bold green]")
    console.print("[dim]Kosongkan field jika tidak ingin dipakai sebagai filter.[/dim]\n")

    name_kw = console.input("Nama Kota: ").strip()
    city_code_kw = console.input("Kode Kota: ").strip()
    country_name_kw = console.input("Nama Negara: ").strip()
    country_code_kw = console.input("Kode Negara (2 huruf, mis. ID): ").strip().upper()

    where = []
    params = []

    if name_kw:
        where.append("name LIKE %s")
        params.append(f"%{name_kw}%")
    if city_code_kw:
        where.append("city_code LIKE %s")
        params.append(f"%{city_code_kw}%")
    if country_name_kw:
        where.append("country_name LIKE %s")
        params.append(f"%{country_name_kw}%")
    if country_code_kw:
        if len(country_code_kw) != 2:
            console.print("[red]Kode negara harus 2 huruf (misalnya ID, US, JP).[/red]")
            return []
        where.append("country_code = %s")
        params.append(country_code_kw)

    query = """
        SELECT
            city_id,
            COALESCE(city_code, ''),
            name,
            COALESCE(country_code, ''),
            COALESCE(country_name, '')
        FROM cities
    """
    if where:
        query += " WHERE " + " AND ".join(where)
    query += " ORDER BY country_name, name LIMIT 100"

    cursor = conn.cursor()
    try:
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        if not rows:
            console.print("[magenta]Tidak ada kota yang cocok dengan kriteria.[/magenta]")
            return []
        _show_table(
            "Hasil Pencarian Kota",
            ["ID Kota", "Kode Kota", "Nama Kota", "Kode Negara", "Nama Negara"],
            rows,
        )
        return rows
    except Error as e:
        console.print(f"[red]Error saat mencari kota:[/red] {e}")
        return []
    finally:
        cursor.close()

# ---------- UPDATE CITY (via search) ----------

def _search_and_update_city(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Cari & Update Kota[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_cities(conn)
    if not rows:
        return

    try:
        city_id = int(console.input("[bold cyan]\nMasukkan ID Kota yang akan Diubah: [/bold cyan]").strip())
    except ValueError:
        console.print("[red]ID kota tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT
                city_id,
                COALESCE(city_code, ''),
                name,
                COALESCE(country_code, ''),
                COALESCE(country_name, '')
            FROM cities
            WHERE city_id = %s
            """,
            (city_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Kota tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Kota Saat Ini",
            ["ID Kota", "Kode Kota", "Nama Kota", "Kode Negara", "Nama Negara"],
            [row],
        )

        console.print("[dim]Kosongkan input jika tidak ingin mengubah field tersebut.[/dim]\n")

        new_city_code = console.input(f"Kode Kota ([yellow bold]{row[1]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_name = console.input(f"Nama Kota ([yellow bold]{row[2]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_country_code = console.input(f"Kode Negara ([yellow bold]{row[3]}[/yellow bold]): ",
            markup=True
        ).strip()

        new_country_name = console.input(f"Nama Negara ([yellow bold]{row[4]}[/yellow bold]): ",
            markup=True
        ).strip()

        updates = []
        params = []

        if new_city_code:
            updates.append("city_code = %s")
            params.append(new_city_code)

        if new_name:
            updates.append("name = %s")
            params.append(new_name)

        if new_country_code:
            if len(new_country_code) != 2:
                console.print("[red]Kode negara harus 2 huruf.[/red]")
                return
            updates.append("country_code = %s")
            params.append(new_country_code)

        if new_country_name:
            updates.append("country_name = %s")
            params.append(new_country_name)

        if not updates:
            console.print("[magenta]Tidak ada perubahan yang dilakukan.[/magenta]")
            return

        params.append(city_id)
        query = f"UPDATE cities SET {', '.join(updates)} WHERE city_id = %s"

        try:
            cursor.execute(query, tuple(params))
            conn.commit()
            console.print("[bold green]✅ Data Kota Berhasil Diubah.[/bold green]")
        except Error as e:
            conn.rollback()
            if "Duplicate" in str(e):
                console.print(
                    "[red]Gagal: kombinasi nama kota + kode negara duplikat (UNIQUE constraint).[/red]"
                )
            else:
                console.print(f"[red]Error update kota:[/red] {e}")
    finally:
        cursor.close()

# ---------- DELETE CITY (via search) ----------

def _search_and_delete_city(conn):
    console.print("\n")
    header = Panel.fit(
        "[bold magenta]Cari & Hapus Kota[/bold magenta]",
        border_style="magenta",
    )
    console.print(header, justify="center")
    console.print("\n")

    rows = _search_cities(conn)
    if not rows:
        return

    try:
        city_id = int(console.input("[bold cyan]\nMasukkan ID Kota yang akan Dihapus: [bold cyan]").strip())
    except ValueError:
        console.print("[red]ID kota tidak valid.[/red]")
        return

    cursor = conn.cursor()
    try:
        # Cek penggunaan di HOTELS
        cursor.execute(
            "SELECT COUNT(*) FROM hotels WHERE city_id = %s",
            (city_id,),
        )
        hotel_count = cursor.fetchone()[0] or 0

        # Cek penggunaan di FLIGHTS (from / to)
        cursor.execute(
            """
            SELECT 
                SUM(CASE WHEN from_city_id = %s THEN 1 ELSE 0 END) AS as_origin,
                SUM(CASE WHEN to_city_id   = %s THEN 1 ELSE 0 END) AS as_destination
            FROM flights
            """,
            (city_id, city_id),
        )
        row_usage = cursor.fetchone()
        as_origin = row_usage[0] or 0
        as_destination = row_usage[1] or 0
        flights_total = as_origin + as_destination

        # Ambil detail kota
        cursor.execute(
            """
            SELECT
                city_id,
                COALESCE(city_code, ''),
                name,
                COALESCE(country_code, ''),
                COALESCE(country_name, '')
            FROM cities
            WHERE city_id = %s
            """,
            (city_id,),
        )
        row = cursor.fetchone()
        if not row:
            console.print("[red]Kota tidak ditemukan.[/red]")
            return

        _show_table(
            "Data Kota yang akan Dihapus",
            ["ID Kota", "Kode Kota", "Nama Kota", "Kode Negara", "Nama Negara"],
            [row],
        )

        console.print(
            f"[yellow]Kota ini digunakan di {hotel_count} hotel, "
            f"{flights_total} penerbangan (origin: {as_origin}, destination: {as_destination}).[/yellow]"
        )

        confirm = console.input(
            "\n[bold red]Yakin ingin menghapus kota ini? (y/n): [/bold red]"
        ).strip().lower()
        if confirm != "y":
            console.print("[yellow]Penghapusan dibatalkan.[/yellow]")
            return

        if hotel_count > 0 or flights_total > 0:
            console.print(
                "[red]Tidak dapat menghapus kota yang masih digunakan di HOTELS/FLIGHTS (FK constraint).[/red]"
            )
            console.print(
                "[dim]Pindahkan atau hapus data hotel & penerbangan terkait terlebih dahulu jika benar-benar harus dihapus.[/dim]"
            )
            return

        cursor.execute("DELETE FROM cities WHERE city_id = %s", (city_id,))
        conn.commit()
        console.print("[bold green]✅ Kota berhasil dihapus.[/bold green]")
    except Error as e:
        conn.rollback()
        console.print(f"[red]Error menghapus kota:[/red] {e}")
    finally:
        cursor.close()
