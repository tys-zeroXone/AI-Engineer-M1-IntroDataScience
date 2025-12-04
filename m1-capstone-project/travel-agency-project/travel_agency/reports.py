from mysql.connector import Error

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def report_top_routes_by_revenue(conn):
    cursor = conn.cursor()
    query = """
        SELECT 
            c_from.name AS from_city,
            c_to.name AS to_city,
            SUM(t.total_flight_price) AS total_revenue,
            COUNT(*) AS total_trips
        FROM trips t
        JOIN flights f_out ON t.outbound_flight_id = f_out.flight_id
        JOIN cities c_from ON f_out.from_city_id = c_from.city_id
        JOIN cities c_to   ON f_out.to_city_id   = c_to.city_id
        GROUP BY from_city, to_city
        ORDER BY total_revenue DESC
        LIMIT 10
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Rute Teratas berdasarkan Pendapatan[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Dari", style="white")
        table.add_column("Ke", style="white")
        table.add_column("Total Perjalanan", justify="right")
        table.add_column("Pendapatan", justify="right")

        if rows:
            for from_city, to_city, revenue, trips in rows:
                table.add_row(
                    from_city,
                    to_city,
                    str(trips),
                    f"${revenue:,.2f}",
                )
        else:
            table.add_row("-", "-", "0", "$0.00")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()


def report_most_popular_destinations(conn):
    cursor = conn.cursor()
    query = """
        SELECT 
            c.name AS city,
            COUNT(t.trip_id) AS total_visits
        FROM trips t
        JOIN hotels h ON t.hotel_id = h.hotel_id
        JOIN cities c ON h.city_id = c.city_id
        GROUP BY city
        ORDER BY total_visits DESC
        LIMIT 10
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Destinasi Paling Populer[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Kota", style="white")
        table.add_column("Total Kunjungan", justify="right")

        if rows:
            for city, total_visits in rows:
                table.add_row(city, str(total_visits))
        else:
            table.add_row("No data", "0")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()


def report_average_spend_per_user(conn):
    cursor = conn.cursor()
    query = """
        SELECT 
            u.user_id,
            u.name,
            AVG(t.total_trip_cost) AS avg_spend,
            SUM(t.total_trip_cost) AS total_spend,
            COUNT(t.trip_id) AS number_of_trips
        FROM users u
        JOIN trips t ON u.user_id = t.user_id
        GROUP BY u.user_id, u.name
        ORDER BY total_spend DESC
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Rata-rata Pengeluaran per Pengguna[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("ID Pengguna", justify="right")
        table.add_column("Nama", style="white")
        table.add_column("Total Perjalanan", justify="right")
        table.add_column("Rata-rata Pengeluaran", justify="right")
        table.add_column("Total Pengeluaran", justify="right")

        if rows:
            for user_id, name, avg_spend, total_spend, trips in rows:
                table.add_row(
                    str(user_id),
                    name,
                    str(trips),
                    f"${avg_spend:,.2f}",
                    f"${total_spend:,.2f}",
                )
        else:
            table.add_row("-", "No data", "0", "$0.00", "$0.00")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()


def report_top_airlines_by_revenue(conn):
    cursor = conn.cursor()
    query = """
        SELECT 
            al.name AS airline,
            SUM(t.total_flight_price) AS revenue,
            COUNT(t.trip_id) AS total_trips
        FROM trips t
        JOIN flights f ON t.outbound_flight_id = f.flight_id
        JOIN airlines al ON f.airline_id = al.airline_id
        GROUP BY al.name
        ORDER BY revenue DESC
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Maskapai dengan Pendapatan Tertinggi[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Maskapai Penerbangan", style="white")
        table.add_column("Total Perjalanan", justify="right")
        table.add_column("Pendapatan", justify="right")

        if rows:
            for airline, revenue, trips in rows:
                table.add_row(
                    airline,
                    str(trips),
                    f"${revenue:,.2f}",
                )
        else:
            table.add_row("No data", "0", "$0.00")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()


def report_hotel_occupancy(conn):
    cursor = conn.cursor()
    query = """
        SELECT
            h.hotel_name,
            c.name AS city,
            COUNT(t.trip_id) AS hotel_visits,
            SUM(t.days) AS total_nights,
            SUM(t.total_hotel_price) AS total_revenue
        FROM trips t
        JOIN hotels h ON t.hotel_id = h.hotel_id
        JOIN cities c ON h.city_id = c.city_id
        GROUP BY h.hotel_id, h.hotel_name, city
        ORDER BY total_revenue DESC
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Peringkat Hotel berdasarkan Penggunaan[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Hotel", style="white")
        table.add_column("Kota", style="white")
        table.add_column("Total Kunjungan", justify="right")
        table.add_column("Total Okupansi (hari)", justify="right")
        table.add_column("Pendapatan", justify="right")

        if rows:
            for hotel_name, city, visits, nights, revenue in rows:
                table.add_row(
                    hotel_name,
                    city,
                    str(visits),
                    str(nights),
                    f"${revenue:,.2f}",
                )
        else:
            table.add_row("No data", "", "0", "0", "$0.00")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()


def report_average_trip_duration_per_destination(conn):
    cursor = conn.cursor()
    query = """
        SELECT 
            c.name AS destination,
            AVG(t.days) AS avg_trip_days
        FROM trips t
        JOIN hotels h ON t.hotel_id = h.hotel_id
        JOIN cities c ON h.city_id = c.city_id
        GROUP BY destination
        ORDER BY avg_trip_days DESC
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Rata-rata Durasi Perjalanan per Destinasi[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Destinasi Perjalanan", style="white")
        table.add_column("Rata- rata Durasi Perjalanan (Hari)", justify="right")

        if rows:
            for dest, avg_days in rows:
                table.add_row(dest, f"{avg_days:.2f}")
        else:
            table.add_row("No data", "0")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()


def report_popular_city_pairs(conn):
    cursor = conn.cursor()
    query = """
        SELECT
            c_from.name AS origin,
            c_to.name AS destination,
            COUNT(*) AS trip_count
        FROM trips t
        JOIN flights f ON t.outbound_flight_id = f.flight_id
        JOIN cities c_from ON f.from_city_id = c_from.city_id
        JOIN cities c_to ON f.to_city_id = c_to.city_id
        GROUP BY origin, destination
        ORDER BY trip_count DESC
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Pola Perjalanan Populer[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Kota Asal", style="white")
        table.add_column("Kota Tujuan", style="white")
        table.add_column("Total Perjalanan", justify="right")

        if rows:
            for origin, dest, count in rows:
                table.add_row(origin, dest, str(count))
        else:
            table.add_row("No data", "", "0")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()


def report_avg_flight_price_by_airline(conn):
    cursor = conn.cursor()
    query = """
        SELECT
            al.name AS airline,
            AVG(f.price) AS avg_price,
            MIN(f.price) AS min_price,
            MAX(f.price) AS max_price
        FROM flights f
        JOIN airlines al ON f.airline_id = al.airline_id
        GROUP BY airline
        ORDER BY avg_price DESC
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Rata-rata Harga Tiket per Maskapai[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Maskapai Penerbangan", style="white")
        table.add_column("Harga Rata-rata", justify="right")
        table.add_column("Harga Minimum", justify="right")
        table.add_column("Harga Maksimum", justify="right")

        if rows:
            for airline, avg_price, min_price, max_price in rows:
                table.add_row(
                    airline,
                    f"${avg_price:,.2f}",
                    f"${min_price:,.2f}",
                    f"${max_price:,.2f}",
                )
        else:
            table.add_row("No data", "$0.00", "$0.00", "$0.00")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()


def report_user_segmentation_by_occupation(conn):
    cursor = conn.cursor()
    query = """
        SELECT
            u.occupation,
            COUNT(DISTINCT u.user_id) AS total_users,
            SUM(t.total_trip_cost) AS total_spent,
            AVG(t.total_trip_cost) AS avg_spent_per_trip
        FROM users u
        JOIN trips t ON u.user_id = t.user_id
        GROUP BY u.occupation
        ORDER BY total_spent DESC
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Segmentasi Pengguna berdasarkan Profesi[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Pekerjaan", style="white")
        table.add_column("Pengguna", justify="right")
        table.add_column("Total Pengeluaran", justify="right")
        table.add_column("Rata-rata Pengeluaran / Perjalanan", justify="right")

        if rows:
            for occ, users_count, total_spent, avg_spent in rows:
                table.add_row(
                    occ,
                    str(users_count),
                    f"${total_spent:,.2f}",
                    f"${avg_spent:,.2f}",
                )
        else:
            table.add_row("No data", "0", "$0.00", "$0.00")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()


def report_monthly_revenue(conn):
    cursor = conn.cursor()
    query = """
        SELECT
            DATE_FORMAT(trip_start_date, '%Y-%m') AS month,
            SUM(total_trip_cost) AS total_revenue,
            COUNT(*) AS trip_count
        FROM trips
        GROUP BY month
        ORDER BY month
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        console.clear()
        console.print("\n")
        header = Panel.fit(
            "[bold magenta]Pendapatan Bulanan[/bold magenta]",
            border_style="magenta",
        )
        console.print(header, justify="center")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Bulan", style="white")
        table.add_column("Perjalanan", justify="right")
        table.add_column("Pendapatan", justify="right")

        if rows:
            for month, revenue, count in rows:
                table.add_row(
                    month,
                    str(count),
                    f"${revenue:,.2f}",
                )
        else:
            table.add_row("No data", "0", "$0.00")

        console.print(table)
    except Error as e:
        console.print(f"[red]Error:[/red] {e}")
    finally:
        cursor.close()
