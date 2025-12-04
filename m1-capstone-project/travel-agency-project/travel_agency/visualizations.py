import numpy as np
import matplotlib.pyplot as plt

from mysql.connector import Error
from rich.console import Console

from .utils import _create_figure, _format_axis, CORPORATE_COLORS

console = Console()

# ========================================================= Ringkasan KPI Utama (Scorecard)       

def viz_key_metrics_overview(conn):
    """
    Key Metrics Overview (Scorecard Style):
    - Total Revenue
    - Total Trips
    - Unique Users
    - Avg Revenue per Trip
    - Avg Revenue per User
    - Cancellation Rate
    Ditampilkan sebagai kumpulan scorecard, bukan bar chart.
    """
    cursor = conn.cursor()
    query = """
        SELECT
            SUM(total_trip_cost) AS total_revenue,
            COUNT(*) AS total_trips,
            COUNT(DISTINCT user_id) AS unique_users,
            SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_trips
        FROM trips
    """
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        if not row or row[1] is None or row[1] == 0:
            console.print("[yellow]Tidak Cukup Data untuk Menampilkan Ringkasan KPI Utama.[/yellow]")
            return

        total_revenue   = float(row[0] or 0)
        total_trips     = int(row[1] or 0)
        unique_users    = int(row[2] or 0)
        cancelled_trips = int(row[3] or 0)

        avg_rev_trip  = total_revenue / total_trips if total_trips else 0
        avg_rev_user  = total_revenue / unique_users if unique_users else 0
        cancel_rate   = (cancelled_trips / total_trips * 100) if total_trips else 0

        # Siapkan data untuk scorecard
        cards = [
            ("Total Pendapatan",       f"${total_revenue:,.0f}"),
            ("Total Perjalanan",         f"{total_trips:,}"),
            ("Total Pengguna",        f"{unique_users:,}"),
            ("Rata-rata Pendapatan / Perjalanan",  f"${avg_rev_trip:,.0f}"),
            ("Rata-rata Pendapatan / Pengguna",  f"${avg_rev_user:,.0f}"),
            ("Ratio Pembatalan Perjalanan",   f"{cancel_rate:,.1f}%"),
        ]

        # Figure: 2 baris x 3 kolom scorecard
        fig, axes = plt.subplots(2, 3, figsize=(12, 6))
        fig.suptitle("Ringkasan KPI Utama (Scorecard)", fontsize=16, fontweight="bold", y=0.98)

        for ax, (title, value) in zip(axes.flatten(), cards):
            ax.set_axis_off()
            # Card background
            ax.set_facecolor("#F4F5F7")
            # Border tipis
            for spine in ax.spines.values():
                spine.set_visible(True)
                spine.set_color(CORPORATE_COLORS["muted"])
                spine.set_linewidth(0.8)

            # Title (kecil, muted)
            ax.text(
                0.5,
                0.65,
                title,
                ha="center",
                va="center",
                fontsize=10,
                color=CORPORATE_COLORS["muted"],
            )
            # Value (besar, bold)
            ax.text(
                0.5,
                0.40,
                value,
                ha="center",
                va="center",
                fontsize=16,
                fontweight="bold",
                color=CORPORATE_COLORS["primary"],
            )

        # Kalau jumlah cards < 6 (future-proof), sisa axes dimatikan
        for ax in axes.flatten()[len(cards):]:
            ax.set_axis_off()

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

    except Error as e:
        console.print(f"[red]Error in viz_key_metrics_overview:[/red] {e}")
    finally:
        cursor.close()


# ========================================================= Rute Teratas berdasarkan Pendapatan
def viz_top_routes_by_revenue(conn):
    cursor = conn.cursor()
    query = """
        SELECT 
            CONCAT(c_from.name, ' → ', c_to.name) AS route,
            SUM(t.total_flight_price) AS total_revenue
        FROM trips t
        JOIN flights f_out ON t.outbound_flight_id = f_out.flight_id
        JOIN cities c_from ON f_out.from_city_id = c_from.city_id
        JOIN cities c_to   ON f_out.to_city_id   = c_to.city_id
        GROUP BY route
        ORDER BY total_revenue DESC
        LIMIT 10
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            console.print("[yellow]Tidak Ada Data yang bisa Divisualisasikan.[/yellow]")
            return

        routes   = [r[0] for r in rows]
        revenues = [float(r[1]) for r in rows]

        fig, ax = _create_figure("Rute Teratas berdasarkan Pendapatan", figsize=(10, 6))

        y_pos = np.arange(len(routes))
        bars = ax.barh(y_pos, revenues, color=CORPORATE_COLORS["primary"])
        ax.set_yticks(y_pos)
        ax.set_yticklabels(routes)
        ax.invert_yaxis()  # route dengan revenue terbesar di paling atas

        # Tambah label nilai di ujung bar
        for i, v in enumerate(revenues):
            ax.text(
                v,
                i,
                f"${v:,.0f}",
                va="center",
                ha="left",
                fontsize=9,
            )

        _format_axis(ax, xlabel="Pendapatan (USD)", grid_y=False)
        plt.tight_layout()
        plt.show()
    except Error as e:
        console.print(f"[red]Error in viz_top_routes_by_revenue:[/red] {e}")
    finally:
        cursor.close()
        

# ========================================================= Destinasi Paling Populer
def viz_most_popular_destinations(conn):
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
        if not rows:
            console.print("[yellow]Tidak Ada Data yang bisa Divisualisasikan.[/yellow]")
            return

        cities = [r[0] for r in rows]
        visits = [int(r[1]) for r in rows]

        fig, ax = _create_figure("Destinasi Paling Populer", figsize=(10, 6))

        x_pos = np.arange(len(cities))
        bars = ax.bar(x_pos, visits, color=CORPORATE_COLORS["primary"])
        ax.set_xticks(x_pos)
        ax.set_xticklabels(cities, rotation=45, ha="right")

        # Label jumlah trip di atas bar
        for i, v in enumerate(visits):
            ax.text(
                i,
                v,
                str(v),
                ha="center",
                va="bottom",
                fontsize=9,
            )

        _format_axis(ax, ylabel="Total Visits", grid_y=True)
        plt.tight_layout()
        plt.show()
    except Error as e:
        console.print(f"[red]Error in viz_most_popular_destinations:[/red] {e}")
    finally:
        cursor.close()


# ========================================================= Tren Pendapatan Bulanan
def viz_monthly_revenue(conn):
    cursor = conn.cursor()
    query = """
        SELECT
            DATE_FORMAT(trip_start_date, '%Y-%m') AS month,
            SUM(total_trip_cost) AS total_revenue
        FROM trips
        GROUP BY month
        ORDER BY month
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            console.print("[yellow]Tidak Ada Data yang bisa Divisualisasikan.[/yellow]")
            return

        months   = [r[0] for r in rows]
        revenues = [float(r[1]) for r in rows]

        fig, ax = _create_figure("Tren Pendapatan Bulanan", figsize=(10, 5))

        ax.plot(
            months,
            revenues,
            marker="o",
            linewidth=2,
            color=CORPORATE_COLORS["primary"],
        )

        # Label setiap titik (boleh dimatikan kalau terasa ramai)
        for x, y in zip(months, revenues):
            ax.text(
                x,
                y,
                f"${y:,.0f}",
                fontsize=8,
                ha="center",
                va="bottom",
            )

        plt.xticks(rotation=45, ha="right")
        _format_axis(ax, xlabel="Month", ylabel="Revenue (USD)", grid_y=True)
        plt.tight_layout()
        plt.show()
    except Error as e:
        console.print(f"[red]Error in viz_monthly_revenue:[/red] {e}")
    finally:
        cursor.close()
