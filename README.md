# Backend — Lamborghini Colección API

FastAPI service with layered architecture (API → services → repositories → domain).

## Database (local)

MySQL database `lb` as `root` without password:

```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS lb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

Connection (`.env`):

```env
DATABASE_URL=mysql+pymysql://root@127.0.0.1:3306/lb
PERSISTENCE=sql
```

### Migrations

```bash
cd backend
.\.venv\Scripts\activate
alembic upgrade head
```

## Run

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 7776
```

## Ubuntu systemd service (`lb`)

Keeps the FastAPI API running permanently (restart on crash and on boot).

1. Put the backend on the server (example path `/opt/lb/backend`).
2. Create the venv and install deps:

```bash
cd /opt/lb/backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env   # edit SECRET_KEY, DATABASE_URL, DEBUG=false, CORS, etc.
.venv/bin/alembic upgrade head
```

3. Install and enable the service:

```bash
sudo bash deploy/install-lb-service.sh /opt/lb/backend
```

The unit file is `deploy/lb.service` (service name **`lb`**). It runs:

`uvicorn app.main:app --host 0.0.0.0 --port 7776`

```bash
sudo systemctl status lb
sudo systemctl restart lb
sudo journalctl -u lb -f
```

## Tests

```bash
pytest
```

Tests force `PERSISTENCE=memory` via `tests/conftest.py`.

## Default admin

- Email: `admin@example.com`
- Password: `Admin123!`
