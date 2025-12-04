# ✈️ Travel Agency Management System

A fully-interactive terminal dashboard application built with Python + MySQL, designed for end-to-end travel management.

This project serves as a real-world implementation of database design, CRUD operations, analytics, visualization, software modularity, and clean system architecture.

--- 

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/CLI-Application-success?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Rich-UI-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

---
## Features
- 👤 Manage Users
- 🏨 Manage Hotels
- ✈️ Manage Flights
- 📅 Create & Cancel Trips
- 📊 Analytical Reports
- 📈 Business Dashboards
- 🖥️ Rich Terminal UI
  
---
## 🗂️ Table of Contents
- 📘 Project Overview
- 🏢 Business Workflow
- 🧱 System Architecture
- 🗄️ Database Design
- 🖥️ Application Screenshots
- 📊 Reports & Analytics
- 📈 Visualization Dashboard
- 🔧 Tech Stack
- 🧠 Key Concepts
- ▶️ Running the Project
- 📦 Folder Structure
- 📜 License

---

## 📘 Project Overview
This system enables travel agencies to manage all aspects of their business operations:
- Customer management
- Hotel inventory
- Flight data
- Trip creation and cancellation
- Analytical insights for business decisions

--- 
## 🏢 Business Workflow
1. Customer pilih rute 
2. Customer pilih hotel 
3. Customer pilih penerbangan 
4. Customer menentukan tanggal
5. Sistem menghitung biaya
6. Perjalanan dijadwalkan
7. Customer dapat membatalkan trip
8. Sistem menghasilkan laporan dan insight

---

### 🧱 System Architecture

```js

+--------------------------+
|         main.py          |
+--------------------------+
            |
            v
+--------------------------+
|    TravelAgencyApp       |   ← Main Controller / Menus
+--------------------------+
   |           |          |
 Views     Reports   Visualizations
   |           |          |
   v           v          v
       MySQL Database

```

---

## 🗄️ Database Design

#### 📌 Entity Relationship Diagram (ERD)

<p align="center">
  <img src="travel-agency-project/database/ERD_travel_agency_db.png" width="700">
</p>

#### 🔍 Entities 

| Table        | Description                |
| ------------ | -------------------------- |
| **users**    | Customer info              |
| **hotels**   | Hotel listing              |
| **cities**   | Normalized city table      |
| **airlines** | Normalized airline table   |
| **flights**  | Flight schedules & pricing |
| **trips**    | Customer trip data         |


#### Key Database Features
- Fully normalized to 3NF
- Strong referential integrity via FK
- Lookup tables (cities, airlines) 
- Auto-calculated trip cost
- Status management for cancellations

---

## 🖥️ Application Screenshots

### 📟 Main Menu

<p align="center">
  <img src="travel-agency-project/screenshot/Menu Utama.png" width="600">
</p>

### 👤 Users Table
<p align="center">
  <img src="travel-agency-project/screenshot/Tampilkan Daftar Pengguna.png" width="600">
</p>

### 🏨 Hotels Table
<p align="center">
  <img src="travel-agency-project/screenshot/Tampilkan Daftar Hotel.png" width="600">
</p>

### ✈️ Flights Table
<p align="center">
  <img src="travel-agency-project/screenshot/Tampilkan Daftar Penerbangan.png" width="600">
</p>

### 📅 Trips View 
<p align="center">
  <img src="travel-agency-project/screenshot/Lihat Daftar Perjalanan.png" width="600">
</p>

--- 

## 📊 Reports & Analytics
All analytical reports are located in reports.py and rendered with rich.table.

| No | Laporan                         |
| -- | ------------------------------- |
| 1  | Top Routes by Revenue           |
| 2  | Most Popular Destinations       |
| 3  | Average Spend per User          |
| 4  | Top Airlines by Revenue         |
| 5  | Hotel Occupancy Ranking         |
| 6  | Average Trip Duration           |
| 7  | Travel Patterns (City Pairs)    |
| 8  | Average Flight Price by Airline |
| 9  | User Segmentation by Occupation |
| 10 | Monthly Revenue (Time Series)   |


#### 📊 Top Routes by Revenue Report
<p align="center">
  <img src="travel-agency-project/screenshot/Rute Teratas berdasarkan Pendapatan.png" width="550">
</p>

#### 📊 Most Popular Destinations Report 
<p align="center">
  <img src="travel-agency-project/screenshot/Destinasi Paling Populer.png" width="550">
</p>

#### 📊 Average Spend per User Report 
<p align="center">
  <img src="travel-agency-project/screenshot/Rata-rata Pengeluaran per Pengguna  .png" width="550">
</p>

#### 📊 Top Airlines by Revenue Report
<p align="center">
  <img src="travel-agency-project/screenshot/Maskapai dengan Pendapatan Tertinggi.png" width="550">
</p>

#### 📊 Hotel Occupancy Ranking Report
<p align="center">
  <img src="travel-agency-project/screenshot/Peringkat Hotel berdasarkan Penggunaan.png" width="550">
</p>

#### 📊 Average Trip Duration Report
<p align="center">
  <img src="travel-agency-project/screenshot/Rata-rata Durasi Perjalanan per Destinasi.png" width="550">
</p>

#### 📊 Travel Patterns (City Pairs) Report
<p align="center">
  <img src="travel-agency-project/screenshot/Pola Perjalanan (Origin → Destination).png" width="550">
</p>

#### 📊 Average Flight Price by Airline Report
<p align="center">
  <img src="travel-agency-project/screenshot/Rata-rata Harga Tiket per Maskapai.png" width="550">
</p>

#### 📊 User Segmentation by Occupation Report
<p align="center">
  <img src="travel-agency-project/screenshot/Segmentasi Pengguna berdasarkan Profesi.png" width="550">
</p>

#### 📊 Monthly Revenue (Time Series)
<p align="center">
  <img src="travel-agency-project/screenshot/Pendapatan Bulanan.png" width="550">
</p>

---

## 📈 Visualization Dashboard
Visualizations in visualizations.py include:

#### ✔ KPI Scorecard (6 Metrics)
- Total revenue
- Total trips
- Unique users
- Avg revenue per trip
- Avg revenue per user
- Cancellation rate


<p align="center">
  <img src="travel-agency-project/screenshot/Ringkasan KPI Utama - Scorecard.png" width="600">
</p>

#### ✔ Horizontal Bar: Top Routes

<p align="center">
  <img src="travel-agency-project/screenshot/Rute Teratas berdasarkan Pendapatan - Chart.png" width="600">
</p>

#### ✔ Bar Chart: Most Popular Destinations

<p align="center">
  <img src="travel-agency-project/screenshot/Destinasi Paling Populer - Chart.png" width="600">
</p>

#### ✔ Line Chart: Monthly Revenue Trend

<p align="center">
  <img src="travel-agency-project/screenshot/Tren Pendapatan Bulanan - Chart.png" width="600">
</p>

#### ✔ Line Chart: Cancellation Rate Over Time

<p align="center">
  <img src="travel-agency-project/screenshot/Tren Persentase Pembatalan Perjalanan - Chart.png" width="600">
</p>

### Styled with:
- Corporate color scheme
- Clear typography
- Value labels
- Grid support

---

## 🔧 Tech Stack

### Backend
- MySQL 8.0
- SQL constraints + foreign keys
- Analytical queries (GROUP BY, JOIN, aggregations)


### Python Libraries

| Library                  | Purpose                           |
| ------------------------ | --------------------------------- |
| `mysql-connector-python` | database connection               |
| `rich`                   | CLI dashboard & table formatting  |
| `matplotlib`             | charts and business visualization |
| `numpy`                  | numerical calculations            |
| `datetime`               | date validation                   |
| `os`, `sys`              | system utilities                  |

---

## 🧠 Key Concepts Demonstrated
✅ Relational Database Modeling (3NF)
✅ ERD Design
✅ SQL Query Optimization
✅ Exception Handling
✅ Modular Programming
✅ Rich CLI UI
✅ Data Visualization
✅ Analytical Reporting
✅ Scorecard Design
✅ Clean Architecture for CLI Apps

--- 
## ▶️ Running the Project
#### 1️⃣ Install Dependencies

``` pip install mysql-connector-python rich matplotlib numpy
```

#### 2️⃣ Import Database Schema
```
mysql -u root -p < travel_agency_db.sql
```

#### 3️⃣ Update Database Credentials (config.py)
```
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "yourpassword"
DB_NAME = "travel_agency_db"
```

#### 4️⃣ Run Application
```
python main.py
```

--- 

## 📦 Folder Structure
```
travel-agency-project/
│
├── main.py
├── README.md
│
└── travel_agency/
    ├── __init__.py
    ├── app.py
    ├── db.py
    ├── config.py
    ├── views.py
    ├── trips.py
    ├── reports.py
    ├── visualizations.py
│
└── database/
    ├── ERD_travel_agency_db.png
    ├── travel_agency_db.sql
│
└── screenshots/
    ├── Menu Utama.png
    ├── Tampilkan Daftar Pengguna.png
    ├── Tampilkan Daftar Hotel.png
    ├── Tampilkan Daftar Penerbangan.png
    └── Lihat Daftar Perjalanan.png
    └── Rute Teratas berdasarkan Pendapatan.png
    └── Destinasi Paling Populer.png
    └── Rata-rata Pengeluaran per Pengguna.png
    └── Maskapai dengan Pendapatan Tertinggi.png
    └── Peringkat Hotel berdasarkan Penggunaan.png
    └── Rata-rata Durasi Perjalanan per Destinasi.png
    └── Pola Perjalanan (Origin → Destination).png
    └── Rata-rata Harga Tiket per Maskapai.png
    └── Segmentasi Pengguna berdasarkan Profesi.png
    └── Pendapatan Bulanan.png
    └── Ringkasan KPI Utama - Scorecard.png.png
    └── Rute Teratas berdasarkan Pendapatan - Chart.png
    └── Destinasi Paling Populer - Chart.png
    └── Tren Pendapatan Bulanan - Chart.png
    └── Tren Persentase Pembatalan Perjalanan - Chart.png
```

---

## 📜 License

This project is licensed under the MIT License — free to use and modify.

--- 

## 🚀 Enhancement Options
If you want the README to look even more premium, I can add:
- ✨ Animated GIF demo of the terminal dashboard
- ✨ Mermaid.js diagrams for GitHub
- ✨ Sequence diagram of trip creation
- ✨ Detailed changelog + contribution guide