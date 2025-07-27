# SNMPy: Network Monitoring Dashboard for CNAM 🇹🇳

SNMPy is a Flask-based web application that visualizes the real-time status of 100+ WAN sites of CNAM Tunisia on a map. It monitors latency and SNMP metrics using ICMP and SNMP polling, with PostgreSQL for persistence and Telegram alerts for incidents.


## 🖼️ Screenshots

| Dashboard | Map View + Labels |
|----------|-------------------|
| ![Dashboard View](/preview/dashboard.png) | ![Map+Label View](/preview/maplabel.png) |

| SNMP Monitor | Manual Testing |
|-------------|----------------|
| ![SNMP Monitor View](/preview/snmp.png) | ![Manual View](/preview/manual.png) |

| Alerts | Charts | DB Table |
|--------|--------|-----------|
| ![Alerts View](/preview/alerts.png) | ![Charts View](/preview/charts.png) | ![DB Table View](/preview/dbsc.png) |




---

## 🌐 Features

- 🗺 **Live Map Dashboard** — Shows WAN sites on a map of Tunisia with real-time latency and SNMP info.
- 📡 **SNMP Polling** — Polls site-specific OIDs dynamically loaded from JSON.
- 📶 **ICMP Latency Checks** — Tracks uptime and latency with ping tests.
- 📈 **Charts & Stats** — Displays site statuses and trends.
- 🔔 **Telegram Alerts** — Sends downtime/status change alerts with cooldowns.
- 🔧 **Admin Panel** — Manage SNMP OIDs, logs, and live values via Flask-Admin.
- ⚙️ **Manual Tools** — Manual ping & SNMP polling from the web UI.
- 🔄 **Auto-Sync** — Syncs `sites.json` and `snmp_oids.json` into PostgreSQL on server restart.

---

## 🐳 Getting Started (via Docker)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/snmpy.git
cd snmpy
```

### 2. Configure environment variables

Edit `.env` and set values:

```env
LOGIN_USERNAME=admin
LOGIN_PASSWORD=secret
SECRET_KEY=supersecretkey
TELEGRAM_BOT_TOKEN=xxxxx
TELEGRAM_CHAT_ID=xxxxx
```

### 3. Run the project

```bash
docker compose up --build
```

This launches:
- `web`: Flask app on `http://localhost` 
- `db`: PostgreSQL with data persistence via Docker volume

the web app is accessible from anywhere by IP on port 80.
you might need to add sudo or change port to one higher than 1024.
in prod we use a proxy for that.
---

## 🧠 Project Structure

```
.
├── run.py               # Entry point
├── app/                 # Flask web app (routes, templates, static)
├── core/                # SNMP polling, ICMP logic, background thread
├── db/                  # SQLAlchemy models and DB init
├── config/              # JSON configs for sites and OIDs
├── utils/               # Telegram alerting, auth
├── scripts/             # Helper scripts for dev/testing
├── sim-data/            # SNMP simulator files (.snmprec)
├── Dockerfile           # Python slim container
└── docker-compose.yaml  # Runs web + DB
```

---

## 📊 Web Pages

- `/` — Summary dashboard
- `/map` — Geographic map view of WAN sites
- `/charts` — Uptime/latency chart logs
- `/snmp` — SNMP metric table by site
- `/logs` — ICMP logs
- `/manual` — Manual ping/SNMP tool
- `/alerts` — Telegram alert log
- `/admin` — Admin interface for DB models

---

## 🔄 Simulating SNMP (Optional)

To simulate SNMP data using [snmpsim](https://github.com/etingof/snmpsim):

```bash
sudo apt install snmpsim
snmpsimd.py --data-dir=sim-data --agent-udpv4-endpoint=:1161
```

Ensure the polling engine inside Docker uses `127.0.0.1` as SNMP target IP.(This is default atm.)
Currently hardcoded for the snmp_get(). So that you don't have to use localhost for all sites pings.
---

## 📦 Dependencies

All Python dependencies are listed in `requirements.txt`, including:

- Flask, SQLAlchemy
- pysnmp, ping3
- psycopg2-binary
- Flask-Admin, Flask-Migrate
- python-dotenv

---

## 🔐 Auth

Basic login is enabled with credentials from `.env`. Admin panel and logs are protected unless `USE_AUTH=False`.
which is the current settings.
u can check config file to change timeout as well.
---

## 📬 Alerts

Telegram alerts are sent when a site's status changes. Cooldown logic prevents spam. You can configure tokens and chat IDs in `.env`.

---

## 🏗 Built With

- Python 3.11 + Flask
- PostgreSQL 15
- Docker & Docker Compose
- SQLAlchemy ORM
- Leaflet.js for mapping
- Chart.js for statistics
- Telegram Bot API

---

## 🧠 Author

Made with ❤️ by Raed Souissi — Network Engineering Intern @ CNAM 🇹🇳  
> _"Infrastructure isn’t just uptime. It’s visibility, clarity, and control."_  

---

## ✅ To Do

- Add SNMP trap support
- Better alerting logic
- Enhance frontend UX
- Export logs to CSV
- Multi-user auth & RBAC

---

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0**.  
You are free to use, study, modify, and share it.  
However, **if you deploy it on a server and expose it publicly**, you must **publish your source code**.

See [`LICENSE`](https://www.gnu.org/licenses/agpl-3.0.html) for full details.
