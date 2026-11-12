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

## Tests

```bash
pytest
```

Tests force `PERSISTENCE=memory` via `tests/conftest.py`.

## Default admin

- Email: `admin@example.com`
- Password: `Admin123!`
